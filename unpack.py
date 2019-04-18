import re
import mmap
import os

def log(string):
    print("[UNPACKER] " + string)

def png_files(content):
    log("UNPACKING PNG FILES...")
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
    log("UNPACKING PNG FILES: DONE")

def ogg_files(content):
    log("UNPACKING OGG FILES...")
    p = re.compile(b'\x4F\x67\x67\x53\x00\x02')
    headers = []
    for header in p.finditer(content):
        headers.append(header.start())

    files_count = len(headers)

    for x in range(files_count):
        result_file = open('OGG/' + str(x) + '.ogg', 'wb')
        if x < len(headers)-1:
            result_file.write(content[headers[x]:headers[x+1]-1])
        else:
            result_file.write(content[headers[x]:])
    log("UNPACKING OGG FILES: DONE")

def text(content):
    log("UNPACKING LANG...")
    text_content = content[23435323:]

    result_file = open('dog.txt', 'wb')
    result_file.write(text_content)
    result_file.close()
    log("UNPACKING LANG: DONE")

def file_names(content):
    name_content = content[:34632]
    p = re.compile(b'\x41\x53\x53\x45\x54\x53')
    pos = []
    for x in p.finditer(name_content):
        pos.append(x.start())

    names = []
    for x in range(len(pos)):
        if x < len(pos)-1:
            names.append(name_content[pos[x]:pos[x+1]-12])
        else:
            names.append(name_content[pos[x]:])

    print(names)

def level_files(content):
    log("UNPACKING LEVEL FILES...")

    level_content = content[23131321:23435322]

    level_count = int((23435322-23131321)/1152)+1

    for x in range(level_count):
        result_file = open('LEVELS/' + str(x) + '.poziom', 'wb')
        if x < level_count:
            result_file.write(level_content[x*1152:(x+1)*1152])
        else:
            result_file.write(level_content[x*1152:])

    log("LEVEL FILES: DONE")

def make_directory():
    if not os.path.exists("./GRAPH"):
        os.mkdir("./GRAPH")
    if not os.path.exists("./OGG"):
        os.mkdir("./OGG")
    if not os.path.exists("./LEVELS"):
        os.mkdir("./LEVELS")

with open('../gamedata', 'r') as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as content:
        make_directory()
        log("VERSION 0.1.4")
        log("WORKS ONLY WITH GAMEDATA FROM PB 1.0!!!")
        #file_names(content)
        level_files(content)
        text(content)
        png_files(content)
        ogg_files(content)