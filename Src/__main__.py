#coding=utf-8


import Gpib, E3631A, time, Shcr


GPIBADDR = 5
PSUDEV = "/dev/ttyUSB1"
PSUBAUD = 460800
HCRDEV = "/dev/ttyUSB0"
HCRBAUD = 115200


serpsu = Gpib.openCom(PSUDEV, PSUBAUD)
print ("GPIB-Adapter:    {}".format(serpsu.name))
print ("GPIB-Adapter FW: {}".format(Gpib.sendrecvascii(serpsu, '++ver')))

Gpib.setauto(serpsu, 1)
print ("PSU GPIB-Adr.:   {}".format(GPIBADDR))
print ("PSU-Ident:       {}\n".format(E3631A.getVersion(serpsu, GPIBADDR)))
Gpib.setauto(serpsu, 0)


E3631A.setoutput(serpsu, 0, 0.0, 1.0)
E3631A.enableoutput(serpsu, 1)

while 1:
    E3631A.clearerrs(serpsu, GPIBADDR)
    E3631A.vramp(serpsu, 0, 0.0, 5.2, 0.2)
    #E3631A.setoutput(serpsu, 0, 5.1, 1.0)
    time.sleep(2)
    serhcr = Shcr.openCom(HCRDEV, HCRBAUD)
    if serhcr:
        resp = Shcr.getsecstatus(serhcr)
        Shcr.clearsecstatus(serhcr)
        Shcr.closecom(serhcr)
        if Shcr.decodestatus(resp):
            break
    time.sleep(1)
    #E3631A.setoutput(serpsu, 0, 4.0, 1.0)
    E3631A.vramp(serpsu, 0, 5.2, 0.0, 0.2)
    time.sleep(2)

E3631A.enableoutput(serpsu, 0)
serpsu.close()
print ("Ende.")
