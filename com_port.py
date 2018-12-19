import serial
import hamming_code
from bitstring import Bits, BitArray


class NetworkStation:
    start_delimiter = Bits(bin='10010000')
    access_control = BitArray(bin='00000000')
    end_delimiter = BitArray(bin='10110100')
    frame_status = BitArray(bin='00000000')
    active_station_flag = True

    def __init__(self, write_port, read_port, baudrate, address, monitor_flag):
        self.write_channel = serial.Serial(port=write_port, baudrate=baudrate, timeout=0)
        self.read_channel = serial.Serial(port=read_port, baudrate=baudrate, timeout=0)
        self.monitor_flag = monitor_flag
        self.priority = 3
        self.mac_address = address
        self.destination_address = None
        self.data = None

    def init_token_ring(self):
        if self.monitor_flag:
            self.write_channel.write(self.start_delimiter.tobytes())
            self.write_channel.write(self.access_control.tobytes())
            self.write_channel.write(self.end_delimiter.tobytes())

    def write_frame(self, data, address, mistake_flag):
        if mistake_flag:
            message = NetworkStation.make_mistake(hamming_code.HammingCode.coding_with_hamming_code(data), 3)
        else:
            message = hamming_code.HammingCode.coding_with_hamming_code(data)
        if address != self.mac_address:
            self.destination_address = address
            self.data = message
        else:
            print('Problem with destination address')

    def read_data(self):
        information = []
        temp_data = bytearray()
        while self.read_channel.in_waiting > 0:
            temp_byte = self.read_channel.read(1)
            temp_data += temp_byte
            if temp_byte == self.end_delimiter.bytes:
                break
        if temp_data:
            information = self.handle_msg(temp_data)
            if information:
                information = hamming_code.HammingCode.encoding_with_hamming_code(information).decode('utf-8')
        return information

    def handle_msg(self, msg):
        frame_flag = self.check_message_field(msg[1], [3], '1')
        if not self.active_station_flag:
            self.data = None
            frame_flag = False
        if not self.data:
            if not frame_flag:
                self.write_channel.write(msg)
            else:
                if msg[2] == self.mac_address:
                    print('Cool')
                    information = bytearray()
                    msg[4] = self.change_message_field(msg[4], [0, 4], 1)
                    end_index = msg.index(self.end_delimiter.tobytes())
                    for i in range(5, end_index):
                        information.append(msg[i])
                    msg[4] = self.change_message_field(msg[4], [1, 5], 1)
                    self.write_channel.write(msg)
                    return information
                elif msg[3] == self.mac_address:
                    print("Ring")
                    if not self.check_message_field(msg[4], [0, 4], '1'):
                        print("Address didn't recognized")
                    if not self.check_message_field(msg[4], [1, 5], '1'):
                        print("Data didn't copy")
                    msg = self.__remove_frame(msg)
                    self.write_channel.write(msg)
                else:
                    self.write_channel.write(msg)
        else:
            print("Mail")
            access_control = BitArray(int=msg[1], length=8)
            priority_bits = access_control[0:3]
            print(priority_bits.int)
            if self.priority > priority_bits.int:
                msg[1] = self.check_priorities(msg[1])
                print("Parcel. Station {} to station {}".format(self.mac_address, self.destination_address))
                msg[2:2] = self.__create_frame()
                msg[1] = self.change_message_field(msg[1], [3], 1)
                self.write_channel.write(msg)
                self.data = None
                self.destination_address = None
                if self.priority > 3:
                    self.priority = 3
            else:
                self.priority += 1

    @staticmethod
    def check_message_field(field, position, value):
        bits_field = BitArray(uint=field, length=8)
        for i in position:
            if bits_field.bin[i] != value:
                return False
        return True

    @staticmethod
    def change_message_field(field, position, value):
        bits_field = BitArray(uint=field, length=8)
        for i in position:
            bits_field[i] = value
        return bits_field.uint

    def check_priorities(self, access_control):
        access_control_bits = BitArray(int=access_control, length=8)
        priority_bits = access_control_bits[0:3]
        reservation_bits = access_control_bits[5:8]
        print(priority_bits.int)
        if self.priority > priority_bits.int:
            access_control_bits[0:3] = self.priority
        elif self.priority > reservation_bits.int:
            access_control_bits[5:8] = self.priority
        return access_control_bits.uint

    def __create_frame(self):
        frame = bytearray()
        frame.append(self.destination_address)
        frame.append(self.mac_address)
        frame.append(self.frame_status.int)
        frame.extend(self.data)
        return frame

    def __remove_frame(self, message):
        message.pop(2)
        message.pop(3)
        end_index = message.index(self.end_delimiter.tobytes())
        for i in range(3, end_index, 1):
            message.pop(3)
        message[1] = self.change_message_field(message[1], [3], 0)
        message[1] = self.change_message_field(message[1], [1, 2], 0)
        return message

    def shutdown(self):
        self.active_station_flag = not self.active_station_flag

    def close_channels(self):
        self.write_channel.close()
        self.read_channel.close()

    @staticmethod
    def make_mistake(data, position):
        temp_data = BitArray(data)
        temp_data.invert(pos=position)
        return temp_data.tobytes()
