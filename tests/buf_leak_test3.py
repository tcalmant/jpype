#!/usr/bin/python3
# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
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

from jpype import *

remote_pack = "c:/tools/netbeean-remote-pack"

profiler_options = [
    "-agentpath:%s/lib/deployed/jdk15/windows/profilerinterface.dll="
    "%s/lib,5140" % (remote_pack, remote_pack)
]

options = [
    # '-verbose:gc',
    '-Xmx64m',
    '-Djava.class.path=classes'
]  # + profiler_options

cnt = 0

# setUsePythonThreadForDeamon(True)
startJVM(getDefaultJVMPath(), *options)


class MyStr(str):
    def __init__(self, val):
        str.__init__(self, val)
        global cnt
        cnt += 1
        print('created string', cnt)

    def __del__(self):
        global cnt
        cnt -= 1
        print('deleted string', cnt)


receive = JClass("jpype.nio.NioReceive")

while True:
    # everything runs great with this line uncommented
    # p = JString('5' * 1024 * 1024)

    # with this line uncommented, the python strings aren't GC'd
    p = java.lang.StringBuffer(MyStr('5' * 1024 * 1024))

    # with this line uncommented, the JVM throws an OutOfMemoryError
    # (not GC'ing the proxied java objects?),
    # but the python strings are being GC'd
    # p = java.lang.StringBuffer(JString(MyStr('5' * 1024 * 1024)))

    #
    # forget the direct buffer for now....
    #
    buf = nio.convertToDirectBuffer(MyStr('5' * 1024 * 1024 * 5))
    try:
        receive.receiveBufferWithException(buf)
    except:
        pass
