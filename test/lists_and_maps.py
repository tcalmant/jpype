#!/usr/bin/env python3

from jpype import java, startJVM, getDefaultJVMPath

startJVM(getDefaultJVMPath())

arr = java.util.ArrayList()

# no matching overloads found for this line:
arr.addAll([str(x) for x in range(50)])

print(arr)

hmap = java.util.HashMap()

# no matching overloads found for this line:
hmap.putAll({5:6, 7:8, 'hello':'there'})

print(hmap)

# for x in xrange(5):
#    # this works:
#    hmap.put(str(x), str(x))
#    # but this doesn't:
#    hmap.put(str(x), x)
#
#
# # this throws: AttributeError: 'java.util.HashMap' object has no attribute 'iterator'
# for x in hmap:
#    print x, hmap[x]
