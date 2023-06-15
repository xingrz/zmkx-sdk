from setuptools import setup, find_packages

setup(
    name='zmkx',
    version='0.2.0',
    author='XiNGRZ',
    author_email='hi@xingrz.me',
    description='Python client for ZMKX',
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
