import numpy as np


def get_scale_local_maximas_vectorized(cube_coordinates, laplacian_cube):
    """
    Check provided cube coordinate for scale space local maximas.
    Returns only the points that satisfy the criteria.

    A point is considered to be a local maxima if its value is greater
    than the value of the point on the next scale level and the point
    on the previous scale level. If the tested point is located on the
    first scale level or on the last one, then only one inequality should
    hold in order for this point to be local scale maxima.

    Parameters
    ----------
    cube_coordinates : (n, 3) ndarray
          A 2d array with each row representing 3 values, ``(y,x,scale_level)``
          where ``(y,x)`` are coordinates of the blob and ``scale_level`` is the
          position of a point in scale space.
    laplacian_cube : ndarray of floats
        Laplacian of Gaussian scale space. 

    Returns
    -------
    output : (n, 3) ndarray
        cube_coordinates that satisfy the local maximum criteria in
        scale space.

    Examples
    --------
    >>> one = np.array([[1, 2, 3], [4, 5, 6]])
    >>> two = np.array([[7, 8, 9], [10, 11, 12]])
    >>> three = np.array([[0, 0, 0], [0, 0, 0]])
    >>> check_coords = np.array([[1, 0, 1], [1, 0, 0], [1, 0, 2]])
    >>> lapl_dummy = np.dstack([one, two, three])
    >>> get_scale_local_maximas(check_coords, lapl_dummy)
    array([[1, 0, 1]])
    """
    x, y, z = [ cube_coordinates[:, ind] for ind in range(3) ]
 
    point_responses = laplacian_cube[x, y, z]
    lowers = point_responses.copy()
    uppers = point_responses.copy()
    not_layer_0 = z > 0
    lower_responses = laplacian_cube[x[not_layer_0], y[not_layer_0], z[not_layer_0]-1]
    lowers[not_layer_0] = lower_responses  
 
    not_max_layer = z < (laplacian_cube.shape[2] - 1)
    upper_responses = laplacian_cube[x[not_max_layer], y[not_max_layer], z[not_max_layer]+1]
    uppers[not_max_layer] = upper_responses
 
    lo_check = np.ones(z.shape, dtype=np.bool)
    lo_check[not_layer_0] = (point_responses > lowers)[not_layer_0]
    hi_check = np.ones(z.shape, dtype=np.bool)
    hi_check[not_max_layer] = (point_responses > uppers)[not_max_layer]
 
    return cube_coordinates[lo_check & hi_check]