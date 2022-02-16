#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

description = ('Scrapes text data about the store/company from '
               'Naver Place.')
with open('README.md', 'r') as f:
    long_description = f.read()

install_requires = [
    'pandas>=1.3.3',
    'requests>=2.26.0',
    'importlib_resources>=5.4.0'
]

project_urls = {
  'Source': 'https://github.com/choi-jiwoo/naver-place-scraper',
}

setup(
    name='naverplacescraper',
    version='0.7.2',
    author='Choi Jiwoo',
    author_email='cho2.jiwoo@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    keywords=['python', 'sns', 'scraper', 'crawler'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls=project_urls,
)
