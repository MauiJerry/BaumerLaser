# Baumer OM-70 test using Trio Sockets
# default ip address is 198.162.0.250
# our rPi is on a dedicated switch on the 198.162.2.x network
# so that needs to be changed
import sys
this = sys.modules[__name__]
import struct
import random
import json
import math
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def keyForDistance ():
    return "DistanceMM"
def keyForTimeStamp():
    return "Timestamp"
def keyForQuality():
    return "Quality"
def keyForAlarmState():
    return "AlarmState"
def keyForSwitchState():
    return "SwitchState"

class OM70Datum():
    """ Baumer OM70 UDP Packet Datum - packing unpacking, test and JSON important bits  """
    # uint32 (4bytes) BlockID
    # uint8 (1byte) FrameType 0= singleFrame 1= first 2 = later frames
    # uint8 reserved
    # uint16 (2b) frame counter; type1: total count type2: current count
    # uint8 Quality 0=ok 1=low 2=nosignal
    # bool 1b State Switching 0= active 1= inactive
    # bool 1b State Alarm 0= active 1=inactive
    # 1b padding
    # float32 (4b) distance in mm
    # float32 measurementrate
    # float32 exposure reserve
    # uint32 response delay seconds
    # uint32 response delay microsec
    # timestamp seconds
    # timestamp microsec
    def __init__(self):
        # format is used by struct in compiled format to (un)pack binary
        # to get it right, slowly add characters and test, as error msgs are not helpful
        # single byte values dont need bytearray
        self.format = '!I B b h b ? ? x fff iiii'
        self.st = struct.Struct(self.format)
        # default data for one record from buffer
        self.blockId = 0
        self.frameId = 0 #bytearray([0])
        self.reservedByte = 0 #bytearray(1)
        self.frameCount = 0
        self.quality = 2
        self.switchingState = 1
        self.alarmState = 1
        #self.padByte = 0# bytearray(1) # we dont need this
        self.distanceMM = 0.0
        self.rate = 0.0
        self.exposureReserve = 0.0
        self.delaySeconds = 0
        self.delayMicroSec = 0
        self.timestampSec =0
        self.timestampMicroSec = 0

    def byteSize(self):
        return struct.calcsize(self.st.format)

    def asJson(self):
        d = {
            keyForDistance(): self.distanceMM,
            keyForAlarmState(): self.alarmState,
            keyForQuality(): self.quality,
            keyForTimeStamp(): self.timestampSec + (self.timestampMicroSec/1000),
            keyForSwitchState(): self.switchingState,
        }
        s = json.dumps(d)
        return s

    def asTuple(self):
        return (
        self.blockId,
        self.frameId,
        self.reservedByte,
        self.frameCount,
        self.quality,
        self.switchingState,
        self.alarmState,
        #self.padByte,
        self.distanceMM,
        self.rate,
        self.exposureReserve,
        self.delaySeconds,
        self.delayMicroSec,
        self.timestampSec,
        self.timestampMicroSec
        )

    def fromTuple(self,tuple):
        (
            self.blockId,
            self.frameId,
            self.reservedByte,
            self.frameCount,
            self.quality,
            self.switchingState,
            self.alarmState,
            #self.padByte,
            self.distanceMM,
            self.rate,
            self.exposureReserve,
            self.delaySeconds,
            self.delayMicroSec,
            self.timestampSec,
            self.timestampMicroSec
        ) = tuple

    def fromBuffer(self, buffer):
        t = self.st.unpack(buffer)
        self.fromTuple(t)

    def toBuffer(self, buffer):
        t = self.asTuple()
        self.st.pack_into(buffer, 0,
            self.blockId,
            self.frameId,
            self.reservedByte,
            self.frameCount,
            self.quality,
            self.switchingState,
            self.alarmState,
            #self.padByte,
            self.distanceMM,
            self.rate,
            self.exposureReserve,
            self.delaySeconds,
            self.delayMicroSec,
            self.timestampSec,
            self.timestampMicroSec
        )

    def setTest1(self):
        self.blockId = 1
        self.frameId = 1
        self.reservedByte = 1#bytearray(1)
        self.frameCount = 1
        self.quality = 0
        self.switchingState = 0
        self.alarmState = 1
        #self.padByte = bytearray(1)
        self.distanceMM = 1.01
        self.rate = 2.0
        self.exposureReserve = 0.0
        self.delaySeconds = 1
        self.delayMicroSec = 5
        self.timestampSec = 10
        self.timestampMicroSec = 2

    def setTestRandom(self):
        self.blockId = random.randrange(0,99)
        self.frameId = random.randrange(0,128)
        self.reservedByte = random.randrange(0,128)
        self.frameCount = random.randrange(0,10)
        self.quality = random.randrange(0,2)
        self.switchingState = 0
        self.alarmState = 1
        self.padByte = bytearray(1)
        self.distanceMM = random.random() * 10.0
        self.rate = 2.0
        self.exposureReserve = 0.0
        self.delaySeconds = 1
        self.delayMicroSec = 5
        self.timestampSec = random.randrange(0,100)
        self.timestampMicroSec = random.randrange(0,1000)

    def equals(self,other):
        if not self.blockId == other.blockId:
            print("blockId not equal")
            return False
        if not self.frameId == other.frameId:
            print("frameId not equal")
            return False
        if not self.reservedByte == other.reservedByte:
            print("reservedByte not equal")
            return False
        if not self.frameCount == other.frameCount:
            print("frameCount not equal")
            return False
        if not self.quality == other.quality:
            print("quality not equal")
            return False
        if not self.switchingState == other.switchingState:
            print("switchingState not equal")
            return False
        if not self.alarmState == other.alarmState:
            print("alarmState not equal")
            return False
        if not self.distanceMM == other.distanceMM:
            if math.isclose(self.distanceMM, other.distanceMM, rel_tol=1e-5):
                print("distance close ",self.distanceMM, other.distanceMM)
            else:
                print("distance not equal")
                return False
        if not self.rate == other.rate:
            if math.isclose(self.rate, other.rate, rel_tol=1e-5):
                print("rate close ", self.rate, other.rate)
            else:
                print("rate not equal")
                return False
        if not self.exposureReserve == other.exposureReserve:
            if not self.exposureReserve == other.exposureReserve:
                if math.isclose(self.exposureReserve, other.exposureReserve, rel_tol=1e-5):
                    print("exposureReserve close ", self.exposureReserve, other.exposureReserve)
                else:
                    print("exposureReserve not close or equal")
                    return False
        if not self.delaySeconds == other.delaySeconds:
            print("delaySeconds not equal")
            return False
        if not self.delayMicroSec == other.delayMicroSec:
            print("delayMicroSec not equal")
            return False
        if not self.timestampSec == other.timestampSec:
            print("timestampSec not equal")
            return False
        if not self.timestampMicroSec == other.timestampMicroSec:
            print("timestampMicroSec not equal")
            return False
        return True
