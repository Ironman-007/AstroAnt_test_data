import csv
import struct

def int8_to_byte(n):
    if not (-128 <= n <= 127):
        raise ValueError("Integer out of range for int8")
    return n.to_bytes(1, byteorder='big', signed=True)

def int16_to_bytes(n):
    if not (-32768 <= n <= 32767):
        raise ValueError("Integer out of range for int16")
    return n.to_bytes(2, byteorder='big', signed=True)

def int32_to_bytes(n):
    if not (-2147483648 <= n <= 2147483647):
        raise ValueError("Integer out of range for int32")
    return n.to_bytes(4, byteorder='big', signed=True)

def float_to_bytes(n):
    return struct.pack('>f', n)

# Generate or provide the data
data = [
    (1, 'int8'), (200, 'int16'), (40000, 'int32'), (3.14, 'float'),
    (-100, 'int8'), (32767, 'int16'), (-2147483648, 'int32'), (2.718, 'float')
]

# Convert each piece of data to bytes and concatenate them
byte_data = []
for value, dtype in data:
    if dtype == 'int8':
        byte_data.extend(int8_to_byte(value))
    elif dtype == 'int16':
        byte_data.extend(int16_to_bytes(value))
    elif dtype == 'int32':
        byte_data.extend(int32_to_bytes(value))
    elif dtype == 'float':
        byte_data.extend(float_to_bytes(value))

# Write the bytes to a CSV file in a single row, each byte in hex format
with open('mixed_byte_data_hex.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Convert each byte to its hex representation and write to CSV
    writer.writerow([f"{b:02x}" for b in byte_data])

print("Data written to mixed_byte_data_hex.csv")
