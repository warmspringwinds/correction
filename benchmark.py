import numpy as np
from timer import take_time
from main import get_scale_local_maximas_cython
from vectorized import get_scale_local_maximas_vectorized
 
lapl_dummy = np.random.rand(100,100,100)
coords = np.random.random_integers(0,99, size=(1000,3))

with take_time('description'):
    get_scale_local_maximas_cython(coords, lapl_dummy)

with take_time('vectorized'):
    get_scale_local_maximas_vectorized(coords, lapl_dummy)