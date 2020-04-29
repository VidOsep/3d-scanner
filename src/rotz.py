import numpy as np

def rotz(theta):
    """
    Rotation about Z-axis
    @type theta: number
    @param theta: the rotation angle
    @rtype: 3x3 orthonormal matrix
    @return: rotation about Z-axis
    @see: L{rotx}, L{roty}, L{rotvec}
    @author: Luis Fernando Lara Tobar and Peter Corke
    """
    ct = np.cos(theta)
    st = np.sin(theta)

    return np.mat([[ct,      -st,  0],
            [st,       ct,  0],
            [ 0,    0,  1]])