#!/usr/bin/python3
# ****************************************************************************
#   Copyright 2004-2008 Steve Menard
#
#   Licensed under the Apache License, Version 2.0 (the "License");
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
# ****************************************************************************

import jpype

jvm_lib = jpype.getDefaultJVMPath()
print("JVM Library path:", jvm_lib)

jpype.startJVM(jvm_lib)
props = jpype.java.lang.System.getProperties()
try:
    for key in props.keySet():
        if key.startswith("java") or key.startswith("sun"):
            print(key, "->", props.getProperty(key))
except:
    pass

jpype.shutdownJVM()
