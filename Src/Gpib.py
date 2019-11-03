#coding=utf-8

import serial, time


def openCom (portname):
    ser = serial.Serial(portname, 460800, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0.1)
    #ser.timeout(2)
    return ser


def sendrecvascii(ser, cmdstring):
    if cmdstring[:-1] == "\n":
        bytestring = cmdstring.encode()
    else:
        bytestring = (cmdstring + "\n").encode()
    ser.write (bytestring)
    resp = ser.readline().decode()
    return resp

def sendascii(ser, cmdstring):
    if cmdstring[:-1] == "\n":
        bytestring = cmdstring.encode()
    else:
        bytestring = (cmdstring + "\n").encode()
    resp = ser.write (bytestring)
    time.sleep(0.1)
    return resp


def setaddr (ser, gpibaddr):
    print ("GPIB-Device: {}".format(gpibaddr))
    cmdstring = "++addr {}".format(gpibaddr)
    return sendascii(ser, cmdstring)


def setauto (ser, automode=1):
    if automode:
        st = "ein"
    else:
        st = "aus"
    print ("AutoRead: {}".format(st))
    cmdstring = "++auto {}".format(automode)
    return sendascii(ser, cmdstring)
    
    