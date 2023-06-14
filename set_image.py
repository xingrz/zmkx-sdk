#!/usr/bin/env python3

from argparse import ArgumentParser
import inquirer
from PIL import Image
import zmkx

CANVAS_WIDTH = 128
CANVAS_HEIGHT = 296


def get_device(features=[]):
    devices = zmkx.find_devices(features=features)

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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file', help='指定要显示的图片文件')

    args = parser.parse_args()

    device = get_device(features=['knob'])
    if device is None:
        exit(1)

    with device.open() as device, Image.open(args.file) as image:
        image.thumbnail((CANVAS_WIDTH, CANVAS_HEIGHT))

        center = ((CANVAS_WIDTH - image.width) // 2,
                  (CANVAS_HEIGHT - image.height) // 2)

        canvas = Image.new('L', (CANVAS_WIDTH, CANVAS_HEIGHT), color=0xFF)
        canvas.paste(image, center)

        canvas = canvas.convert('1', dither=Image.FLOYDSTEINBERG)

        device.eink_set_image(canvas.tobytes())
