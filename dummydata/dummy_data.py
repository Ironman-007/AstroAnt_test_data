from cobs import cobs
import numpy as np
import struct
import csv

FRAME_CNT     = 20

ACK_HEADER    = [0xEB, 0x90]
ACK_TYPE      = 0x99

TIME_INTERVAL = 2000 # 2000ms
ACK_TIMESTAMP = 0
ACK_SEQ       = 0x00

ORIGIN_SELF_ACK_HEADER = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

def int8_to_byte(num):
    # Check if the integer is within the range of a single byte
    if num < 0 or num > 255:
        raise ValueError("Integer out of range for a single byte")
    # Convert integer to one byte
    return num.to_bytes(1, byteorder='little', signed=False)

def int16_to_bytes(num):
    # Check if the integer is within the range of two bytes
    if num < 0 or num > 65535:
        raise ValueError("Integer out of range for two bytes")
    # Convert integer to two bytes
    return num.to_bytes(2, byteorder='little', signed=False)

def int32_to_bytes(num):
    # Check if the integer is within the range of four bytes
    if num < 0 or num > 4294967295:
        raise ValueError("Integer out of range for int32")
    return num.to_bytes(4, byteorder='little', signed=False)

def float_to_bytes(num):
    # Convert float to 4 bytes using IEEE 754 format
    return struct.pack('>f', num)

def form_ack_package():
    global ACK_TIMESTAMP
    global ACK_SEQ

    ack_package = []

    ack_package.extend([int8_to_byte(i)[0] for i in ACK_HEADER])

    ACK_TIMESTAMP += TIME_INTERVAL
    ACK_TIMESTAMP = ACK_TIMESTAMP & 0xFFFFFFFF
    ack_package.extend(int32_to_bytes(ACK_TIMESTAMP))

    ACK_SEQ += 1
    ACK_SEQ = ACK_SEQ  & 0xFF
    ack_package.extend(int8_to_byte(ACK_SEQ))

    ack_package.extend(int8_to_byte(ACK_TYPE))

    ack_package.extend([int8_to_byte(i)[0] for i in ORIGIN_SELF_ACK_HEADER])

    return ack_package

def log_ack_package(ack_package):
    with open('dummy_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([f"{b:02x}" for b in ack_package])

if __name__ == '__main__':
    for i in range(FRAME_CNT):
        ack_package = form_ack_package()
        log_ack_package(ack_package)
