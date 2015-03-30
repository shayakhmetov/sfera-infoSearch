from __future__ import print_function
__author__ = 'rim'
import codecs, sys


def format_control_code(num):
        return '{0:04b}'.format(num)


def get_length(number=1, to_next=None):
    lengths = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    numbers = list(reversed(lengths))
    if to_next:
        for i, l in enumerate(lengths):
            if l == to_next:
                return lengths[i+1]
    for i, num in enumerate(numbers):
        if num <= number:
            return lengths[i]


def get_number(length):
    if length > 28:
        return 1
    lengths = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    numbers = list(reversed(lengths))
    for i, l in enumerate(lengths):
        if l >= length:
            return numbers[i]


def get_code(length):
    if length > 28:
        return '0000'
    lengths = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    for i, l in enumerate(lengths):
        if l == length:
            return format_control_code(i + 1)


def give_nums(current_nums, max_length, string_code):
    if string_code == '0000':
        byte_string = current_nums[0]
        assert len(byte_string) > 28
        n_bytes = (len(byte_string)-5)/7 + 1
        byte_string = ('{0:0' + str(n_bytes*7+4) + 'b}').format(int(byte_string, base=2))
        byte = string_code + byte_string[:4]
        yield byte

        byte_string = byte_string[4:]
        assert len(byte_string) % 7 == 0
        assert n_bytes == (len(byte_string)-1)/7 + 1
        for i in range(n_bytes):
            if i == n_bytes-1:
                byte = '1'
            else:
                byte = '0'
            byte += byte_string[:7]
            assert len(byte) == 8
            yield byte
            byte_string = byte_string[7:]
        assert byte_string == ''
    else:
        result_bytes = string_code
        if string_code == format_control_code(3) or string_code == format_control_code(7):
            result_bytes += '0'
        elif string_code == format_control_code(5):
            result_bytes += '000'

        for num in current_nums:
            result_bytes += ('{0:0' + str(max_length) + 'b}').format(int(num, base=2))
        assert len(result_bytes) == 32
        for i in range(4):
            assert len(result_bytes[i*8:(i+1)*8]) == 8
            yield result_bytes[i*8:(i+1)*8]


def encode(int_array):
    current_nums, looking_nums = [], []
    number_of_current, cur_max_length, cur_max_n, new_max_length, new_max_n = 0, 0, 0, 0, 0
    looking_nums.append(next(int_array))
    while looking_nums or current_nums:
        finish = False
        byte_string = ''
        assert number_of_current == len(current_nums)
        if not looking_nums:
            try:
                looking_nums.append(next(int_array))
            except StopIteration, e:
                finish = True
        if not finish:
            number = looking_nums.pop(0)
            byte_string = '{0:b}'.format(number)
            if len(byte_string) >= cur_max_length:
                new_max_length = len(byte_string)
            else:
                new_max_length = cur_max_length
            new_max_n = get_number(new_max_length)
            new_max_length = get_length(number=new_max_n)

        if not finish and (number_of_current+1)*new_max_length <= new_max_n*new_max_length:
            number_of_current += 1
            current_nums.append(byte_string)
            cur_max_length, cur_max_n = new_max_length, new_max_n

        elif number_of_current == cur_max_n or number_of_current == 1:
            if number_of_current == 1:
                if len(current_nums[0]) > 28:
                    cur_max_length = len(current_nums[0])
                    string_code = '0000'
                else:
                    cur_max_length = 28
                    string_code = get_code(cur_max_length)
            else:
                cur_max_length = get_length(number=number_of_current)
                string_code = get_code(cur_max_length)
            for num in give_nums(current_nums, cur_max_length, string_code):
                yield int(num, base=2)
            if not finish:
                current_nums = [byte_string]
            else:
                current_nums = []
            cur_max_length, number_of_current = len(byte_string), 1
            cur_max_n = get_number(cur_max_length)

        else:
            cur_max_length = get_length(to_next=cur_max_length)
            cur_max_n = get_number(cur_max_length)
            if cur_max_n > number_of_current:
                cur_max_n = 1
                cur_max_length = get_length(cur_max_n)
            assert cur_max_n <= number_of_current

            if byte_string:
                looking_nums = [int(x, base=2) for x in current_nums[cur_max_n:]] + [int(byte_string, base=2)] + looking_nums
            else:
                looking_nums = [int(x, base=2) for x in current_nums[cur_max_n:]]
            current_nums = current_nums[:cur_max_n]
            string_code = get_code(cur_max_length)
            for num in give_nums(current_nums, cur_max_length, string_code):
                yield int(num, base=2)
            current_nums, cur_max_length, cur_max_n, number_of_current = [], 0, 0, 0


def get_pair_by_code(code):
    lengths = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    for l_code, length in [(format_control_code(i + 1), l) for i, l in enumerate(lengths)]:
        if l_code == code:
            return length, get_number(length)



def decode(bytes):
    current_bytestring = ''
    string_code = None
    n_bytes = 0
    for byte in bytes:
        decoded_byte = '{0:08b}'.format(byte)
        if not string_code:
            string_code = decoded_byte[:4]

        if string_code == '0000':
            if n_bytes == 0:
                current_bytestring += decoded_byte[4:]
                n_bytes += 1
            elif decoded_byte[0] == '1':
                current_bytestring += decoded_byte[1:]
                yield int(current_bytestring, base=2)
                string_code, current_bytestring, n_bytes = None, '', 0
            elif decoded_byte[0] == '0':
                current_bytestring += decoded_byte[1:]
                n_bytes += 1
        else:
            length, number = get_pair_by_code(string_code)
            if n_bytes == 0:
                if string_code == format_control_code(3) or string_code == format_control_code(7):
                    current_bytestring += decoded_byte[5:]
                elif string_code == format_control_code(5):
                    current_bytestring += decoded_byte[-1]
                else:
                    current_bytestring += decoded_byte[4:]
                n_bytes += 1
            elif n_bytes == 3:
                current_bytestring += decoded_byte
                for i in range(number):
                    assert len(current_bytestring[i*length:(i+1)*length]) == length
                    yield int(current_bytestring[i*length:(i+1)*length], base=2)
                string_code, current_bytestring, n_bytes = None, '', 0
            else:
                current_bytestring += decoded_byte
                n_bytes += 1


def read_raw_data(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as file:
        cur_num = 0
        for line in file:
            nums = [int(x) for x in line.rstrip().split()]
            for num in nums:
                if cur_num > num:
                    print('FILE IS NOT SORTED! FAIL')
                    exit(1)
                yield num - cur_num
                cur_num = num


def read_encoded_data(filename):
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte:
            yield ord(byte)
            byte = file.read(1)


def encode_file(write_filename, read_filename):
    with open(write_filename, 'wb') as blob_file:
        for byte in encode(read_raw_data(read_filename)):
            blob_file.write(bytearray([byte]))


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