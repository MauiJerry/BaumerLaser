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
from collections import namedtuple
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Hmm whats a good way to address items - id in tuple t[n] or getattr(t,name)
def DISTANCEMM():
    return 9
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


# memberNames for namedTuple
_memberNames = ("blockId", "frameId", "reservedByte", "frameCount", "quality",
               "switchingState", "alarmState", "distanceMM", "rate", "exposureReserve",
               "delaySeconds", "delayMicroSec", "timestampSec", "timestampMicroSec")
_memberDefaults = (0, 0, 0, 0, 2, True, True, 0.0, 0.0, 0.0, 0, 0, 0, 0)
# format is used by struct in compiled format to (un)pack binary
# to get it right, slowly add characters and test, as error msgs are not helpful
# single byte values dont need bytearray
_structFormat = '<I B b h b ? ? x fff iiii'
# common struct for all class members to use
_om70struct = struct.Struct(_structFormat)

_OM70DatumT = namedtuple('OM70Datum', [*_memberNames], defaults=[*_memberDefaults])

def byteSize():
    return struct.calcsize(_structFormat)


class OM70Datum(_OM70DatumT):
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

    # def blockId(self):
    #     return getattr(self,"blockId")
    #
    # def frameId(self):
    #     return getattr(self,"frameId")
    #
    # def reservedByte(self):
    #     return getattr(self,"reservedByte")
    #
    # def frameCount(self):
    #     return getattr(self,"frameCount")
    #
    # def quality(self):
    #     return getattr(self,"quality")
    #
    # def switchingState(self):
    #     return getattr(self,"switchingState")
    #
    # def alarmState(self):
    #     return getattr(self,"alarmState")
    #
    # def distanceMM(self):
    #     return getattr(self,"distanceMM")
    #
    # def rate(self):
    #     return getattr(self,"rate")
    #
    # def exposureReserve(self):
    #     return getattr(self,"exposureReserve")
    #
    # def delaySeconds(self):
    #     return getattr(self,"delaySeconds")
    #
    # def delayMicroSec(self):
    #     return getattr(self,"delayMicroSec")
    #
    # def timestampSec(self):
    #     return getattr(self,"timestampSec")
    #
    # def timestampMicroSec(self):
    #     return getattr(self,"timestampMicroSec")

    def asJson(self):
        s = json.dumps(self._asdict())
        return s
    
    def asJsonIndent(self):
        s = json.dumps(self._asdict(), indent=4)
        return s

    def toBuffer(self, buffer):
        _om70struct.pack_into(buffer, 0, *self)

    def equals(self,other):
        if not getattr(self,"blockId") == getattr(other,"blockId"):
            print("blockId not equal ",getattr(self,"blockId"),getattr(other,"blockId"))
            return False
        if not getattr(self,"frameId") == getattr(other,"frameId"):
            print("frameId not equal")
            return False
        if not getattr(self,"reservedByte") == getattr(other,"reservedByte"):
            print("reservedByte not equal")
            return False
        if not getattr(self,"frameCount") == getattr(other,"frameCount"):
            print("frameCount not equal")
            return False
        if not getattr(self,"quality") == getattr(other,"quality"):
            print("quality not equal")
            return False
        if not getattr(self,"switchingState") == getattr(other,"switchingState"):
            print("switchingState not equal")
            return False
        if not getattr(self,"alarmState") == getattr(other,"alarmState"):
            print("alarmState not equal")
            return False
        if not getattr(self,"distanceMM") == getattr(other,"distanceMM"):
            if math.isclose(getattr(self,"distanceMM"), getattr(other,"distanceMM"), rel_tol=1e-5):
                print("distance close ",getattr(self,"distanceMM"), getattr(other,"distanceMM"))
            else:
                print("distance not equal")
                return False
        if not getattr(self,"rate") == getattr(other,"rate"):
            if math.isclose(getattr(self,"rate"), getattr(other,"rate"), rel_tol=1e-5):
                print("rate close ", getattr(self,"rate"), getattr(other,"rate"))
            else:
                print("rate not equal")
                return False
        if not getattr(self,"exposureReserve") == getattr(other,"exposureReserve"):
            if math.isclose(getattr(self,"exposureReserve"), getattr(other,"exposureReserve"), rel_tol=1e-5):
                print("exposureReserve close ", getattr(self,"exposureReserve"), getattr(other,"exposureReserve"))
            else:
                print("exposureReserve not close or equal")
                return False
        if not getattr(self,"delaySeconds") == getattr(other,"delaySeconds"):
            print("delaySeconds not equal")
            return False
        if not getattr(self,"delayMicroSec") == getattr(other,"delayMicroSec"):
            print("delayMicroSec not equal")
            return False
        if not getattr(self,"timestampSec") == getattr(other,"timestampSec"):
            print("timestampSec not equal")
            return False
        if not getattr(self,"timestampMicroSec") == getattr(other,"timestampMicroSec"):
            print("timestampMicroSec not equal")
            return False
        return True

def fromBuffer(buffer):
    t = _om70struct.unpack(buffer)
    print("fromBuffer tuple: ", t)
    return OM70Datum._make(t)

def makeRandomOm70():
    t = (random.randrange(0,99), random.randrange(0,128), random.randrange(0,128),
         random.randrange(0,10), random.randrange(0,2), 0, 1, random.random() * 10.0,
         2.0, 0.0, 1, 5, random.randrange(0,100), random.randrange(0,1000))
    return OM70Datum._make(t)

if __name__ == "__main__":
    print("test OM70Datum PackUnpack  begin")
    b1 = OM70Datum()
    b2 = OM70Datum()
    print("b1:",b1)
    print("b2:",b2)
    if b1.equals(b2):
        print("B1=B2 defaults are equal")
    else:
        print("B1 not = B2 defaults not equal")
    b2 = makeRandomOm70()
    b1= makeRandomOm70()
    print("b1 Test:",b1)
    print("b2 Random:",b2)
    if b1.equals(b2):
        print("B1=B2 randoms are but should not be equal" )
    else:
        print("B1 not = B2 randoms not equal")
    print("b1 json:", b1.asJson())
    print("b2 json:", b2.asJson())
    buffer = bytearray(byteSize())
    print("Now try converting to/from buffer")
    b1.toBuffer(buffer)
    print("buffer:", buffer)
    b2 = fromBuffer(buffer)
    print("b1 to   buffer", b1)
    print("b2 from Buffer", b2)
    if b1.equals(b2):
        print("B1=B2 Conversion to/from buffer works")
    else:
        print("B1 not = B2 Conversion to/from buffer Fails")
    print("b2 from buffer as json", b2.asJsonIndent())
    print("testDatumPackUnpack  end")
