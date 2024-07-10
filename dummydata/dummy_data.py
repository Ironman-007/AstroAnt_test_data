from cobs import cobs
import numpy as np

ACK_HEADER = [0xEB, 0x90]

TIME_INTERVAL = 2000 # 2000ms
ACK_TIMESTAMP = 0
ACK_SEQ       = 0

FRAME_CNT = 100

CS_PACKAGE  = []
ANT_PACKAGE = []

def form_ack_package():
    global ACK_TIMESTAMP
    global ACK_SEQ

    ACK_TIMESTAMP += TIME_INTERVAL
    ACK_SEQ += 1

    ack_package = ACK_HEADER + [ACK_TIMESTAMP & 0xFF, (ACK_TIMESTAMP >> 8) & 0xFF, (ACK_TIMESTAMP >> 16) & 0xFF, (ACK_TIMESTAMP >> 24) & 0xFF]
    ack_package += [ACK_SEQ & 0xFF, (ACK_SEQ >> 8) & 0xFF]

    return ack_package

def log_ack_package():
    ack_package = form_ack_package()
    CS_PACKAGE.append(ack_package)
    ANT_PACKAGE.append(ack_package)

if __name__ == '__main__':
    pass
