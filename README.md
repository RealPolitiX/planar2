## planar2

Planar2 is extended from the original [planar](https://github.com/Benjamin-Dobell/planar) by Casey Duncan. Planar is a 2D geometry library for Python. It is intended for use by games and interactive real-time applications, but is designed to be useful for most any program that needs a convenient, high-performance geometry API.


### Installation

To build and install Planar from the source distribution or repository use::
```
python setup.py install
```
To install only the pure-Python modules without compiling, use::
```
python setup.py build_py install --skip-build
```
Only performance is sacrificed without the C extensions, all functionality is
still available when using only the pure-Python modules.


### Documentation

The documentation for the older version (v0.4) of planar is [here](https://pythonhosted.org/planar/).