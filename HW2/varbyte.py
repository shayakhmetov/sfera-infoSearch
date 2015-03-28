__author__ = 'rim'
import codecs


def encode(int_array):
    for number in int_array:
        n_bytes = 1
        while number >= 2**(n_bytes*7):
            n_bytes += 1
        byte_string = ('{0:0' + str(n_bytes*7) + 'b}').format(number)
        index = 0
        for i in range(n_bytes):
            if i == n_bytes - 1:
                byte = '1'
            else:
                byte = '0'
            byte += byte_string[index:index+7]
            index += 7
            yield chr(int(byte, base=2))


def decode(bytes):
    current_bytestring = ''
    for byte in bytes:
        decoded_byte = '{0:08b}'.format(ord(byte))
        if decoded_byte[0] == '1':
            current_bytestring += decoded_byte[1:]
            yield int(current_bytestring, base=2)
            current_bytestring = ''
        elif decoded_byte[0] == '0':
            current_bytestring += decoded_byte[1:]


def read_raw_data(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        cur_num = 0
        for line in file:
            nums = [int(x) for x in line.rstrip().split()]
            for num in nums:
                yield num - cur_num
                cur_num = num


def read_encoded_data(filename):
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte:
            yield byte
            byte = file.read(1)


def encode_file(write_filename, read_filename):
    with open(write_filename, 'wb') as blob_file:
        for byte in encode(read_raw_data(read_filename)):
            blob_file.write(bytearray([ord(byte)]))


def decode_file(read_filename, write_filename):
    with codecs.open(write_filename, 'w', encoding='utf-8') as file:
        current_num = 0
        for num in decode(read_encoded_data(read_filename)):
            file.write(str(num + current_num) + '\n')
            current_num += num


def main():
    encode_file(write_filename='blob', read_filename='nums')
    decode_file(read_filename='blob', write_filename='result')




if __name__ == '__main__':
    main()