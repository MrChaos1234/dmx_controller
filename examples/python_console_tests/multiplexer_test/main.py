import time
import smbus as SMBus

IODIRA = 0x00  # IO direction A - 1= input 0 = output
IODIRB = 0x01  # IO direction B - 1= input 0 = output
IPOLA = 0x02  # Input polarity A
IPOLB = 0x03  # Input polarity B
GPINTENA = 0x04  # Interrupt-onchange A
GPINTENB = 0x05  # Interrupt-onchange B
DEFVALA = 0x06  # Default value for port A
DEFVALB = 0x07  # Default value for port B
INTCONA = 0x08  # Interrupt control register for port A
INTCONB = 0x09  # Interrupt control register for port B
IOCON = 0x0A  # Configuration register
GPPUA = 0x0C  # Pull-up resistors for port A
GPPUB = 0x0D  # Pull-up resistors for port B
INTFA = 0x0E  # Interrupt condition for port A
INTFB = 0x0F  # Interrupt condition for port B
INTCAPA = 0x10  # Interrupt capture for port A
INTCAPB = 0x11  # Interrupt capture for port B
GPIOA = 0x12  # Data port A
GPIOB = 0x13  # Data port B
OLATA = 0x14  # Output latches A
OLATB = 0x15  # Output latches B


class Multiplexer:
    def __init__(self):
        self.i2c = SMBus.SMBus(1)
        self.i2cadress = 0x20
        self.setup()

    def setup(self):
        self.i2c.write_byte_data(
            self.i2cadress, IOCON, 0x02)  # Update Register
        # Set A to output and B to input
        self.i2c.write_word_data(self.i2cadress, IODIRA, 0xFF00)
        # Enable pullup resistors on B
        self.i2c.write_word_data(self.i2cadress, GPPUA, 0xFF00)

    def test_inputs(self):
        # set all outputs high for testing
        self.i2c.write_byte_data(self.i2cadress, GPIOA, 0xFF00)
        while (True):
            portB_val = self.i2c.read_byte_data(self.i2cadress, GPIOB)
            portB_val_str = str(bin(portB_val))

            # print("Port B: " + portB_val_str)

            button_states = [0, 0, 0, 0]

            # get the states of the buttons
            for bit in range(0, 4):
                button_states[bit] = (portB_val >> bit) & 1

            # reverse the states
            for i in range(0, 4):
                if button_states[i] == 0:
                    button_states[i] = 1
                else:
                    button_states[i] = 0

            print(button_states)
            time.sleep(0.01)

    def test_matrix_logic(self):
        button_states_old = []
        button_states = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]

        while (True):
            # set all rows high
            self.i2c.write_byte_data(self.i2cadress, GPIOA, 0xFF)

            rows = [int("00011110", 2), int("00011101", 2), int(
                "00011011", 2), int("00010111", 2), int("00001111", 2)]

            for row in range(len(rows)):
                self.i2c.write_byte_data(self.i2cadress, GPIOA, rows[row])

                # get the states of the buttons
                row_button_states = [0, 0, 0, 0]
                for bit in range(0, 4):
                    row_button_states[bit] = (self.i2c.read_byte_data(
                        self.i2cadress, GPIOB) >> bit) & 1

                # reverse the states
                for i in range(0, 4):
                    if row_button_states[i] == 0:
                        row_button_states[i] = 1
                    else:
                        row_button_states[i] = 0

                # write the states to the matrix
                button_states[row] = row_button_states

            # check if more than 2 buttons are pressed beacuse that would cause a problem
            count = 0
            for row in button_states:
                count += row.count(1)
            if count > 2:
                print("Too many buttons pressed")

            else:
                for row in button_states:
                    print(row)
                print("\n")

    def keypad_listener(self):
        button_states_old = [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
        button_states = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]

        while (True):
            # set all rows high
            self.i2c.write_byte_data(self.i2cadress, GPIOA, 0xFF)

            rows = [int("00011110", 2), int("00011101", 2), int(
                "00011011", 2), int("00010111", 2), int("00001111", 2)]

            for row in range(len(rows)):
                self.i2c.write_byte_data(self.i2cadress, GPIOA, rows[row])

                # get the states of the buttons
                row_button_states = [0, 0, 0, 0]
                for bit in range(0, 4):
                    row_button_states[bit] = (self.i2c.read_byte_data(
                        self.i2cadress, GPIOB) >> bit) & 1

                # reverse the states
                for i in range(0, 4):
                    if row_button_states[i] == 0:
                        row_button_states[i] = 1
                    else:
                        row_button_states[i] = 0

                # write the states to the matrix
                button_states[row] = row_button_states

            # check if more than 2 buttons are pressed beacuse that would cause a problem
            count = 0
            for row in button_states:
                count += row.count(1)
            if count > 2:
                print("Too many buttons pressed")

            else:
                for row in range(len(button_states)):
                    for digit in range(len(button_states[row])):
                        if button_states[row][digit] != button_states_old[row][digit]:
                            print(button_states)

                for row in range(len(button_states)):
                    for digit in range(len(button_states[row])):
                        button_states_old[row][digit] = button_states[row][digit]


M = Multiplexer()
# M.test_inputs()
# M.test_matrix_logic()
M.keypad_listener()
