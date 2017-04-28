#!/usr/bin/env python3

import os
from setuptools import setup


def resolve_meta():
  result = {}
  f = open('META')
  contents = f.read()
  f.close()
  for line in contents.split('\n'):
    if ' = ' in line:
      attr, value = line.split(' = ')
      result[attr] = value.replace('\'', '')
  return result


def resolve_namespace_packages():
  result = []
  packages = resolve_packages()
  for package in packages:
    f = open(package.replace('.', '/') + '/__init__.py')
    contents = f.read()
    f.close()
    if '__import__(\'pkg_resources\').declare_namespace(__name__)' in contents:
      result.append(package)
  return sorted(result)


def resolve_packages():
  result = []
  for root, dirs, files in os.walk('.', topdown = False):
    if '__init__.py' in files:
      if 'tests' not in root:
        result.append(root[2:].replace('/', '.'))
  return sorted(result)


def resolve_requirements():
  result = []
  try:
    f = open('requirements.txt', 'r')
    contents = f.read()
    f.close()
    for line in contents.split('\n'):
      result.append(line.strip())
  except:
    pass
  return result


meta = resolve_meta()

setup(
  name=meta['PACKAGE'],
  version=meta['VERSION'],

  license=meta['LICENSE'],

  description=meta['DESCRIPTION'],
  long_description='',
  url=meta['URL'],

  classifiers=[
    meta['DEV_STATUS'],
    meta['LICENSE'],
    meta['OS'],
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Version Control',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],

  author=meta['AUTHOR'],
  author_email=meta['AUTHOR_EMAIL'],

  namespace_packages=resolve_namespace_packages(),
  packages=resolve_packages(),

  install_requires=resolve_requirements(),

  zip_safe=bool(meta['ZIP_SAFE'])
)

# vim: expandtab:ts=2:sw=2:
