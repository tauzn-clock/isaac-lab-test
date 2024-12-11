import open3d as o3d
import numpy as np
from utils import *

# Load the .obj file
mesh = o3d.io.read_triangle_mesh("filtered_terrain.obj")

mesh.compute_vertex_normals()

#o3d.visualization.draw_geometries([mesh])

# Extract vertices and faces as numpy arrays
vertices = np.asarray(mesh.vertices)
faces = np.asarray(mesh.triangles)

print(len(vertices), len(faces))


graph = [set() for _ in range(len(vertices))]

mask = np.zeros(len(faces), dtype=bool)

for i, face in enumerate(faces):
    vert = vertices[face]
    if angle_to_z(vert) < np.pi/72: # Tune acceptable planes
        mask[i] = True

        v0, v1, v2 = face
        graph[v0].add(v1)
        graph[v0].add(v2)
        graph[v1].add(v0)
        graph[v1].add(v2)
        graph[v2].add(v0)
        graph[v2].add(v1)

new_faces =faces[mask]

print(len(new_faces))

# Create a new mesh with the filtered vertices and faces
new_mesh = o3d.geometry.TriangleMesh()
new_mesh.vertices = o3d.utility.Vector3dVector(vertices)
new_mesh.triangles = o3d.utility.Vector3iVector(new_faces)

new_mesh.compute_vertex_normals()

o3d.visualization.draw_geometries([new_mesh])