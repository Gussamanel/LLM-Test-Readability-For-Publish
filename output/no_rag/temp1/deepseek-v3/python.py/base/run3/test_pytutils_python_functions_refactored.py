import pytest
import python as python_module

def test_pyinfo_can_be_instantiated():
    py_info = python_module.PyInfo()
    assert isinstance(py_info, python_module.PyInfo)

