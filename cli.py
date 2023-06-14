from argparse import ArgumentParser
import zmkx


def list(serial, features):
    devices = zmkx.find_devices(serial=serial, features=features)
    for d in devices:
        print(f'* {d.manufacturer} {d.product} (序列号: {d.serial})')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--serial', help='指定所操作的设备的序列号')

    subparsers = parser.add_subparsers(dest='command', metavar='command',
                                       help='命令')

    list_parser = subparsers.add_parser('list', help='列出所有符合条件的设备')
    list_parser.add_argument('-f', '--features', nargs='+', default=[],
                             help='只列出支持指定特性的设备')

    kwargs = vars(parser.parse_args())
    command = kwargs.pop('command')
    if command in globals():
        globals()[command](**kwargs)
    else:
        parser.print_help()
