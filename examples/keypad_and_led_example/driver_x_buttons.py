from smbus import SMBus

IODIRA = 0x00  # IO direction A - 1= input 0 = output
IODIRB = 0x01  # IO direction B - 1= input 0 = output
IOCON = 0x0A  # Configuration register
GPPUA = 0x0C  # Pull-up resistors for port A
GPPUB = 0x0D  # Pull-up resistors for port B
GPIOA = 0x12  # Data port A
GPIOB = 0x13  # Data port B
OLATA = 0x14  # Output latches A
OLATB = 0x15  # Output latches B


class XButtons(object):
    i2c_bus: SMBus
    multiplexer_1: int
    button_states_old: list
    button_states: list
    # callback function that is called when a key is pressed
    key_pressed_callback: callable
    # callback function that is called when a key is released
    key_released_callback: callable

    def __init__(self, i2c_bus: SMBus, key_pressed_callback: callable, key_released_callback: callable):
        self.i2c_bus = i2c_bus
        self.multiplexer_1 = 0x21
        self.i2c_bus.write_byte_data(self.multiplexer_1, IOCON, 0x02)  # Update Register
        
        self.i2c_bus.write_word_data(self.multiplexer_1, IODIRA, 0x1F)  # Set Outputs and Inputs of Port A
        self.i2c_bus.write_word_data(self.multiplexer_1, GPPUA, 0x1F) # Enable pullup resistors for Port A
        self.i2c_bus.write_word_data(self.multiplexer_1, IODIRB, 0x1F)  # Set Outputs and Inputs of Port B
        self.i2c_bus.write_word_data(self.multiplexer_1, GPPUB, 0x1F) # Enable pullup resistors for Port B
        
        self.button_states_old = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.button_states = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.key_pressed_callback = key_pressed_callback
        self.key_released_callback = key_released_callback
        print("XButtons initialized")

    def check_for_change(self):
        self.i2c_bus.write_byte_data(self.multiplexer_1, GPIOA, 0x1F)  # set all rows high
        self.i2c_bus.write_byte_data(self.multiplexer_1, GPIOB, 0x1F)  # set all rows high

        rows = [int("01000000", 2), int("00100000", 2)]

        for row in range(len(rows)):
            self.i2c_bus.write_byte_data(self.multiplexer_1, OLATA, rows[row])
            
            # get the states of the first five buttons
            row_button_states_a = [0, 0, 0, 0, 0]
            for bit in range(0, 5):
                row_button_states_a[bit] = (self.i2c_bus.read_byte_data(self.multiplexer_1, GPIOA) >> bit) & 1
            
            # get the states of the last five buttons
            row_button_states_b = [0, 0, 0, 0, 0]
            for bit in range(0, 5):
                row_button_states_b[bit] = (self.i2c_bus.read_byte_data(self.multiplexer_1, GPIOB) >> bit) & 1
                
                
            row_button_states = row_button_states_a + row_button_states_b
            
            #reverse the states
            for i in range(0, 10):
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