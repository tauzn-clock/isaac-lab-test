import numpy as np

def angle_to_z(vertices):
    """Calculate the angle of the vertices with respect to the z-axis."""

    cross_product = np.cross((vertices[1] - vertices[0]), (vertices[2] - vertices[0]))
    cross_product = cross_product / (np.linalg.norm(cross_product) + 1e-7)

    angle_1 = np.arccos(np.dot(cross_product, np.array([0, 0, 1])))
    angle_2 = np.arccos(np.dot(cross_product, np.array([0, 0, -1])))

    return min(abs(angle_1), abs(angle_2))

