#*****************************************************************************
#   Copyright 2013 Thomas Calmant
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

from . import _jvmfinder
import os

# ------------------------------------------------------------------------------

class CygwinJVMFinder(_jvmfinder.JVMFinder):
    """
    Cygwin JVM library finder class
    """
    def __init__(self):
        """
        Sets up members
        """
        # Call the parent constructor
        _jvmfinder.JVMFinder.__init__(self)

        # Library file name
        self._libfile = "jvm.dll"

        # Predefined locations
        self._locations = set()
        for key in (
                # 64 bits (or 32 bits on 32 bits OS) JDK
                'ProgramFiles'
                # 32 bits JDK on 32 bits OS
                'ProgramFiles(x86)'):
            try:
                env_folder = os.environ[key]
                self._locations.add(os.path.join(env_folder, "Java"),)
            except KeyError:
                # Environment variable is missing (ignore)
                pass

        # Search methods
        self._methods = (self._get_from_java_home,
                         self._get_from_known_locations)
