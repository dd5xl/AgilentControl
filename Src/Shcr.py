#coding=utf-8

'''
Created on 04.11.2019

@author: Bert
'''

import serial, time


def openCom (portname, baud):
    retries = 5
    while retries:
        try:
            ser = serial.Serial(portname, baud, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1)
            ser.rtscts=False
            ser.dsrdtr=False
            return ser
        except:
            retries -= 1
            print ("FEHLER: {} nicht geoeffnet, Neuversuch.".format(portname)) 
            time.sleep(5)
    return 0
            

def closecom (ser):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.close()
    

def shcrsend(ser, scmd):
    sbuf = scmd + b'\x10\x03'
    crc = 0
    for sbyte in sbuf:
        crc = crc ^ sbyte
    sbuf = b'\x10\x02' + sbuf + bytes([crc & 255])
    slen = ser.write(sbuf)
    rbuf = ser.read(1)
    if rbuf == b'\x06':
        #print ("sACK")
        return slen
    else:
        print ("RECV: {}".format(rbuf))
        return 0

     
def shcrrecv(ser):
    rbuf = ser.read(255)
    rcrc = rbuf[-1]
    crc = 0
    for rbyte in rbuf[2:]:
        crc = crc ^ rbyte
    if crc == 0:
        #print ("rACK")
        ser.write(b'\x06')
        ser.flush()
        return rbuf[2:-3]
    else:
        ser.write(b'\x15')
        ser.flush()
        print ("rNAK")
    return 0


def getsecstatus(ser):
    if ser:
        slen = shcrsend(ser, b'\xb4\x00')
        if slen:
            resp= shcrrecv(ser)
            if resp:
                return resp[2:]
            else:
                print ("RXBuf leer.")
        else:
            print ("FEHLER: slen={}".format(slen))
    else:
        print ("FEHLER: kein Handle.")
        return 0
    

def getsecstatusreg(ser):
    if ser:
        slen = shcrsend(ser, b'\xb4\x03')
        if slen:
            resp= shcrrecv(ser)
            if resp:
                return resp[2:]
            else:
                print ("RXBuf leer.")
        else:
            print ("FEHLER: slen={}".format(slen))
    else:
        print ("FEHLER: kein Handle.")
        return 0
    

def clearsecstatus(ser):
    if ser:
        slen = shcrsend(ser, b'\xb4\x01')
        if slen:
            resp= shcrrecv(ser)
            if resp:
                return resp[2:]
            else:
                print ("RXBuf leer.")
        else:
            print ("FEHLER: slen={}".format(slen))
    else:
        print ("FEHLER: kein Handle.")
        return 0
        

def decodestatus(secstatus):
    if secstatus[3]:
        print (time.strftime("%H:%M:%S : ")+ "{0:02X} {1:02X} {2:02X} {3:02X} : TAMPER!".format(secstatus[0], secstatus[1], secstatus[2], secstatus[3]))
        return secstatus 
    else:
        print (time.strftime("%H:%M:%S : ")+ "{0:02X} {1:02X} {2:02X} {3:02X} : OK".format(secstatus[0], secstatus[1], secstatus[2], secstatus[3]))
        return 0
