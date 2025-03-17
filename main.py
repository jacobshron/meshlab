import pymeshlab
import numpy as np
from scipy.spatial import Voronoi

def processFile(input_file, output_file):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_file)
    print(f"Loaded {input_file}")

    ms.generate_sampling_poisson_disk(samplenum=500)
    sampled_mesh = ms.current_mesh()
    vertices = np.array(sampled_mesh.vertex_matrix())

    vor = Voronoi(vertices)

    # Save Voronoi edges as an OBJ file
    with open("voronoi.obj", "w") as f:
        # Write vertices
        for v in vor.vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Write edges as faces (for visualization)
        for edge in vor.ridge_vertices:
            if -1 not in edge:  # Ignore infinite edges
                f.write(f"l {edge[0]+1} {edge[1]+1}\n")  # 'l' defines a line in OBJ

    # Load the generated Voronoi structure
    ms.load_new_mesh("voronoi.obj")

    # Apply filters (e.g., thickening, smoothing)
    ms.apply_filter("simplify_quadric_edge_collapse_decimation", targetfacenum=5000)  # Simplify the mesh
    ms.apply_filter("remove_isolated_pairs")  # Remove isolated edges or vertices
    ms.apply_filter("smooth_laplacian", iterations=10)  # Smooth the mesh to improve appearance

    ms.save_current_mesh(output_file)
    print(f"Saved processed mesh as {output_file}")

input_model = input("Enter the input model file path: ")
output_model = input("Enter the output model file path: ")

processFile(input_model, output_model)