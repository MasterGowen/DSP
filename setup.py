"""Setup for dsp XBlock."""

import os

from setuptools import setup
# from Cython.Build import cythonize

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
    # ext_modules = cythonize(["*.pyx"]),
    version='0.1',
    description='digital signal processing XBlock',   # TODO: write a better description.
    license='UNKNOWN',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    packages=[
        'dsp',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'dsp = dsp.dsp:DSPXBlock',
        ]
    },
    package_data=package_data("dsp", ["static", "public"]),
)
