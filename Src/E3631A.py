#coding=utf-8
'''
Created on 02.11.2019

@author: bert
'''
import Gpib

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

def pwroutput(ser, status=0):
    statlist= ["OFF", "ON"]
    cmdstring = "OUTP {}".format(statlist[status])
    return Gpib.sendrecvascii(ser, cmdstring)
    