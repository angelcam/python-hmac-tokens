#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="hmac_tokens",
    version='1.2.0',
    description="Angelcam HMAC token helpers",
    keywords="hmac api token",
    author="Angelcam",
    author_email="dev@angelcam.com",
    url="https://bitbucket.org/angelcam/python-hmac-tokens/",
    license="MIT",
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ]
)
