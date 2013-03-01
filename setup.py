try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='deltacloud_heat',
    version='0.1.0',
    description='Deltacloud backend for Heat',
    author='Tomas Sedovic',
    author_email='tomas@sedovic.cz',
    url='https://github.com/tomassedovic/deltacloud_heat',
    packages=['deltacloud_heat'],
    install_requires=[
        'deltacloud>=0.9.1',
        'python-novaclient',
    ],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description = open('README.rst').read(),
)