import open3d as o3d
import numpy as np
import trimesh

def angle_to_z(vertices):
    """Calculate the angle of the vertices with respect to the z-axis."""

    cross_product = np.cross((vertices[1] - vertices[0]), (vertices[2] - vertices[0]))
    cross_product = cross_product / (np.linalg.norm(cross_product) + 1e-7)

    angle_1 = np.arccos(np.dot(cross_product, np.array([0, 0, 1])))
    angle_2 = np.arccos(np.dot(cross_product, np.array([0, 0, -1])))

    return min(abs(angle_1), abs(angle_2))



def get_stepable_region(mesh):
    # Extract vertices and faces as numpy arrays
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces).astype(np.uint16)

    print("Verices: ", len(vertices), "Faces: ", len(faces))


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

    print("New Faces: ", len(new_faces))

    # Create a Trimesh object
    trimesh_obj = trimesh.Trimesh(vertices=vertices, faces=new_faces)
    return trimesh_obj

if __name__ == "__main__":
    # Load the .obj file
    mesh = o3d.io.read_triangle_mesh("filtered_terrain.obj")
    mesh.compute_vertex_normals()

    #o3d.visualization.draw_geometries([mesh])

    new_trimesh = get_stepable_region(mesh)

    vertices = new_trimesh.vertices
    faces = new_trimesh.faces

    new_mesh = o3d.geometry.TriangleMesh()
    new_mesh.vertices = o3d.utility.Vector3dVector(vertices)
    new_mesh.triangles = o3d.utility.Vector3iVector(faces)

    # Optionally, you can compute normals for visualization
    new_mesh.compute_vertex_normals()


    o3d.visualization.draw_geometries([new_mesh])