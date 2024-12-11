import open3d as o3d

# Load the .obj file
mesh = o3d.io.read_triangle_mesh("terrain.obj")

mesh.compute_vertex_normals()

o3d.visualization.draw_geometries([mesh])