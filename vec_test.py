import numpy as np
def myfunc(a, b):
    if a > b:
        return a - b
    else:
        return a + b
a = [1,2,3,4]
b = [1,3,4]
vfunc = np.vectorize(myfunc)
result = vfunc(a, b)
print(result)