#!/usr/bin/env python

import socket
import sys
import re
import struct
import numpy
import pyaudio

def int_from_bytes(bytes):
    if len(bytes) != 4:
        print "WRONG, WRONG"
        return 0
    ret = 0
    ret = ret ^ bytes[3]
    ret = ret ^ (bytes[2] << 8)
    ret = ret ^ (bytes[1] << 16)
    ret = ret ^ (bytes[0] << 24)
    return ret

def parsePacket(dump):
    orig_bytes = map(ord, dump)
    #print orig_bytes
    seq =  int_from_bytes(orig_bytes[:4])
    chk = int_from_bytes(orig_bytes[4:8])
    len = int_from_bytes(orig_bytes[8:12])
    print "Sequence number: " + str(seq)
    #print "Checksum: " + str(chk)
    print "Length: " + str(len)
    fr_diff = 0#len % 4 == 0 ? 0 : 4 - (len%4)
    if fr_diff != 0:
        fr_diff = 4 - fr_diff
    len_bytes = len
    while fr_diff > 0:
        print "Found 4 diff: " + str(fr_diff)
        orig_bytes.append(171)
        fr_diff -= 1
        len_bytes += 1
    bytes = map(str, orig_bytes)
    data = b"".join(bytes[12:])
    #print "DATA:"                                                                                                                                                                                          
    print "====================================================================================================================================================================================="          
    #print data                                                                                                                                                                                             
    #print "====================================================================================================================================================================================="          

    '''com_chk = 0
    i = 0;
    data_str = b""
    while i < len_bytes:
        data_str += str(chr(orig_bytes[i]))
        data_str += chr(orig_bytes[i+1])
        data_str += chr(orig_bytes[i+2])
        data_str += chr(orig_bytes[i+3])
        reg_data = int_from_bytes(orig_bytes[i:i+4])
        com_chk = com_chk ^ reg_data
        i += 4
    com_chk = com_chk ^ seq
    print "COMPUTED CHECKSUM: " + str(com_chk)'''

def understand():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    answer = s.recv(1024).rstrip()
    print answer
    rep = answer[6:]
    f_resp = "IAM:" + rep + ":r.vooda@gmail.com:at\n"
    print f_resp
    s.send(f_resp)
    new_ans = s.recv(10240)
    print new_ans
    #p = pyaudio.PyAudio()
    #stream = p.open(format=FORMAT, channels=1, rate=RATE,input=True, output=True,frames_per_buffer=CHUNK_SIZE)

    while True:
        dump = s.recv(100000)
        if dump.strip(' '):
            parsePacket(dump)
        else:
            print "No data"
            return
                
if __name__ == "__main__":
    understand()
    
