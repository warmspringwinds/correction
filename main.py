import numpy as np
cimport numpy as cnp
 
 
def get_scale_local_maximas_cython(cnp.ndarray[cnp.int_t, ndim=2] cube_coordinates, cnp.ndarray[cnp.double_t, ndim=3] laplacian_cube):
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
 
    cdef Py_ssize_t y_coord, x_coord, point_layer, point_index
    cdef cnp.double_t point_response, lower_point_response, upper_point_response
    cnp.ndarray[cnp.int_t] interest_point_coords
    cdef Py_ssize_t amount_of_layers = laplacian_cube.shape[2]
    cdef Py_ssize_t amount_of_points = cube_coordinates.shape[0]
 
    # Preallocate index. Fill it with False.
    accepted_points_index = np.ones(amount_of_points, dtype=bool)
 
    for point_index in range(amount_of_points):
 
        interest_point_coords = cube_coordinates[point_index]
        # Row coordinate
        y_coord = interest_point_coords[0]
        # Column coordinate
        x_coord = interest_point_coords[1]
        # Layer number starting from the smallest sigma
        point_layer = interest_point_coords[2]
        point_response = laplacian_cube[y_coord, x_coord, point_layer]
 
        # Check the point under the current one
        if point_layer != 0:
            lower_point_response = laplacian_cube[y_coord, x_coord, point_layer-1]
            if lower_point_response >= point_response:
                accepted_points_index[point_index] = False
                continue
 
        # Check the point above the current one
        if point_layer != (amount_of_layers-1):
            upper_point_response = laplacian_cube[y_coord, x_coord, point_layer+1]
            if upper_point_response >= point_response:
                accepted_points_index[point_index] = False
                continue
 
    # Return only accepted points
    return cube_coordinates[accepted_points_index]