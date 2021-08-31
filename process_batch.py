import os
import pandas as pd
import sys
from processing import process_volume, measure

if __name__ == "__main__":
    base_path = os.path.abspath(__file__ + "/..")

    expansion_factors = pd.read_csv(base_path + "/data/expansion_factors.csv")
    expansion_factors_dict = {}

    input_batch = sys.argv[1:]

    for input_folder in input_batch:
        if not os.path.isdir(input_folder):
            raise Exception(input_folder + " is not a directory. Inputs must be a folder of files.")
        
        row = expansion_factors[expansion_factors["id"]  == os.path.basename(input_folder)[4:-4]]
        expansion_factor = row["expansion_factor"].values[0]

        if not expansion_factor:
            raise Exception(input_folder + " does not have an expansion factor.")
        
        expansion_factors_dict[input_folder] = expansion_factor
    
    assert len(input_batch) == len(expansion_factors_dict), "Collisions when creating expansion_factor dictionary (i.e. one to many relationship)."

    print(f"Number of volumes: {len(expansion_factors_dict)}")

    save_file = base_path + "/data/segmentation_data.csv"

    with open(save_file, "w") as f:
        f.write("id,image_volume (um3),axon_volume (um3),axon_length (um),avg_axon_radius (um)\n")

    for input_folder, expansion_factor in expansion_factors_dict.items():
        name = os.path.basename(input_folder)
        print(f"Processing {name}")

        vol = process_volume(input_folder)
        data = measure(vol, expansion_factor)
        
        with open(save_file, "a") as f:
            f.write(f"{name},{data[0]},{data[1]},{data[2]},{data[3]}\n")