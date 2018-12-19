from bitstring import Bits, BitArray


class HammingCode:
    SIZE_OF_PACKET = 7
    SIZE_OF_INFORMATION_PART = 4

    mistake_flag = 0

    @staticmethod
    def coding_with_hamming_code(data):
        msg = BitArray()
        packet_list = HammingCode.split_message(BitArray(data), HammingCode.SIZE_OF_INFORMATION_PART)
        for i in packet_list:
            msg += HammingCode.insert_control_bits(i)
        return msg.tobytes()

    @staticmethod
    def encoding_with_hamming_code(data):
        msg, temp_msg = BitArray(), BitArray()
        packet_list = HammingCode.split_message(BitArray(data), HammingCode.SIZE_OF_PACKET)
        packet_list.pop(-1)
        for i in packet_list:
            temp_msg = HammingCode.remove_control_bits(BitArray(i))
            if HammingCode.mistake_flag == 1:
                HammingCode.mistake_flag = 0
                return 'Mistake'.encode("utf-8", errors="ignore")
            else:
                msg += temp_msg
        return msg.tobytes()

    @staticmethod
    def split_message(bin_data, divider):
        return [bin_data[i:i + divider] for i in range(0, bin_data.len, divider)]

    @staticmethod
    def insert_control_bits(packet):
        for i in HammingCode.get_list_of_power_of_two(HammingCode.SIZE_OF_INFORMATION_PART - 1):
            packet.insert('0b0', i -1)
        for i in HammingCode.get_list_of_power_of_two(HammingCode.SIZE_OF_INFORMATION_PART - 1):
            amount = HammingCode.check_control_bits(packet, i)
            if amount % 2 == 0 and amount:
                    packet[i - 1] = '0b1'
        return packet

    @staticmethod
    def remove_control_bits(packet):
        counter = 0
        for i in HammingCode.get_list_of_power_of_two(HammingCode.SIZE_OF_INFORMATION_PART - 1):
            amount = HammingCode.check_control_bits(packet, i)
            if amount % 2 == 0 and amount and packet[i - 1] != '0b1':
                HammingCode.mistake_flag = 1
                return -1
        for i in HammingCode.get_list_of_power_of_two(HammingCode.SIZE_OF_INFORMATION_PART - 1):
            del packet[i - 1 - counter:i - counter]
            counter += 1
        return packet

    @staticmethod
    def check_control_bits(packet, counter):
        amount = 0
        temp_counter = Bits(int=counter, length=4)
        pos = temp_counter.find('0b1')
        pos_int = pos[0]
        for i in range(1, 8):
            temp_pos = Bits(int=i, length=4)
            res = BitArray(temp_pos ^ temp_counter)
            if res._readbin(1, pos_int) == '0' and packet._readbin(1, i - 1) == '1':
                amount += 1
        return amount

    @staticmethod
    def get_list_of_power_of_two(power):
        return [1 << i for i in range(power)]
