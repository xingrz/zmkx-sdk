#!/usr/bin/env python3

from argparse import ArgumentParser
import inquirer
import math
from time import sleep
from PIL import Image
import zmkx
from zmkx.comm_pb2 import MotorState


def list(serial, features):
    devices = zmkx.find_devices(serial=serial, features=features)
    for d in devices:
        print(f'* {d.manufacturer} {d.product} (序列号: {d.serial})')


def get_device(serial, features=[]):
    devices = zmkx.find_devices(serial=serial, features=features)

    if len(devices) == 0:
        print('未找到符合条件的设备')
        return None

    if len(devices) == 1:
        return devices[0]

    choice = inquirer.prompt([
        inquirer.List('device', message='有多个设备，请选择', choices=[
            (f'{d.manufacturer} {d.product} (SN: {d.serial})', d)
            for d in devices
        ]),
    ])

    if choice is None:
        return None

    return choice['device']


def knob(serial, monitor):
    device = get_device(serial, features=['knob'])
    if device is None:
        return

    def rad_norm(rad):
        rad = rad % (2 * math.pi)
        return rad if rad >= 0 else rad + 2 * math.pi

    def rad_to_deg(rad):
        return rad * 180 / math.pi

    with device.open() as device:
        try:
            while True:
                status = device.motor_get_state()

                control_mode = {
                    MotorState.ControlMode.TORQUE: '扭矩',
                    MotorState.ControlMode.VELOCITY: '速度',
                    MotorState.ControlMode.ANGLE: '角度',
                }[status.control_mode]

                current_angle = '{:5.1f}°'.format(
                    rad_to_deg(rad_norm(status.current_angle)))

                current_velocity = '{:7.2f} rad/s'.format(
                    status.current_velocity)

                target_angle = '{:5.1f}°'.format(rad_to_deg(rad_norm(status.target_angle)))  \
                    if status.control_mode == MotorState.ControlMode.ANGLE \
                    else '------'

                target_velocity = '{:7.2f} rad/s'.format(
                    status.target_velocity)

                target_voltage = '{:7.3f} V'.format(
                    status.target_voltage)

                print(' | '.join([
                    f'控制模式: {control_mode}',
                    f'当前角度: {current_angle}',
                    f'当前速度: {current_velocity}',
                    f'目标角度: {target_angle}',
                    f'目标速度: {target_velocity}',
                    f'目标电压: {target_voltage}',
                ]), end='\r')

                if not monitor:
                    break

                sleep(0.1)
        except KeyboardInterrupt:
            pass


def eink(serial, set, dither=False):
    device = get_device(serial, features=['knob'])
    if device is None:
        return

    CANVAS_WIDTH = 128
    CANVAS_HEIGHT = 296

    with device.open() as device, Image.open(set) as image:
        image.thumbnail((CANVAS_WIDTH, CANVAS_HEIGHT))

        center = ((CANVAS_WIDTH - image.width) // 2,
                  (CANVAS_HEIGHT - image.height) // 2)

        canvas = Image.new('L', (CANVAS_WIDTH, CANVAS_HEIGHT), color=0xFF)
        canvas.paste(image, center)

        canvas = canvas.convert(
            '1', dither=Image.FLOYDSTEINBERG if dither else Image.NONE)

        device.eink_set_image(canvas.tobytes())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--serial', help='指定所操作的设备的序列号')

    subparsers = parser.add_subparsers(dest='command', metavar='command',
                                       help='命令')

    list_parser = subparsers.add_parser('list', help='列出所有符合条件的设备')
    list_parser.add_argument('-f', '--features', nargs='+', default=[],
                             help='只列出支持指定特性的设备')

    knob_parser = subparsers.add_parser('knob', help='旋钮控制')
    knob_parser.add_argument('-m', '--monitor', action='store_true',
                             help='实时监控电机状态')

    eink_parser = subparsers.add_parser('eink', help='墨水屏控制')
    eink_parser.add_argument('--set',
                             help='指定要显示的图片文件')
    eink_parser.add_argument('-d', '--dither', action='store_true',
                             help='使用抖动')

    kwargs = vars(parser.parse_args())
    command = kwargs.pop('command')
    if command in globals():
        globals()[command](**kwargs)
    else:
        parser.print_help()
