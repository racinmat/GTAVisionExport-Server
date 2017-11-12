import io
from PIL import Image

if __name__ == '__main__':
    data = b'\x00\x00\x00\x00\x00\x0f\xc6\xc4'
    print(data)
    print(int.from_bytes(data, byteorder='big'))
    print(int.from_bytes(data, byteorder='little'))
    # with open('last_screen.bin', 'rb') as file:
    #     data = file.read()
    #     # b_data = binascii.unhexlify(data)
    #     stream = io.BytesIO(data)
    #     img = Image.open(stream)
