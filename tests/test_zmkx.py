import unittest
from unittest.mock import MagicMock
from binascii import unhexlify

from zmkx import Device

ZMKX_REPORT_ID = 1


def assert_hid_calls(calls):
    assert len(calls) >= 1
    for i, (args, kwargs) in enumerate(calls):
        assert isinstance(args[0], bytes)
        assert len(args[0]) == 64
        assert args[0][0] == ZMKX_REPORT_ID
        if i == len(calls) - 1:
            assert args[0][1] < 62
        else:
            assert args[0][1] == 62


class DeviceTestCase(unittest.TestCase):
    def setUp(self):
        self.device = Device("device_path", ZMKX_REPORT_ID)
        self.device._hid = MagicMock()

    def tearDown(self):
        self.device.close()

    def test_version(self):
        self.device._hid.read.return_value = unhexlify(
            '012e2d08011a290a07306633343535391207386634306366391a0736393534616337220c08011001180120012801300100000000000000000000000000000000')

        version = self.device.version()

        self.assertIsNotNone(version.zephyr_version)
        self.assertIsNotNone(version.zmk_version)
        self.assertIsNotNone(version.app_version)

        self.device._hid.write.assert_called()
        assert_hid_calls(self.device._hid.write.call_args_list)

    def test_motor_get_state(self):
        self.device._hid.read.return_value = unhexlify(
            '0126250802222108dcc1febd0710021d2a3fa0c025112ebe3c2dc19a9ec035fc6574403d12699e3d180120012801300100000000000000000000000000000000')

        state = self.device.motor_get_state()

        self.assertIsNotNone(state.timestamp)
        self.assertIsNotNone(state.control_mode)
        self.assertIsNotNone(state.current_angle)
        self.assertIsNotNone(state.current_velocity)
        self.assertIsNotNone(state.target_angle)
        self.assertIsNotNone(state.target_velocity)
        self.assertIsNotNone(state.target_voltage)

        self.device._hid.write.assert_called()
        assert_hid_calls(self.device._hid.write.call_args_list)

    def test_eink_set_image(self):
        self.device._hid.read.return_value = unhexlify(
            '01090808073a0408d1e42e33343535391207386634306366391a0736393534616337220c08011001180120012801300100000000000000000000000000000000')

        result = self.device.eink_set_image(bytes([0xFF] * 16 * 296))

        self.assertIsNotNone(result.id)

        self.device._hid.write.assert_called()
        assert_hid_calls(self.device._hid.write.call_args_list)


if __name__ == '__main__':
    unittest.main()
