#coding=utf-8
'''
Created on 02.11.2019

@author: bert
'''
import Gpib, time

def getVersion(ser, addr):
    cmdstring="*IDN?"
    Gpib.setaddr(ser, addr)
    version=Gpib.sendrecvascii(ser, cmdstring)
    return version


def reset(ser, addr):
    cmdstring="*RST"
    Gpib.setaddr(ser, addr)
    version=Gpib.sendrecvascii(ser, cmdstring)
    return version


def clearerrs(ser,addr):
    cmdstring="*CLS"
    Gpib.setaddr(ser, addr)
    version=Gpib.sendascii(ser, cmdstring)
    return version


def setoutput(ser, outp, volt, amps):
    outlist=["P6V", "P25V", "N25V"]
    cmdstring = "APPL {}, {}, {}".format(outlist[outp], volt, amps)
    return Gpib.sendascii(ser, cmdstring)


def enableoutput(ser, status=0):
    statlist= ["OFF", "ON"]
    cmdstring = "OUTP {}".format(statlist[status])
    return Gpib.sendrecvascii(ser, cmdstring)
    
    
def vramp(ser, outp, vstart=0.0, vend=1.0, vstep=0.1, twait=0.0, amps=1.0):
    vnow = vstart
    if vend > vstart: # ansteigende Rampe
        while vnow <= vend:
            setoutput(ser, outp, vnow, amps)
            vnow = round(vnow + vstep, 2)
            time.sleep(twait) 
    elif vend < vstart: 
        while vnow >= vend:
            setoutput(ser, outp, vnow, amps)
            vnow = round(vnow - vstep, 2)
            time.sleep(twait)
    else:
        print ("Fehler: Vstart = Vend!")
        return 1
    return 0
        
