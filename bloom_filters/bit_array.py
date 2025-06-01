from typing import List

class BitArray:
    def __init__(self, bits: List[int]):
        self.buffer = self.bits_to_bytearray(bits)

    def bits_to_bytearray(self, bits: List[int]) -> bytearray:
        bytearr = bytearray()
        byte = 0
        counter = 0

        for bit in bits:
            byte = (byte << 1) | bit
            counter += 1
            if counter == 8:
                bytearr.append(byte)
                byte = 0
                counter = 0

        if counter > 0:
            byte = byte << (8 - counter)
            bytearr.append(byte)
        
        return bytearr
        
    def __getitem__(self, index):
        byte_index = index // 8

        bit_pos = index % 8

        byte = self.buffer[byte_index]

        shifting_amount = 7 - bit_pos

        ans = byte >> shifting_amount

        return ans & 1


# Example usage:
bits = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]  # 10 bits
ba = BitArray(bits)

print(ba[9])