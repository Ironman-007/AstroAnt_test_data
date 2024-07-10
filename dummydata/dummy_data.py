from cobs import cobs
import numpy as np
import struct
import csv
import random

FRAME_CNT     = 200

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
    ACK_TYPE      = 0x99

    TIME_INTERVAL = 2000 # 2000ms
    ACK_TIMESTAMP = 0
    ACK_SEQ       = 0x00

    # CS Data
    RTD     = 455
    _5V     = 193
    _3V     = 128
    FRAM    = 0
    CS_ACX  = 0.0
    CS_ACY  = 0.0
    CS_ACZ  = 0.0
    HEAT_EN = 1

    # Ant Data
    ANT_TIMESTAMP = 1000
    ANT_seq       = 0

    COM_time_stamp = 2333

    COM_seq        = 3
    COM_DT         = 0x01
    COM_CRC        = 0xEF

    ANT_APT        = 24
    ANT_ARTD       = 25
    ANT_BATV       = 160
    ANT_AFRAM      = 100
    ANT_gyrox      = 1.0
    ANT_gyroy      = 2.0
    ANT_gyroz      = 3.0
    ANT_acx        = 4.0
    ANT_acy        = 5.0
    ANT_acz        = 6.0
    ANT_DIR        = 0.0
    ANT_CORX       = 10
    ANT_CORY       = 10
    ANT_HEATERON   = 0
    ANT_CRC8       = 0x01
    ANT_CRC8_2     = 0x02

    for i in range(FRAME_CNT):
        # Header
        ACK_TIMESTAMP += TIME_INTERVAL
        ACK_TIMESTAMP = ACK_TIMESTAMP & 0xFFFFFFFF

        ACK_SEQ += 1
        ACK_SEQ = ACK_SEQ  & 0xFF

        # CS Data
        RTD    += i%2
        RTD    = RTD & 0xFFFF

        _5V    += i%2
        _5V    = _5V & 0xFF

        _3V    += i%2
        _3V    = _3V & 0xFF

        FRAM   += 1
        FRAM   = FRAM & 0xFF

        CS_ACX  = 0.0  + random.uniform(-0.1, 0.1)
        CS_ACY  = -3.0 + random.uniform(-0.1, 0.1)
        CS_ACZ  = 9.8  + random.uniform(-0.1, 0.1)

        if (i < FRAME_CNT/2):
            HEAT_EN = 1
        else:
            HEAT_EN = 0

        # Ant Data
        ANT_TIMESTAMP += TIME_INTERVAL
        ANT_TIMESTAMP = ANT_TIMESTAMP & 0xFFFFFFFF

        ANT_seq += 1
        ANT_seq = ANT_seq  & 0xFF

        COM_time_stamp = 2333

        COM_seq += 1
        COM_seq = COM_seq & 0xFF

        ANT_APT        += i%3
        ANT_APT        = ANT_APT & 0xFFFF

        ANT_ARTD       += i%3
        ANT_ARTD       = ANT_ARTD & 0xFFFF

        ANT_BATV       += i%3
        ANT_BATV       = ANT_BATV & 0xFF

        ANT_AFRAM      += 1
        ANT_AFRAM      = ANT_AFRAM & 0xFFFF

        ANT_gyrox      = 1.0 + random.uniform(-0.1, 0.1)
        ANT_gyroy      = 2.0 + random.uniform(-0.1, 0.1)
        ANT_gyroz      = 3.0 + random.uniform(-0.1, 0.1)
        ANT_acx        = 4.0 + random.uniform(-0.1, 0.1)
        ANT_acy        = 5.0 + random.uniform(-0.1, 0.1)
        ANT_acz        = 6.0 + random.uniform(-0.1, 0.1)
        ANT_DIR        = 0.0 + random.uniform(-0.1, 0.1)

        ANT_CORX       += 1
        ANT_CORX       = ANT_CORX & 0xFFFF

        ANT_CORY       += 2
        ANT_CORY       = ANT_CORY & 0xFFFF

        if (i < FRAME_CNT/2):
            ANT_HEATERON = 0
        else:
            ANT_HEATERON = 1

        print(
                0xEB, ',',
                0x90, ',',
                ACK_TIMESTAMP, ',',
                ACK_SEQ, ',',
                ACK_TYPE, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                RTD, ',',
                _5V, ',',
                _3V, ',',
                FRAM, ',',
                CS_ACX, ',',
                CS_ACY, ',',
                CS_ACZ, ',',
                HEAT_EN, ',',
                0, ',',
                0, ',',
                0xEB, ',',
                0x90, ',',
                ANT_TIMESTAMP, ',',
                ANT_seq, ',',
                0x81, ',',
                0xEB, ',',
                0x92, ',',
                COM_time_stamp, ',',
                COM_seq, ',',
                COM_DT, ',',
                COM_CRC, ',',
                ANT_APT, ',',
                ANT_ARTD, ',',
                ANT_BATV, ',',
                ANT_AFRAM, ',',
                ANT_gyrox, ',',
                ANT_gyroy, ',',
                ANT_gyroz, ',',
                ANT_acx, ',',
                ANT_acy, ',',
                ANT_acz, ',',
                ANT_DIR, ',',
                ANT_CORX, ',',
                ANT_CORY, ',',
                ANT_HEATERON, ',',
                0, ',',
                0, ',',
                0, ',',
                0, ',',
                ANT_CRC8, ',',
                ANT_CRC8_2
            )

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
                        (ANT_TIMESTAMP,  'int32'),
                        (ANT_seq,        'int8'),
                        (0x81,           'int8'),
                        (0xEB,           'int8'),
                        (0x92,           'int8'),
                        (COM_time_stamp, 'int32'),
                        (COM_seq,        'int8'),
                        (COM_DT,         'int8'),
                        (COM_CRC,        'int8'),
                        (ANT_APT,        'int16'),
                        (ANT_ARTD,       'int16'),
                        (ANT_BATV,       'int8'),
                        (ANT_AFRAM,      'int16'),
                        (ANT_gyrox,      'float'),
                        (ANT_gyroy,      'float'),
                        (ANT_gyroz,      'float'),
                        (ANT_acx,        'float'),
                        (ANT_acy,        'float'),
                        (ANT_acz,        'float'),
                        (ANT_DIR,        'float'),
                        (ANT_CORX,       'int16'),
                        (ANT_CORY,       'int16'),
                        (ANT_HEATERON,   'int8'),
                        (0,              'int8'),
                        (0,              'int8'),
                        (0,              'int8'),
                        (0,              'int8'),
                        (ANT_CRC8,       'int8'),
                        (ANT_CRC8_2,     'int8')
                    ]

        ack_package = form_ack_package(dummy_data)
        log_ack_package(ack_package)









