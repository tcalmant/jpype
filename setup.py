#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
import os
import sys
import platform

from distutils.core import setup as distSetup
from distutils.core import Extension


class JPypeSetup(object):
    """
    jPype setup utility class
    """

    def __init__(self):
        """
        Sets up members
        """
        # C++ source files
        self.cpp = []

        # JDK home folder
        self.javaHome = None

        # JDK (extra) include folder
        self.jdkInclude = None

        # C++ libraries
        self.libraries = []

        # C++ libraries folders
        self.libraryDir = []

        # C++ compiler definitions
        self.macros = []

        # C++ compiler extra arguments
        self.extra_compile_args = []


    def setupFiles(self):
        """
        Sets up the list of files to be compiled
        """
        # Source folders
        common_dir = os.path.join("src", "native", "common")
        python_dir = os.path.join("src", "native", "python")

        # List all .cpp files in those folders
        cpp_files = []
        for folder in (common_dir, python_dir):
            cpp_files.extend(os.path.join(folder, filename)
                             for filename in os.listdir(folder)
                             if os.path.splitext(filename)[1] == '.cpp')

        self.cpp = cpp_files


    def setupWindows(self):
        """
        Set up the compilation properties for Windows
        """
        # Use the JAVA_HOME environment variable
        home = os.getenv("JAVA_HOME")
        if not home:
            print('Environment variable JAVA_HOME must be set')
            sys.exit(-1)

        # TODO: look in the Windows registry if needed

        if not os.path.exists(home):
            # Check if the path is valid
            print('No JDK found at JAVA_HOME={0}'.format(home))
            sys.exit(-1)

        # Compiler configuration...
        self.javaHome = home
        self.jdkInclude = "win32"
        self.libraries = ["Advapi32"]
        self.libraryDir = [os.path.join(self.javaHome, "lib")]
        self.macros = [("WIN32", 1)]
        self.extra_compile_args = ['/EHsc']


    def setupMacOSX(self):
        """
        Set up the compilation properties for Mac OS 10.6, 10.7 or 10.8 
        """
        # Changes according to:
        # http://stackoverflow.com/questions/8525193/cannot-install-jpype-on-os-x-lion-to-use-with-neo4j
        # and
        # http://blog.y3xz.com/post/5037243230/installing-jpype-on-mac-os-x
        osx = platform.mac_ver()[0][:4]
        javaHome = '/Library/Java/Home'
        if osx == '10.6':
            # I'm not sure if this really works on all 10.6 - confirm please
            # :)
            javaHome = ('/Developer/SDKs/MacOSX10.6.sdk/System/Library/'
                        'Frameworks/JavaVM.framework/Versions/1.6.0/')

        elif osx in ('10.7', '10.8'):
            javaHome = ('/System/Library/Frameworks/JavaVM.framework/'
                        'Versions/Current/')

        # Compiler configuration...
        self.javaHome = javaHome
        self.jdkInclude = ""
        self.libraries = ["dl"]
        self.libraryDir = [os.path.join(self.javaHome, "Libraries")]
        self.macros = [('MACOSX', 1)]


    def __find_jdk(self, parent):
        """
        Tries to find a JDK folder in the first-level children of the
        given folder
        
        :param parent: A parent folder
        :return: The first found JDK, or None
        """
        for folder in os.listdir(parent):
            # Construct the full path
            java_home = os.path.join(parent, folder)

            # Lower-case content tests
            folder = folder.lower()

            # Consider it's a JDK if it has an 'include' folder
            # and if the folder name contains 'jdk' or 'java'
            if os.path.isdir(java_home) \
            and ('jdk' in folder or 'java' in folder):
                include_path = os.path.join(java_home, 'include')
                if os.path.exists(include_path):
                    # Match
                    return java_home

        return None


    def setupLinux(self):
        """
        Sets up the compilation properties for Linux
        """
        # Use the JAVA_HOME environment variable
        home = os.getenv("JAVA_HOME")
        if home:
            # Validate the given Java home
            include_path = os.path.join(home, 'include')
            if not os.path.exists(include_path):
                # Not a JDK...
                print('WARNING: JAVA_HOME ({0}) does not point to a JDK. '
                      'Looking for another one.'
                      .format(home))
                home = None

        if not home:
            # Known places where we might find a JDK
            possible_install_dirs = ('/usr/lib/jvm', '/usr/java')

            for install in possible_install_dirs:
                if os.path.isdir(install):
                    home = self.__find_jdk(install)
                    if home:
                        # Match
                        self.javaHome = home
                        print('Using JDK at {0}'.format(home))
                        break

            else:
                # No JDK found: Abandon
                print("No Java/JDK could be found. I looked in the following "
                      "directories:\n{0}\n"
                      "Please check that you have a JDK installed.\n"
                      "If you have and the destination is not in the above "
                      "list please consider opening a ticket or creating a "
                      "pull request on github: "
                      "https://github.com/tcalmant/jpype/"
                      .format('\n'.join(possible_install_dirs)))
                sys.exit(1)

        # Compiler configuration...
        self.javaHome = home
        self.jdkInclude = "linux"
        self.libraries = ["dl"]
        self.libraryDir = [os.path.join(self.javaHome, "lib")]


    def setupPlatform(self):
        """
        Chooses the setup method to call according to the current platform
        """
        if sys.platform == 'win32':
            self.setupWindows()

        elif sys.platform == 'darwin':
            self.setupMacOSX()

        else:
            self.setupLinux()


    def setupInclusion(self):
        """
        Sets up the headers files folders
        """
        if sys.platform == 'darwin':
            headerDirName = 'Headers'
        else:
            headerDirName = 'include'

        self.includeDirs = [
            os.path.join("src", "native", "common", "include"),
            os.path.join("src", "native", "python", "include"),
            os.path.join(self.javaHome, headerDirName)
        ]

        if self.jdkInclude:
            # This one might be empty
            self.includeDirs.append(os.path.join(self.javaHome, headerDirName,
                                                 self.jdkInclude))


    def setup(self):
        """
        Package setup
        """
        # Look for C++ files
        self.setupFiles()

        # Look for the JDK installation
        self.setupPlatform()

        # Set up C++ include folders
        self.setupInclusion()

        # Define the Python extension
        jpypeLib = Extension("_jpype",
                             self.cpp,
                             libraries=self.libraries,
                             define_macros=self.macros,
                             include_dirs=self.includeDirs,
                             library_dirs=self.libraryDir,
                             extra_compile_args=self.extra_compile_args
                             )

        # Setup the package
        distSetup(
            name="JPype - Python 3",
            version="0.5.5",
            description="Python-Java bridge. Fork of the jPype project by "
            "Steve Menard (http://jpype.sourceforge.net/), with the "
            "modifications applied by Luis Nell "
            "(https://github.com/originell/jpype)",
            long_description=open("README.md").read(),
            author="Thomas Calmant",
            author_email="thomas.calmant@gmail.com",
            url="http://github.com/tcalmant/jpype-py3/",
            packages=[
                "jpype", 'jpype.awt', 'jpype.awt.event',
                'jpypex', 'jpypex.swing'],
            package_dir={
                "jpype": os.path.join("src", "python", "jpype"),
                'jpypex': os.path.join("src", "python", "jpypex"),
            },
            ext_modules=[jpypeLib],
            classifiers=[
                'Intended Audience :: Developers',
                'License :: OSI Approved :: Apache Software License',
                'Programming Language :: Python :: 3'
            ]
        )

if __name__ == "__main__":
    JPypeSetup().setup()
