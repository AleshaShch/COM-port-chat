import serial, random, time
from bitstring import Bits, BitArray


class ComPort:
    SIZE_OF_PACKET = 7
    SIZE_OF_INFORMATION_PART = 4
    MAX_NUMBER_OF_ACCESS_ATTEMPT = 10
    BIT_TIME = 10 ** (-7)
    COLLISION_WINDOW = 232 * 2 * BIT_TIME

    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=0)
        self.synchrony_flag = Bits(bin='01111110')
        self.mistake_flag = 0
        self.jam_signal = Bits(bin='01100010010101110110001001010111')

    def write_frame(self, data, mistake_flag):
        attempt_count = 0
        while True:
            while not self.is_channel_open():
                pass
            self.write_data(data, mistake_flag)
            #time.sleep(self.COLLISION_WINDOW)
            time.sleep(3)
            if not self.is_collision():
                print("Collision")
                self.serial.write(self.jam_signal.tobytes())
                attempt_count += 1
                if not self.is_late_collision():
                    print("Late collision")
                    return 1
                elif attempt_count > 10:
                    print("Maximum number of transmission attempts")
                    return 2
                time.sleep(random.randrange(0, (2**(min(attempt_count, 10)))))
            else:
                return 0


    def write_data(self, data, mistake_flag):
        if mistake_flag:
            print('With mistake')
            message = self.make_mistake(self.coding_with_hamming_code(data), 3)
        else:
            message = self.coding_with_hamming_code(data)
        self.serial.write(message)


    def read_data_without_flag(self):
        data = []
        temp_data = bytearray()
        while self.serial.in_waiting > 0:
            temp_byte = self.serial.read(1)
            if temp_byte == self.synchrony_flag.bytes:
                print("Synchrony flag")
            else:
                temp_data += temp_byte
        if temp_data:
            if (Bits(temp_data).bin == self.jam_signal.bin):
                return "Jam signal"
            data = self.encoding_with_hamming_code(temp_data).decode('utf-8')
        return data

    def read_data(self):
        data = []
        temp_data = BitArray()
        flag_count = 0
        while 1:
            temp_byte = self.serial.read(1)
            if temp_byte == self.synchrony_flag.bytes:
                if flag_count == 1:
                    data = self.remove_bits(temp_data).decode('utf-8')
                    return data
                else:
                    flag_count += 1
            elif flag_count == 1:
                temp_data += temp_byte

    def coding_with_hamming_code(self, data):
        msg = BitArray()
        packet_list = self.split_message(BitArray(data), self.SIZE_OF_INFORMATION_PART)
        for i in packet_list:
            msg += self.insert_control_bits(i)
        return msg.tobytes()

    def encoding_with_hamming_code(self, data):
        msg, temp_msg = BitArray(), BitArray()
        packet_list = self.split_message(BitArray(data), self.SIZE_OF_PACKET)
        packet_list.pop(-1)
        for i in packet_list:
            temp_msg = self.remove_control_bits(BitArray(i))
            if self.mistake_flag == 1:
                self.mistake_flag = 0
                return 'Mistake'.encode("utf-8", errors="ignore")
            else:
                msg += temp_msg
        return msg.tobytes()

    @staticmethod
    def split_message(bin_data, divider):
        return [bin_data[i:i+divider] for i in range(0, bin_data.len, divider)]

    def remove_control_bits(self, packet):
        counter = 0
        for i in self.get_list_of_power_of_two(self.SIZE_OF_INFORMATION_PART - 1):
            amount = self.check_control_bits(packet, i)
            if amount % 2 == 0 and amount and packet[i - 1] != '0b1':
                self.mistake_flag = 1
                return -1
        for i in self.get_list_of_power_of_two(self.SIZE_OF_INFORMATION_PART - 1):
            del packet[i-1-counter:i-counter]
            counter += 1
        return packet

    def insert_control_bits(self, packet):
        for i in self.get_list_of_power_of_two(self.SIZE_OF_INFORMATION_PART - 1):
            packet.insert('0b0', i -1)
        for i in self.get_list_of_power_of_two(self.SIZE_OF_INFORMATION_PART - 1):
            amount = self.check_control_bits(packet, i)
            if amount % 2 == 0 and amount:
                    packet[i - 1] = '0b1'
        return packet

    @staticmethod
    def make_mistake(data, position):
        temp_data = BitArray(data)
        temp_data.invert(pos=position)
        return temp_data.tobytes()

    @staticmethod
    def check_control_bits(packet, counter):
        amount = 0
        temp_counter = Bits(int=counter, length=4)
        pos = temp_counter.find('0b1')
        pos_int = pos[0]
        for i in range(1, 8):
            temp_pos= Bits(int=i, length=4)
            res = BitArray(temp_pos ^ temp_counter)
            if res._readbin(1, pos_int) == '0' and packet._readbin(1, i - 1) == '1':
                amount += 1
        return amount

    @staticmethod
    def insert_flag_bits(data):
        bit_data = BitArray(data)
        bit_data.replace('0b11111', '0b111110')
        return bit_data.tobytes()

    @staticmethod
    def remove_flag_bits(data):
        temp_data = BitArray(data)
        if temp_data:
            temp_data.replace('0b111110', '0b11111')
        return temp_data.tobytes()

    @staticmethod
    def get_list_of_power_of_two(power):
        return [1 << i for i in range(power)]

    @staticmethod
    def is_channel_open():
        print("Try to access channel")
        return random.randrange(0, 2)

    @staticmethod
    def is_collision():
        return random.randrange(0, 2)

    @staticmethod
    def is_late_collision():
        return random.randrange(0, 2)
