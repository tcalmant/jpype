#!/usr/bin/python3
# *****************************************************************************
# Copyright 2004-2008 Steve Menard
#
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
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
    '-verbose:gc',
    '-Xmx16m',
]  # + profiler_options

startJVM(getDefaultJVMPath(), *options)


class MyStr(str):
    def __del__(self):
        print('string got deleted')


while True:
    buf = java.lang.String('5' * 1024 * 1024 * 5)
    buf = nio.convertToDirectBuffer(MyStr('5' * 1024 * 1024))
    # time.sleep(1)
