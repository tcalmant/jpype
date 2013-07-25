JPype - Python 3
================

From the [original Website](http://jpype.sourceforge.net/index.html):

> JPype is an effort to allow python programs full access to java class libraries.
> This is achieved not through re-implementing Python, as Jython/JPython has done,
> but rather through interfacing at the native level in both Virtual Machines.
> Eventually, it should be possible to replace Java with python in many, though not all, situations.
> JSP, Servlets, RMI servers and IDE plugins are good candidates.
>
> Once this integration is achieved, a second phase will be started to separate the Java logic from
> the Python logic, eventually allowing the bridging technology to be used in other environments,
> I.E. Ruby, Perl, COM, etc ...

This github fork is a Python 3 version of jPype. *It does not support Python 2*.

This is a fork of [originell/jpype](https://github.com/originell/jpype),
which originally aims to simplify the installation of jPype on Linux and MacOS X.

Known Bugs/Limitations
----------------------
* Java classes outside of a package (in the `<default>`) cannot be imported.
* unable to access a field or method if it conflicts with a python keyword.
* Because of lack of JVM support, you cannot shutdown the JVM and then restart it.
* Some methods rely on the "current" class/caller. Since calls coming directly from
  python code do not have a current class, these methods do not work. The User Manual
  lists all the known methods like that.

Requirements
------------

JDK and JRE.

Installation
------------

Easy as

    python setup.py install

:+1:

Tested on
---------

* OS X 10.7.4 with Sun/Oracle JDK 1.6.0
* Debian 6.0.4/6.0.5 with Sun/Oracle JDK 1.6.0
* Ubuntu 12.04 with Sun/Oracle JDK 1.6.0
