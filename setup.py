from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md'), encoding='utf-8').read()

version = '0.2.1'

setup(
    name='zmkx',
    version=version,
    author='XiNGRZ',
    author_email='hi@xingrz.me',
    description='Python client for ZMKX',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/xingrz/zmkx-sdk',
    license='MIT',
    packages=find_packages(),
    scripts=['bin/zmkx'],
    install_requires=[
        'hid>=1.0.5',
        'protobuf>=3.20.1',
        'inquirer>=3.1.3',
        'pillow>=9.5.0',
    ],
)
