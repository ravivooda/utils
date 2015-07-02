#!/usr/bin/env python

import socket
import sys
import re
import struct
import numpy
import pyaudio

def int_from_bytes(bytes):
    ret = 0
    first = 171
    second = 171
    third = 171
    fourth = 171
    if len(bytes) > 0:
        first = bytes[0]
    if len(bytes) > 1:
        second = bytes[1]
    if len(bytes) > 2:
        third = bytes[2]
    if len(bytes) > 3:
        fourth = bytes[3]
    #print "Computing for " + str(bytes)
    ret = ret ^ fourth
    ret = ret ^ (third << 8)
    ret = ret ^ (second << 16)
    ret = ret ^ (first << 24)
    return ret

def parsePacket(dump):
    orig_bytes = map(ord, dump)
    #print orig_bytes
    seq =  int_from_bytes(orig_bytes[:4])
    chk = int_from_bytes(orig_bytes[4:8])
    length = int_from_bytes(orig_bytes[8:12])
    print "Sequence number: " + str(seq)
    print "Checksum: " + str(chk)
    print "Length: " + str(length)

    bytes = map(str, orig_bytes)
    data = b"".join(bytes[12:])

    print len(orig_bytes)
    
    valid = False
    if not abs(len(orig_bytes) - length) <= 16:
        print "Looks like a clear mismatch"
    else :
        valid = True
        com_chk = 0
        i = 0;
        len_bytes = length
        if len_bytes % 4 != 0:
            len_bytes += 4 - (len_bytes % 4)
        while i < len_bytes:
            reg_data = int_from_bytes(orig_bytes[i+12:i+16])
            com_chk = com_chk ^ reg_data
            i += 4
        com_chk = com_chk ^ seq
        print "COMPUTED CHECKSUM: " + str(com_chk)
    print "==========================================================================================================================================================================================="
    return data, valid

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
    
    check = True
    seq_arr = []
    dump_arr = []
    i = 0
    while check:
        dump = (s.recv(100000))
        if dump.strip(' '):
            i += 1
            check = True
            dump_arr.append(dump)
        else:
            check = False
    j = 0
    valid = 0;
    while j < i:
        dumped, isValid = parsePacket(dump_arr[j])
        seq_arr.append(dumped)
        if isValid:
            #seq_arr.append(dumped)
            valid += 1
            #return seq_arr, valid
        j += 1
    #print seq_arr
    return seq_arr, valid
                
if __name__ == "__main__":
    seq_arr1, valid_items = understand()
    #seq_arr2 = understand()
    print "SEQ 1"
    #print seq_arr1
    print "Number of valid: " + str(valid_items)
    #p = pyaudio.PyAudio()
    #stream = p.open(format=pyaudio.paInt8, channels=1, rate=44100, output=1)
    #stream.write(str(seq_arr1))
    #stream.close()
    #p.terminate()
    print "==========================================================================================================================================================================================="
    #print "SEQ 2"
    #print seq_arr2
    #print "==========================================================================================================================================================================================="
    #print list(set(seq_arr1).intersection(seq_arr2))
    
