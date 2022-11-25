from stupidArtnet import StupidArtnet


class ArtnetSender():
    def __init__(self, universe):
        target_ip = '255.255.255.255'
        packet_size = 512

        self.artnet_client = StupidArtnet(target_ip, universe, packet_size, 30, True, True)  # init artnet client
        self.artnet_client.set_simplified(False)
        self.artnet_client.set_net(0)
        self.artnet_client.set_subnet(0)

        self.artnet_client.start()  # start the artnet client

        self.packet = bytearray(512)  # create empty packet

    def set_channels_to_values(self, channels_values: dict) -> None:
        '''
        input: channels_values: dict with channel as key and value as value
        output: None
        '''

        for channel, value in channels_values.items():  # fill packet with values
            self.packet[int(channel) - 1] = value

        self.artnet_client.set(self.packet)  # send the packet





if __name__ == "__main__":
    a = ArtnetSender(1)
    a.set_channels_to_values({1: 255, 2: 12, 3: 255})
