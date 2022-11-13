from artnet_manager import ArtnetManager
import threading


def read_hardware_values():
    while True:
        buffer = A.read_input_hardware()
        if buffer is not None:
            if len(buffer) > 0:
                for x in range(10):
                    print(buffer[x])
                for x in range(10):
                   print(buffer[x + 100])


if __name__ == '__main__':
    A = ArtnetManager(512)
    A.start_output_hardware()
    A.start_input_hardware()

    input_thread = threading.Thread(target=read_hardware_values)
    input_thread.start()

    input("Press Enter to start output")









# A.generate_empty_dmx_output_file()
