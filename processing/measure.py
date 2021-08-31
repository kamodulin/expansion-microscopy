import numpy as np
from edt import edt3d
from skan import Skeleton, summarize
from skimage.morphology import skeletonize_3d


"""
Lateral and axial lightsheet resolution (microns).
"""
x_res = 0.091000116097948115
z_res = 0.52175056847846326


def measure(vol, expansion_factor):   
    voxel_size = x_res * x_res * z_res
    sampling = (z_res, x_res, x_res)

    normalized_voxel_size = voxel_size / (expansion_factor ** 3)
    normalized_sampling = tuple(dim / expansion_factor for dim in sampling)

    total_img_volume = vol.size * normalized_voxel_size
    total_axon_volume = np.count_nonzero(vol) * normalized_voxel_size

    skeleton = skeletonize_3d(vol)
    branch_data = summarize(Skeleton(skeleton, spacing=normalized_sampling))
    total_axon_length = branch_data["branch-distance"].sum()

    # significantly faster than scipy.ndimage.distance_transform_edt
    distance_transform = edt3d(vol, anisotropy=normalized_sampling, black_border=False, order="C", parallel=10)
    avg_axon_radius = np.mean(distance_transform[skeleton.astype(bool)])

    return [total_img_volume, total_axon_volume, total_axon_length, avg_axon_radius]