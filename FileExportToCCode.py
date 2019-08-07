#!/usr/bin/env python3
# Convert binary file to hexadecimal text file
import argparse, os, binascii, struct, re

bytes_per_line = 16

parser = argparse.ArgumentParser(description = 'Convert binary file to hexadecimal text file')
parser.add_argument('filename', help = 'The binary file as input')
args = parser.parse_args()

size = os.path.getsize(args.filename)
loc_width = len(hex(size)[2:])
loc_width = loc_width + ((8 - (loc_width % 8)) if loc_width % 8 != 0 else 0) # Make it multiple of 8

a = 0

with open(args.filename, 'rb') as fin:
    fileNamePrefix = re.findall(r'(.+?)\.',args.filename)
    with open(fileNamePrefix[0] + '.cpp', 'wb') as fout:
        while True:
            line = []
            characters = []
            for i in range(bytes_per_line):
                data = fin.read(1)
                if data != b'':
                    line.append(binascii.hexlify(data).upper())
                    a = a + 1
                    if a == 1:
                        fout.write(b'unsigned char ' + str.encode(fileNamePrefix[0]) + b'[' + str.encode(str(size)) + b'] = {\n')
                else:
                    break
            if len(line) > 0:
                fout.write(b'    0x')
                fout.write(b', 0x'.join(line))
                #The last line of bytes is partially filled with blank space
                #if len(line) < bytes_per_line:
                #   fout.write(b'      ' * (bytes_per_line - len(line)))
                if a != size:
                    fout.write(b',\n')
                else:
                    fout.write(b' \n};\n')
            else:
                break
            print('\r{0:.1f}%'.format(fin.tell() / size * 100), end = '', flush = True)
