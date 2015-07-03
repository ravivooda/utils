#!/usr/bin/env python

import socket
import sys
import re
import struct
import numpy
import pyaudio
import collections
import wave
import matplotlib.pyplot as plt

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
    ret = ret ^ fourth
    ret = ret ^ (third << 8)
    ret = ret ^ (second << 16)
    ret = ret ^ (first << 24)
    return ret

def parsePacket(dump):
    orig_bytes = map(ord, dump)
    print orig_bytes
    seq =  int_from_bytes(orig_bytes[:4])
    chk = int_from_bytes(orig_bytes[4:8])
    length = int_from_bytes(orig_bytes[8:12])
    print "Sequence number: " + str(seq) + "s"
    print "Checksum: " + str(chk)
    print "Length: " + str(length)

    bytes = map(str, orig_bytes)
    d_len = min(length, len(orig_bytes) - 12)
    data = b"".join(bytes[12:d_len+12])

    print "ACTUAL LENGTH OF BYTES RECEIVED: " + str(len(orig_bytes)) + " COMPUTED LENGTH: " + str(length)
    
    valid = False
    if not abs(len(orig_bytes) - length) <= 16 and False:
        print "Looks like a clear mismatch"
    else :
        valid = True
        com_chk = 0
        i = 0;
        len_bytes = len(orig_bytes) - 12
        if len_bytes % 4 != 0:
            len_bytes += 4 - (len_bytes % 4)
        #print "LENGTH FOR CHECKSUM: " + str(len_bytes)
        while i < len_bytes:
            reg_data = int_from_bytes(orig_bytes[i+12:i+16])
            com_chk = com_chk ^ reg_data
            #print "Index: "+str(i)+" Computed for reg_data: " +str(reg_data) +", " + str(com_chk) + ", " + str(com_chk ^ seq)  + "\tfor bytes: "+str(orig_bytes[i+12:i+16])
            i += 4
        com_chk = com_chk ^ seq
        print "COMPUTED CHECKSUM: " + str(com_chk)
        if com_chk == chk:
            print "CHECKSUM MATCH"
            return True, seq, orig_bytes[12:]
    print "==========================================================================================================================================================================================="
    return False, seq, []
    #return (seq, chk, len(orig_bytes), data)

seq_counts = collections.defaultdict(int)
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
            dump_arr.extend(dump)
        else:
            check = False

    curr_pointer = 0
    success = 0
    fail = 0
    max_seq_success = 0
    max_success = 0
    return_data = []
    while curr_pointer < len(dump_arr):
        #seqcnt = int_from_bytes(dump_arr[curr_pointer:curr_pointer+4])
        #chksum = int_from_bytes(dump_arr[curr_pointer+4:curr_pointer+8])
        len_arr = map(ord, dump_arr[curr_pointer+8:curr_pointer+12])
        length = int_from_bytes(len_arr)
        #data = dump_arr[curr_pointer+12:curr_pointer+12+length]
        curr_packet = dump_arr[curr_pointer:curr_pointer+length+12]
        isValid, seq, data = parsePacket(curr_packet)
        seq_counts[seq] += 1
        if isValid:
            success += 1
            max_seq_success = max(max_seq_success,seq)
            return_data.append((seq,data))
        else:
            fail += 1
        max_success = max(max_success,seq)
        curr_pointer += length + 12
    print "Success: " + str(success) + " Fail: " + str(fail)
    print "Max success sequence: " + str(max_seq_success) + " Max success: " + str(max_success)
    return return_data
    '''j = 0
    valid = 0;
    while j < i:
        dumped = parsePacket(dump_arr[j])
        j += 1
        #if dumped[2] % 1448 == 0:
        #    print "Leaving : " + str(dumped[0])
        #    continue
        #print "Adding : " + str(dumped[0])
        seq_arr.append(dumped)
        if valid < 2:
            #seq_arr.append(dumped)
            valid += 1
            print "\n\n\n\n\n\n\n"
        else:
            return seq_arr, valid
    #print seq_arr
    seq_arr = sorted(seq_arr, key=lambda packet:packet[0]) #sort by seq number
    return seq_arr, valid'''
                
if __name__ == "__main__":
    data = understand()
    sorted_data = sorted(data,key=lambda x:x[0])
    print "SORTED DATA"
    print str([(tupp[0],seq_counts[tupp[0]]) for tupp in sorted_data]) + str(sum(seq_counts.values()))
    data_merged = []
    for tupp in sorted_data:
        if tupp[1] > 128:
            data_merged.extend(tupp[1])
    #print "DATA MERGED: "
    morse_string = ""
    for i in data_merged:
        if i < 128:
            morse_string += "."
        else:
            morse_string += "_"
    #print "\n\n\n\n\n\n"
    #print morse_string
    print "\n\n\n\n\n\n"
    #print data_merged
    print "TOTAL BYTES OF AUDIO: " + str(len(data_merged))

    CHUNK = 1024
    FORMAT = pyaudio.paUInt8
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "alien.wav"
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    data_chars = [chr(item) for item in data_merged]
    print int_from_bytes(data_merged[8:12])

    print("* recording")
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data_chars))
    wf.close()
    '''
    plt.plot(data_merged)
    plt.show()
    
    data_chars = [chr(item) for item in data_merged] #if 65 <= item <= 90 or 97 <= item <= 122]
    print data_chars[:100]
    p = pyaudio.PyAudio()                                                                            
    stream = p.open(format=pyaudio.paUInt8, channels=2, rate=44100, output=True, input=True)                                                                                                                           
    stream.write(str(data_merged))
    stream.close()                                                                                                                                                                 
    p.terminate()
    '''
    '''seq_arr1, valid_items = understand()
    #seq_arr2 = understand()
    print "SEQ 1"
    #print seq_arr1
    print "Number of valid: " + str(valid_items)
    seq_arr = [tupp[0] for tupp in seq_arr1]
    print seq_arr
    p = pyaudio.PyAudio()
    aud_data = [tupp[3] for tupp in seq_arr1]
    #for tupp in seq_arr1:
    #    aud_data.extend(tupp[3])
    #    #print len(tupp[3])
    #stream = p.open(format=pyaudio.paInt8, channels=1, rate=44100, output=True)
    #stream.write(str(aud_data))
    #stream.close()
    #p.terminate()
    print "==========================================================================================================================================================================================="
    #print "SEQ 2"
    #print seq_arr2
    #print "==========================================================================================================================================================================================="
    #print list(set(seq_arr1).intersection(seq_arr2))'''
    
