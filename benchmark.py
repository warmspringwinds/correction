import numpy as np
from timer import take_time
from main import get_scale_local_maximas_cython
 
lapl_dummy = np.random.rand(100,100,100)
coords = np.random.random_integers(0,99, size=(1000,3))

with take_time('description'):
    get_scale_local_maximas_cython(coords, lapl_dummy)
 



