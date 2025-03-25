import pymeshlab
import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial import Delaunay

def processFile(input_file, output_file):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_file)
    print(f"Loaded {input_file}")

    ms.generate_sampling_poisson_disk(samplenum=500)
    sampled_mesh = ms.current_mesh()
    vertices = np.array(sampled_mesh.vertex_matrix())

    vor = Voronoi(vertices)

    # Perform Delaunay triangulation to generate faces
    tri = Delaunay(vertices)

    with open("voronoi.obj", "w") as f:
        # Write vertices
        for v in vor.vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Write faces from Delaunay triangulation
        for simplex in tri.simplices:
            f.write(f"f {simplex[0]+1} {simplex[1]+1} {simplex[2]+1}\n")  # OBJ indexing starts from 1

    # Load the generated Voronoi structure
    ms.load_new_mesh("voronoi.obj")

    # Apply filters (e.g., thickening, smoothing)
    ms.apply_filter("meshing_decimation_quadric_edge_collapse", targetfacenum=5000)  # Simplify the mesh
    ms.apply_filter("meshing_remove_connected_component_by_face_number", mincomponentsize=10)  # Remove isolated edges or vertices
    ms.apply_filter("smooth_laplacian", iterations=10)  # Smooth the mesh to improve appearance

    ms.save_current_mesh(output_file)
    print(f"Saved processed mesh as {output_file}")

input_model = input("Enter the input model file path: ")
output_model = input("Enter the output model file path: ")

processFile(input_model, output_model)