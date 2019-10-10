# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(name='scrapy_imit',
      version='1.0',
      description='A spider framewoke like scrapy_redis',
      long_description='',
      author='long',
      author_email='1029130619@qq.com',
      url='https://github.com/LongLinwei/scrapy_imit',
      license='Apache License v2',
      install_requires=["requests>=2.22.0","lxml>=4.3.4"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='spider,scrapy,redisr',
      packages=find_packages(),
      include_package_data=True,
      package_data={'': ['*.*']}
      )