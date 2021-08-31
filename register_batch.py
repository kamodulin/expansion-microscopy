import cv2
import os
from registration import rigid_registration


def get_images(path):
    images = [os.path.join(path, f) for f in os.listdir(path) if f[0] != "."]
    return sorted(images)


if __name__ == "__main__":
    base_path = os.path.abspath(__file__ + "/..")

    pre_folder = get_images(base_path + "/data/registration/pre_expansion")
    post_folder = get_images(base_path + "/data/registration/post_expansion")

    assert len(pre_folder) == len(post_folder), "Unequal number of images. Pre- and post-expansion directories must have a 1-to-1 matching of files."

    save_file = base_path + "/data/expansion_factors.csv"
    
    with open(save_file, "w") as f:
        f.write("id,expansion_factor\n")

    for i in range(len(pre_folder)):
        name = os.path.basename(pre_folder[i])
        name, _ = os.path.splitext(name)
        
        pre = cv2.imread(pre_folder[i], cv2.COLOR_BGR2GRAY)
        post = cv2.imread(post_folder[i], cv2.COLOR_BGR2GRAY)

        expansion_factor = rigid_registration(pre, post)

        with open(save_file, "a") as f:
            f.write(f"{name},{expansion_factor}\n")