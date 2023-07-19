from smbus import SMBus

IODIRA = 0x00  # IO direction A - 1= input 0 = output
IOCON = 0x0A  # Configuration register
GPPUA = 0x0C  # Pull-up resistors for port A
GPIOA = 0x12  # Data port A
GPIOB = 0x13  # Data port B

class I2cKeypadDriver(object):
    i2c_bus: SMBus
    i2cadress: int
    button_states_old: list
    button_states: list
    key_pressed_callback: callable  # callback function that is called when a key is pressed
    key_released_callback: callable  # callback function that is called when a key is released

    def __init__(self, i2c_bus: SMBus, key_pressed_callback: callable, key_released_callback: callable):
        self.i2c_bus = i2c_bus
        self.i2cadress = 0x20
        self.i2c_bus.write_byte_data(self.i2cadress, IOCON, 0x02)  # Update Register
        self.i2c_bus.write_word_data(self.i2cadress, IODIRA, 0xFF00)  # Set A to output and B to input
        self.i2c_bus.write_word_data(self.i2cadress, GPPUA, 0xFF00) # Enable pullup resistors on B
        self.button_states_old = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.button_states = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.key_pressed_callback = key_pressed_callback
        self.key_released_callback = key_released_callback

    def check_for_change(self):
        self.i2c_bus.write_byte_data(self.i2cadress, GPIOA, 0xFF) # set all rows high

        rows = [int("00011110", 2), int("00011101", 2), int("00011011", 2), int("00010111", 2), int("00001111", 2)]

        for row in range(len(rows)):
            self.i2c_bus.write_byte_data(self.i2cadress, GPIOA, rows[row])

            # get the states of the buttons
            row_button_states = [0, 0, 0, 0]
            for bit in range(0, 4):
                row_button_states[bit] = (self.i2c_bus.read_byte_data(
                    self.i2cadress, GPIOB) >> bit) & 1

            # reverse the states
            for i in range(0, 4):
                if row_button_states[i] == 0:
                    row_button_states[i] = 1
                else:
                    row_button_states[i] = 0

            # write the states to the matrix
            self.button_states[row] = row_button_states

        # check if more than 2 buttons are pressed beacuse that would cause a problem
        count = 0
        for row in self.button_states:
            count += row.count(1)
        if count > 2:
            print("Too many buttons pressed")
        else:
            key_counter: int = 1
            for row in range(len(self.button_states)):
                for digit in range(len(self.button_states[row])):
                    if self.button_states[row][digit] != self.button_states_old[row][digit]:
                        if self.button_states[row][digit] == 1:
                            self.key_pressed_callback(key_counter)
                        else:
                            self.key_released_callback(key_counter)
                    key_counter += 1
            
            for row in range(len(self.button_states)):
                for digit in range(len(self.button_states[row])):
                    self.button_states_old[row][digit] = self.button_states[row][digit]