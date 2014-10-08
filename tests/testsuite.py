#!/usr/bin/python3
# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
# 	   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

# WARNING: This test suite must be ran from inside the "tests" folder

import unittest
import os.path

from jpypetest import test_numeric, test_attr, test_array, test_objectwrapper,\
    test_proxy, test_exc, test_serial, test_mro
import jpype


def suite():
    return unittest.TestSuite((
        test_numeric.suite(),
        test_attr.suite(),
        test_array.suite(),
        test_objectwrapper.suite(),
        test_proxy.suite(),
        test_exc.suite(),
        test_serial.suite(),
        test_mro.suite(),
    ))


def runTest():
    root = os.path.abspath(os.path.dirname(__file__))

    print("Running testsuite using JVM: {0}".format(jpype.getDefaultJVMPath()))
    jpype.startJVM(jpype.getDefaultJVMPath(),
                   "-ea", "-Xmx256M", "-Xms64M",
                   "-Djava.class.path={0}"
                   .format(os.path.join(root, "classes")))

    runner = unittest.TextTestRunner()
    runner.run(suite())

    s = slice(2, 4)
    print("{0} {1}".format(s, dir(s)))

    jpype.shutdownJVM()


if __name__ == '__main__':
    runTest()
