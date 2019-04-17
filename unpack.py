import re
import mmap

def png_files(content):
    p1 = re.compile(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
    starts = []
    for header in p1.finditer(content):
        starts.append(header.start())

    p2 = re.compile(b'\x49\x45\x4E\x44\xAE\x42\x60\x82')
    ends = []
    for end in p2.finditer(content):
        ends.append(end.end())

    files_count = len(starts)

    for x in range(files_count):
        result_file = open('GRAPH/' + str(x) + '.png', 'wb')
        result_file.write(content[starts[x]:ends[x]])

with open('../gamedata', 'r') as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as content:
        png_files(content)