import os
import random

if 'CI' not in os.environ:
    import hid

from . import comm_pb2 as comm
from . import delimited

ZMKX_VID = 0x1d50
ZMKX_PID = 0x615e
ZMKX_USAGE = 0xff14

REPORT_COUNT = 63
PAYLOAD_SIZE = REPORT_COUNT - 1


def find_devices(serial=None, features=[]):
    devices = [
        Device(h['path'], h['usage'])
        for h in hid.enumerate(ZMKX_VID, ZMKX_PID)
        if h['usage_page'] == ZMKX_USAGE
    ]

    def _filter(device):
        with device.open() as dev:
            if serial is not None:
                if dev.serial != serial:
                    return False

            if len(features) > 0:
                if not all(getattr(dev.version().features, f, False) for f in features):
                    return False

            return True

    return [device for device in devices if _filter(device)]


class Device(object):
    def __init__(self, path, usage):
        self.path = path
        self.usage = usage

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self):
        self._hid = hid.Device(path=self.path)

        self.manufacturer = self._hid.manufacturer
        self.product = self._hid.product
        self.serial = self._hid.serial

        return self

    def close(self):
        if self._hid:
            self._hid.close()
            self._hid = None

    def _call(self, h2d):
        msg_out = delimited.encode(h2d)

        for offset in range(0, len(msg_out), PAYLOAD_SIZE):
            buf = msg_out[offset:offset + PAYLOAD_SIZE]
            hdr = bytes([self.usage, len(buf)])
            buf = hdr + buf.ljust(PAYLOAD_SIZE, b'\x00')
            self._hid.write(buf)

        msg_in = bytearray()

        while True:
            buf = self._hid.read(1 + REPORT_COUNT)
            cnt = buf[1]
            msg_in += buf[2:cnt + 2]
            if cnt < PAYLOAD_SIZE:
                break

        return comm.MessageD2H.FromString(delimited.decode(msg_in))

    def version(self):
        h2d = comm.MessageH2D()
        h2d.action = comm.Action.VERSION

        d2h = self._call(h2d)

        return d2h.version

    def motor_get_state(self):
        h2d = comm.MessageH2D()
        h2d.action = comm.Action.MOTOR_GET_STATE

        d2h = self._call(h2d)

        return d2h.motor_state

    def eink_set_image(self, image):
        h2d = comm.MessageH2D()
        h2d.action = comm.Action.EINK_SET_IMAGE
        h2d.eink_image.id = round(random.random() * 1000000)
        h2d.eink_image.bits = image

        d2h = self._call(h2d)

        return d2h.eink_image
