# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='apispec-ext-webframeworks',
    version='0.1',
    description='Web frameworks plugins for ApiSpec.',
    long_description=read('README.md'),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/marshmallow-code/apispec-ext.webframeworks',
    packages=find_packages(exclude=('test*', )),
    include_package_data=True,
    extras_require={},
    license='MIT',
    zip_safe=False,
    keywords='apispec swagger openapi specification documentation spec rest api web frameworks',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    project_urls={
        'Funding': 'https://opencollective.com/marshmallow',
        'Issues': 'https://github.com/marshmallow-code/apispec-ext-webframeworks/issues'
    },
)
