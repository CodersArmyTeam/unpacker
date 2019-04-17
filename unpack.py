import re
import mmap

def png_files(content):
    p1 = re.compile(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
    starts = []
    for start in p1.finditer(content):
        starts.append(start.start())

    p2 = re.compile(b'\x49\x45\x4E\x44\xAE\x42\x60\x82')
    ends = []
    for end in p2.finditer(content):
        ends.append(end.end())

    files_count = len(starts)

    for x in range(files_count):
        result_file = open('GRAPH/' + str(x) + '.png', 'wb')
        result_file.write(content[starts[x]:ends[x]])

def ogg_files(content):
    p = re.compile(b'\x4F\x67\x67\x53\x00\x02')
    headers = []
    for header in p.finditer(content):
        headers.append(header.start())

    files_count = len(headers)
    print(files_count)

    for x in range(files_count):
        result_file = open('OGG/' + str(x) + '.ogg', 'wb')
        if x < len(headers)-1:
            result_file.write(content[headers[x]:headers[x+1]-1])
        else:
            result_file.write(content[headers[x]:])

def text(content):
    text_content = content[23435323:]

    result_file = open('dog.txt', 'wb')
    result_file.write(text_content)
    result_file.close()

with open('../gamedata', 'r') as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as content:
        text(content)
        png_files(content)
        ogg_files(content)