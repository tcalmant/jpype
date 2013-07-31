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

# ------------------------------------------------------------------------------

# Predefined locations on Linux
PREDEFINED_LOCATIONS = ("/usr/lib/jvm",
                        "/usr/java",
                        "/opt/sun")

# ------------------------------------------------------------------------------

def getDefaultJVMPath():
    """
    Retrieves the path to the JVM library (libjvm.so) according to:
    
    * the JAVA_HOME environment variable
    * the /usr/bin/java executable real path
    * the known locations (/usr/lib/jvm, /usr/java, ...)
    
    :return: The path to the libjvm.so file
    :raise ValueError: No JVM library found
    """
    for method in (_getJVMFromJavaHome, _getJVMFromBin,
                   _getJVMFromKnownLocations):
        jvm = method()
        if jvm is not None:
            return jvm

    else:
        # Not found
        raise ValueError("No libjvm.so file found. "
                         "Try setting up the JAVA_HOME environment variable "
                         "properly.")

# ------------------------------------------------------------------------------

def _find_libjvm(java_home, filename="libjvm.so"):
    """
    Recursively looks for the given file
    
    :param java_home: A JVM home folder
    :param filename: Name of the file to find
    :return: The first found file path, or None
    """
    # Look for the file
    for root, _, names in os.walk(java_home):
        if filename in names:
            # Found it
            return os.path.join(root, filename)

    else:
        # File not found
        return None


def _find_possible_homes(parents):
    """
    Generator that looks for the first-level children folders that could be JVM
    installations, according to their name
    
    :param parents: A list of parent directories
    :return: The possible JVM installation folders
    """
    homes = []
    java_names = ('jre', 'jdk', 'java')

    for parent in parents:
        for childname in sorted(os.listdir(parent)):
            # Compute the real path
            path = os.path.realpath(os.path.join(parent, childname))
            if path in homes or not os.path.isdir(path):
                # Already known path, or not a directory -> ignore
                continue

            # Check if the path seems OK
            real_name = os.path.basename(path).lower()
            for java_name in java_names:
                if java_name in real_name:
                    # Correct JVM folder name
                    homes.append(path)
                    yield path
                    break

# ------------------------------------------------------------------------------

def _getJVMFromJavaHome():
    """
    Retrieves the Java library path according to the JAVA_HOME environment
    variable
    
    :return: The path to the JVM library, or None 
    """
    java_home = os.getenv("JAVA_HOME")
    if java_home and os.path.exists(java_home):
        return _find_libjvm(java_home)


def _getJVMFromBin(java_bin="/usr/bin/java"):
    """
    Retrieves the Java library path according to the real installation of
    the java executable
    
    :param java_bin: Path to the Java interpreter (default: /usr/bin/java)
    :return: The path to the JVM library, or None
    """
    # Find the real interpreter installation path
    java_bin = os.path.realpath(java_bin)
    if os.path.exists(java_bin):
        # Get to the home directory
        java_home = os.path.abspath(os.path.join(os.path.dirname(java_bin),
                                                 '..'))

        # Look for the JVM library
        return _find_libjvm(java_home)


def _getJVMFromKnownLocations():
    """
    Retrieves the first existing Java library path in the predefined known
    locations
    
    :return: The path to the JVM library, or None 
    """
    for home in _find_possible_homes(PREDEFINED_LOCATIONS):
        jvm = _find_libjvm(home)
        if jvm is not None:
            return jvm
