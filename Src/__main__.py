#coding=utf-8


import Gpib, E3631A, time


ADDR = 5

ser = Gpib.openCom("/dev/ttyUSB0")
print ("USB-Device:      {}".format(ser.name))
print ("GPIB-Adapter FW: {}\n".format(Gpib.sendrecvascii(ser, '++ver')))
Gpib.setauto(ser, 1)
print (E3631A.getVersion(ser, ADDR))
Gpib.setauto(ser, 0)
while 1:
    E3631A.clearerrs(ser, ADDR)
    volt = 0
    E3631A.pwroutput(ser, 1)
    while volt < 5.1:
        E3631A.setoutput(ser, 0, volt, 1)
        volt += 0.1
    time.sleep(5)
    E3631A.setoutput(ser, 0, 0, 1)
E3631A.pwroutput(ser, 0)
ser.close
print ("Ende.")
