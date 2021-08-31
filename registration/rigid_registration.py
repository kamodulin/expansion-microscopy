import numpy as np
import cv2


def rescale_and_convert(image):
    lower_bound, upper_bound = np.percentile(image, (0, 98))

    image = np.clip(image, lower_bound, upper_bound)
    image = (image - lower_bound) / (upper_bound - lower_bound)

    return np.asarray(image * (2 ** 8 - 1), dtype=np.uint8)


def rigid_registration(pre, post, h_flip=False):
    if not h_flip:
        if pre.dtype != np.uint8:
            pre = rescale_and_convert(pre)    
        if post.dtype != np.uint8:
            post = rescale_and_convert(post)

    sift = cv2.xfeatures2d.SIFT_create(sigma=1.6)
    kp1, des1 = sift.detectAndCompute(post, None)
    kp2, des2 = sift.detectAndCompute(pre, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 10

    if len(good) > MIN_MATCH_COUNT:
        print("\x1b[32mSuccess! Enough matches found: %d>%d\x1b[0m."% (len(good), MIN_MATCH_COUNT), "Horizontal flip:", h_flip)

        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, _ = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC)
 
        cos_scale = M[0, 0]
        sin_scale = M[0, 1]

        expansion_factor = 1 / ((cos_scale ** 2 + sin_scale ** 2) ** 0.5)

    elif not h_flip:
        print("\x1b[31mFailure! Not enough matches are found: %d<%d\x1b[0m."% (len(good), MIN_MATCH_COUNT), "Attempting horizontal flip...")
        return rigid_registration(pre, post[:, ::-1], h_flip=True)

    else:
        print("\x1b[31mFailure! Not enough matches are found: %d<%d\x1b[0m."% (len(good), MIN_MATCH_COUNT), "Horizontal flip:", h_flip)
        expansion_factor = None

    return expansion_factor