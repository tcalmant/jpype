#!/usr/bin/python3
# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

__all__ = ['common', 'test_array', 'test_attr', 'test_objectwrapper',
           'test_proxy', 'test_numeric', 'test_exc', 'test_serial', 'test_mro']

import os

import jpype


def setup_package():
    """
    Sets up the test package: starts a JVM.
    See https://nose.readthedocs.org/en/latest/writing_tests.html
    """
    # Get name of the folder above the one containing the current file
    root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    jpype.startJVM(jpype.getDefaultJVMPath(),
                   "-ea", "-Xmx256M", "-Xms64M",
                   "-Djava.class.path={0}"
                   .format(os.path.join(root, "classes")))


def teardown_package():
    """
    Stops the JVM use in tests
    """
    # Stop the JVM
    jpype.shutdownJVM()
