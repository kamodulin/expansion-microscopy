# Expansion Microscopy Analysis
Analysis code for expansion factor estimation and TRAILMAP ([fork](https://github.com/kamodulin/TRAILMAP), [original](https://github.com/AlbertPun/TRAILMAP)) post-processing used in []().

## Expansion Factor Estimation
To quantify expansion factor, pre- and post-expansion images of the same field of view were acquired on an Olympus FV3000 confocal with a 4x/0.16NA air objective.

Expansion factor calculation was performed using an implementation of the scale-invariant feature transform (SIFT) algorithm.
1. Generate SIFT descriptor keypoints `cv2.xfeatures2d.SIFT_create()`
2. Brute force match descriptors via `cv2.BFMatcher()` object and its `knnMatch()` method
3. Estimate a partial 2D affine transformation between pre- and post-expansion keypoints, restricting image alignment to rotation, translation, and uniform scaling  `cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC)`

This was designed to batch process pairs of expansion images located in the /data/registration/ directory. Images with the same name in both pre and post folders are treated as image pairs.

```
data/
└──registration/
    └──pre_expansion/
    │  └──example1.tif
    │  └──example2.tif
    └──post_expansion/
       └──example1.tif
       └──example2.tif
```

### Usage
```python
python3 register_batch.py
```

### Output
An expansion_factors.csv file is written to the data directory with the following columns:
- id
- expansion_factor

## Post-processing of TRAILMAP segmentations
Huge thanks to Friedmann D, Pun A, et al. for creating the [TRAILMAP](https://github.com/AlbertPun/TRAILMAP) package. My [forked repo](https://github.com/kamodulin/TRAILMAP) adds additional functionality and provides a link to my model used to segment my images.

After TRAILMAP segmentation, probabilties are thresholded (P > 0.7) and objects smaller than 256 voxels are removed. Total axon volume, total axon length, and average axon radius are then extracted from this 3D binary volume. All measurements are normalized by the ROI's expansion factor.

### Usage
```python
python3 process_batch.py input_folder1 input_folder2
```

Example:
```python
python3 process_batch.py data/trailmap_volumes/seg-example1.tif data/trailmap_volumes/seg-example2.tif
```

or process all volumes in /data/trailmap_volumes/
```python
python3 process_batch.py data/trailmap_volumes/*
```

Note: expansion factors are retrieved from the expansion_factors.csv file located in the data directory. TRAILMAP creates image sequences with leading "seg-" and trailing ".tif" strings, and they should match to an `id` in this csv without these strings. i.e. ***example1*** and seg-***example1***.tif.

### Output
A segmentation_data.csv file is written to the data directory with the following columns:
- id
- total image volume (um3)
- total axon volume (um3)
- total axon length (um)
- average axon radius (um)

## Requirements
```
numpy
scikit-image
opencv-contrib-python (note: opencv-python includes SIFT as of 2021. https://github.com/opencv/opencv/issues/16736)
pandas
edt (3D euclidean distance transform, https://github.com/seung-lab/euclidean-distance-transform-3d)
skan (skeleton analysis, https://github.com/jni/skan)
```
