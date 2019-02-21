#!/usr/bin/env python3
from os import path as op
from setuptools import setup

with open(op.join(op.abspath(op.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().split('\n')

with open('README.md') as f:
    readme = f.read()

with open('VERSION.txt') as f:
    version = str(f.read())

setup(
    name='MIYU',
    author='Robert Clayton',
    author_email='rclayton@theia.io',
    version=version,
    description='Data preparation for bounding box based machine learning',
    url='https://github.com/robert-clayton/MIYU/tree/master',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: GPLv3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='social-media scraper',
    include_package_data=True,
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'miyu=MIYU.miyu:main',
            'miyu=MIYU.miyu:main'
        ]
    },
    packages=['ILYA'],
    scripts=['ILYA/ilya.py']
)