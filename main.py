import pymeshlab

def processFile(input_file, output_file):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_file)
    print(f"Loaded {input_file}")

    ms.load_filter_script('scripts/laplacian.mlx')
    ms.apply_filter_script()

    ms.save_current_mesh(output_file)
    print(f"Saved processed mesh as {output_file}")

input_model = input("Enter the input model file path: ")
output_model = input("Enter the output model file path: ")
processFile(input_model, output_model)