import pytest

import python as python_module

def test_pyinfo_constructor_creates_non_none_instance():
    py_info = python_module.PyInfo()
    assert py_info is not None

