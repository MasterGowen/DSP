"""Setup for dsp XBlock."""

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='dsp-xblock',
    version='0.1.1',
    description='digital signal processing XBlock',  # TODO: write a better description.
    license='UNKNOWN',  # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    url='https://github.com/MasterGowen/DSP',
    packages=[
        'dsp',
    ],
    install_requires=[
        'XBlock',
        'matplotlib==1.5.3',
        'mpld3==0.3'
    ],
    entry_points={
        'xblock.v1': [
            'dsp = dsp:DSPXBlock',
        ]
    },
    package_data=package_data("dsp", ["static", "templatetags", "translations"]),
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: Free For Educational Use',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Education :: Computer Aided Instruction (CAI)'
    ],
)
