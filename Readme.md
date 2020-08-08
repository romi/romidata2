romidata2
=========

WORK IN PROGRESS


## Installation

Clone the code repository from github:

```
git clone https://github.com/romi/romidata2.git
```


Install the dependencies for the romidata2 module:

```shell
python -m pip install tzlocal
python -m pip install python-dateutil
python -m pip install fs
```

In addition, if you want to use the REST server, you must install the
following modules:

```shell
python -m pip install flask flask_cors flask_restful
python -m pip install Pillow
```

## Examples

See the examples/*.py script for some example in Python.
See examples/html/ for a minima example of the REST API in Javascript.

## Documentation

* See docs/webapi/ for documenation on the REST API.
* See docs/assets/ for a diagram of the datamodel.

