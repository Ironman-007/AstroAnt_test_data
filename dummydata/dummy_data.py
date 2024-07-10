from cobs import cobs
import numpy as np
import struct
import csv
import random

FRAME_CNT     = 20

ACK_HEADER    = [0xEB, 0x90]
ACK_TYPE      = 0x99

TIME_INTERVAL = 2000 # 2000ms
ACK_TIMESTAMP = 0
ACK_SEQ       = 0x00

ORIGIN_SELF_ACK_HEADER = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

RTD = 0

def int8_to_byte(num):
    # Check if the integer is within the range of a single byte
    if num < 0 or num > 255:
        num = num & 0xFF
        raise ValueError("Integer out of range for a single byte")
    # Convert integer to one byte
    return num.to_bytes(1, byteorder='little', signed=False)

def int16_to_bytes(num):
    # Check if the integer is within the range of two bytes
    if num < 0 or num > 65535:
        num = num & 0xFFFF
        raise ValueError("Integer out of range for two bytes")
    # Convert integer to two bytes
    return num.to_bytes(2, byteorder='little', signed=False)

def int32_to_bytes(num):
    # Check if the integer is within the range of four bytes
    if num < 0 or num > 4294967295:
        num = num & 0xFFFFFFFF
        raise ValueError("Integer out of range for int32")
    return num.to_bytes(4, byteorder='little', signed=False)

def float_to_bytes(num):
    # Convert float to 4 bytes using IEEE 754 format
    return struct.pack('>f', num)

def form_ack_package(dummy_data):
    ack_package = []

    for value, dtype in dummy_data:
        if   dtype == 'int8':
            ack_package.extend(int8_to_byte(value))
        elif dtype == 'int16':
            ack_package.extend(int16_to_bytes(value))
        elif dtype == 'int32':
            ack_package.extend(int32_to_bytes(value))
        elif dtype == 'float':
            ack_package.extend(float_to_bytes(value))

    ack_package = cobs.encode(bytes(ack_package))
    ack_package = ack_package + b'\x00'

    return ack_package

def log_ack_package(ack_package):
    with open('dummy_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([f"{b:02x}" for b in ack_package])

if __name__ == '__main__':
    RTD     = 455
    _5V     = 193
    _3V     = 128
    FRAM    = 0
    CS_ACX  = 0.0
    CS_ACY  = 0.0
    CS_ACZ  = 0.0
    HEAT_EN = 1

    for i in range(FRAME_CNT):
        ACK_TIMESTAMP += TIME_INTERVAL
        ACK_TIMESTAMP = ACK_TIMESTAMP & 0xFFFFFFFF

        ACK_SEQ += 1
        ACK_SEQ = ACK_SEQ  & 0xFF

        RTD    += i%2
        _5V    += i%2
        _3V    += i%2
        FRAM   += 1
        CS_ACX  = 0.0  + random.uniform(-0.1, 0.1)
        CS_ACY  = -3.0 + random.uniform(-0.1, 0.1)
        CS_ACZ  = 9.8  + random.uniform(-0.1, 0.1)

        if (i < FRAME_CNT/2):
            HEAT_EN = 1
        else:
            HEAT_EN = 0

        print(RTD, _5V, _3V, FRAM, CS_ACX, CS_ACY, CS_ACZ, HEAT_EN)

        dummy_data = [
                      (0xEB,    'int8'),
                      (0x90,    'int8'),
                      (ACK_TIMESTAMP, 'int32'),
                      (ACK_SEQ,       'int8'),
                      (ACK_TYPE,      'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (RTD,     'int16'),
                      (_5V,     'int8'),
                      (_3V,     'int8'),
                      (FRAM,    'int8'),
                      (CS_ACX,  'float'),
                      (CS_ACY,  'float'),
                      (CS_ACZ,  'float'),
                      (HEAT_EN, 'int8'),
                      (0,       'int8'),
                      (0,       'int8'),
                      (0xEB,    'int8'),
                      (0x90,    'int8'),
                    ]

        ack_package = form_ack_package(dummy_data)
        log_ack_package(ack_package)









