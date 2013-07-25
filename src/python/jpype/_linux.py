#*****************************************************************************
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
#*****************************************************************************
import os
import re


_KNOWN_LOCATIONS = [
        ("/opt/sun/", re.compile(r"j2sdk(.+)/jre/lib/i386/client/libjvm.so")),
        ("/usr/java/", re.compile(r"j2sdk(.+)/jre/lib/i386/client/libjvm.so")),
        ("/usr/java/", re.compile(r"jdk(.+)/jre/lib/i386/client/libjvm.so")),
]

JRE_ARCHS = ["amd64/server/libjvm.so",
             "i386/client/libjvm.so",
             "i386/server/libjvm.so", ]

def filter_homes(homes):
    """
    Filters the given possible Java home folders: the last part of the name
    must contain 'java', 'jre' or 'jdk'.
    
    :param homes: A list of homes
    :return: A generator filtering the given homes
    """
    for home in homes:
        # Only accept directories
        if not os.path.isdir(home):
            continue

        # Use lower-case for comparisons
        folder = os.path.dirname(home).lower()
        if not folder:
            # Invalid folder name
            continue

        # Filter names
        for java_name in ('jre', 'jdk', 'java'):
            if java_name in folder:
                # Seems to be a good name
                break
        else:
            # Doesn't seem to be a valid JVM installation
            continue

        # Yield the current folder
        yield home


def find_libjvm(java_home):
    """
    Recursively looks for the given file
    
    :param java_home: A JVM home folder
    :return: The first found file path, or None
    """
    # Look for the file
    filename = "libjvm.so"

    for root, _, names in os.walk(java_home):
        if filename in names:
            # Found it
            return os.path.join(root, filename)

    else:
        # File not found
        return None


def getDefaultJVMPath():
    jvm = _getJVMFromJavaHome()
    if jvm is not None:
        return jvm

    # on Linux, the JVM has to be in the LD_LIBRARY_PATH anyway,
    # so might as well inspect it first
    jvm = _getJVMFromLibPath()
    if jvm is not None:
        return jvm

    # failing that, lets look in the "known" locations
    for parent in _KNOWN_LOCATIONS:
        # Get all children
        children = map(lambda x: os.path.join(parent, x), os.listdir(parent))

        for home in filter_homes(children):
            jvm = find_libjvm(home)
            if jvm is not None:
                return jvm

    # Not found
    raise ValueError("No libjvm.so file found. Try setting up the JAVA_HOME "
                     "environment variable properly.")


def _getJVMFromJavaHome():
    java_home = os.getenv("JAVA_HOME")
    if not java_home:
        try:
            # Look for the real installation path
            java_home = os.path.realpath('/usr/bin/java').replace('bin/java', '')
        except:  # I know. catchall is bad...
            # Avoid NoneType + String
            java_home = ''

    rootJre = None
    if os.path.exists(java_home + "/bin/javac"):
        # this is a JDK home
        rootJre = java_home + '/jre/lib'
    elif os.path.exists(java_home + "/bin/java"):
        # this is a JRE home
        rootJre = java_home + '/lib'
    else:
        return None

    for i in JRE_ARCHS:
        if os.path.exists(rootJre + "/" + i):
            return rootJre + "/" + i
    return None


def _getJVMFromLibPath():
    if 'LD_LIBRARY_PATH' in os.environ:
        libpath = os.environ['LD_LIBRARY_PATH']
        if libpath is None:
            return None

        paths = libpath.split(os.pathsep)
        for i in paths:
            if i.find('jre') != -1:
                # this could be it!
                # TODO
                pass

    return None
