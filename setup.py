#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import Command, setup, find_packages
from setuptools.command.test import test

import os
import re
import sys
import codecs

try:
    import platform
    _pyimp = platform.python_implementation
except (AttributeError, ImportError):
    def _pyimp():
        return 'Python'

NAME = 'deux'

E_UNSUPPORTED_PYTHON = '%s 1.1.1 requires %%s %%s or later!' % (NAME,)

PYIMP = _pyimp()
PY26_OR_LESS = sys.version_info < (2, 7)
PY3 = sys.version_info[0] == 3
PY33_OR_LESS = PY3 and sys.version_info < (3, 4)
PYPY_VERSION = getattr(sys, 'pypy_version_info', None)
PYPY = PYPY_VERSION is not None
PYPY24_ATLEAST = PYPY_VERSION and PYPY_VERSION >= (2, 4)

if PY26_OR_LESS:
    raise Exception(E_UNSUPPORTED_PYTHON % (PYIMP, '2.7'))
elif PY33_OR_LESS and not PYPY24_ATLEAST:
    raise Exception(E_UNSUPPORTED_PYTHON % (PYIMP, '3.4'))

# -*- Classifiers -*-

classes = """
    Development Status :: 4 - Beta
    License :: OSI Approved :: BSD License
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Framework :: Django
    Framework :: Django :: 1.9
    Framework :: Django :: 1.10
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

# -*- Distribution Meta -*-

re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_vers = re.compile(r'VERSION\s*=.*?\((.*?)\)')
re_doc = re.compile(r'^"""(.+?)"""')


def rq(s):
    return s.strip("\"'")


def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, rq(attr_value)),)


def add_version(m):
    v = list(map(rq, m.groups()[0].split(', ')))
    return (('VERSION', '.'.join(v[0:3]) + ''.join(v[3:])),)


def add_doc(m):
    return (('doc', m.groups()[0]),)

pats = {re_meta: add_default,
        re_vers: add_version,
        re_doc: add_doc}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, NAME, '__init__.py')) as meta_fh:
    meta = {}
    for line in meta_fh:
        if line.strip() == '# -eof meta-':
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))

# -*- Installation Requires -*-

def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def _reqs(*f):
    return [
        _pip_requirement(r) for r in (
            strip_comments(l) for l in open(
                os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]

# -*- Long Description -*-

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See http://pypi.python.org/pypi/%s' % (NAME,)


setup(
    name=NAME,
    version=meta['VERSION'],
    description=meta['doc'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    platforms=['any'],
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    include_package_data=False,
    zip_safe=False,
    install_requires=reqs('default.txt'),
    tests_require=reqs('test.txt'),
    classifiers=classifiers,
    long_description=long_description,
)
