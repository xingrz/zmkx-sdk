zmkx-sdk [![.github/workflows/build.yml](https://github.com/xingrz/zmkx-sdk/actions/workflows/build.yml/badge.svg)](https://github.com/xingrz/zmkx-sdk/actions/workflows/build.yml)
========

[![release][release-img]][release-url] [![downloads][downloads-img]][downloads-url] [![license][license-img]][license-url] [![issues][issues-img]][issues-url] [![stars][stars-img]][stars-url] [![commits][commits-img]][commits-url]

[zmkx.app](https://github.com/xingrz/zmkx.app) 的 Python 实现，包含一个供二次开发的库和一个简单的 CLI 客户端。

## 安装

需要 Python 3.8 以上。

```sh
pip3 install -e .
```

## 快速上手

本仓库提供了一个最简单的 [`set_image.py`](set_image.py) 演示换图功能：

```sh
python3 set_image.py 你的图片.jpg
```

## 命令行

本仓库实现了一个命令行工具 [`zmkx`](bin/zmkx) 来操作设备，命令格式如下：

```
zmkx [-s SERIAL] command ...
```

完整命令说明请参考 `zmkx -h`。

#### 列出设备

```
$ zmkx list
* HelloWord HW-75 Dynamic (序列号: 34314704001A002B)
* HelloWord HW-75 Keyboard (序列号: 55895648066BFF53)
```

#### 监控电机状态

```
$ zmkx knob --monitor
控制模式: 角度 | 当前角度:  23.7° | 当前速度:   -0.01 rad/s | 目标角度:  30.6° | 目标速度:    1.76 rad/s | 目标电压:   0.035 V
```

#### 换图

```
$ zmkx eink --set 图片.jpg --dither
```

## 相关链接

* [zmkx.app](https://github.com/xingrz/zmkx.app)
* [ZMK for HW-75](https://github.com/xingrz/zmk-config_helloword_hw-75)
* [peng-zhihui/HelloWord-Keyboard](https://github.com/peng-zhihui/HelloWord-Keyboard)

## 协议

[MIT License](LICENSE)

[release-img]: https://img.shields.io/github/v/release/xingrz/zmkx-sdk?style=flat-square
[release-url]: https://github.com/xingrz/zmkx-sdk/releases/latest
[downloads-img]: https://img.shields.io/github/downloads/xingrz/zmkx-sdk/total?style=flat-square
[downloads-url]: https://github.com/xingrz/zmkx-sdk/releases
[license-img]: https://img.shields.io/github/license/xingrz/zmkx-sdk?style=flat-square
[license-url]: LICENSE
[issues-img]: https://img.shields.io/github/issues/xingrz/zmkx-sdk?style=flat-square
[issues-url]: https://github.com/xingrz/zmkx-sdk/issues
[stars-img]: https://img.shields.io/github/stars/xingrz/zmkx-sdk?style=flat-square
[stars-url]: https://github.com/xingrz/zmkx-sdk/stargazers
[commits-img]: https://img.shields.io/github/last-commit/xingrz/zmkx-sdk?style=flat-square
[commits-url]: https://github.com/xingrz/zmkx-sdk/commits/master
