# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='pynagsystemd',
    packages=find_packages(),
    version='1.2.0',
    scripts=['bin/pynagsystemd.py'],
    install_requires=[
        'nagiosplugin>=1.2',
    ],
    description='A simple nagios plugin that detects failed systemd units.',
    author='Andrea Briganti',
    author_email='kbytesys@gmail.com',
    url='https://github.com/kbytesys/pynagsystemd',
    download_url='https://github.com/kbytesys/pynagsystemd/tarball/v1.2.0',
    keywords=['nagios', 'systemd'],
    license='GNU LGPL v2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking :: Monitoring'
    ],
)


