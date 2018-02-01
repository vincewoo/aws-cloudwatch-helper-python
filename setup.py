#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='metricshelper',
      version='1.0',
      description='Simplifying collecting and publishing metrics to AWS Cloudwatch',
      author='vwoo',
      author_email='vince.woo@jpl.nasa.gov',
      url='https://github.jpl.nasa.gov/vwoo/aws-cloudwatch-helper-python',
      packages=find_packages()
      )
