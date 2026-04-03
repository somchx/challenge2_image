"""
matcher.py
----------
Descriptor matcher factory and Lowe's ratio test.

For float descriptors (SIFT):
    FLANN with FLANN_INDEX_KDTREE (efficient approximate nearest-neighbor)

For binary descriptors (ORB, AKAZE):
    FLANN with FLANN_INDEX_LSH  OR  BFMatcher with NORM_HAMMING

Reference: David Lowe, "Distinctive Image Features from Scale-Invariant
Keypoints", IJCV 2004 — Section 7.1 describes the ratio test.
"""

import cv2
import numpy as np
from typing import List, Tuple


# ──────────────────────────────────────────────
# Matcher factory
# ──────────────────────────────────────────────

def get_matcher(descriptor_type: str, use_flann: bool = True) -> cv2.DescriptorMatcher:
    """
    Create and return a configured descriptor matcher.

    Parameters
    ----------
    descriptor_type : str
        'float'  -> FLANN with KD-tree index   (for SIFT)
        'binary' -> FLANN with LSH index        (for ORB / AKAZE)
    use_flann : bool
        If False and descriptor_type is 'binary', use BFMatcher instead of FLANN.
        BFMatcher is brute-force but exact; sometimes more stable on small sets.

    Returns
    -------
    cv2.DescriptorMatcher
    """
    if descriptor_type == 'float':
        # KD-tree index: fast for high-dimensional float descriptors like SIFT
        FLANN_INDEX_KDTREE = 1
        index_params  = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)   # higher checks = more accurate, slower
        return cv2.FlannBasedMatcher(index_params, search_params)

    elif descriptor_type == 'binary':
        if use_flann:
            # LSH index: locality-sensitive hashing for binary descriptors
            FLANN_INDEX_LSH = 6
            index_params  = dict(
                algorithm     = FLANN_INDEX_LSH,
                table_number  = 6,    # number of hash tables
                key_size      = 12,   # bits per key
                multi_probe_level = 1
            )
            search_params = dict(checks=50)
            return cv2.FlannBasedMatcher(index_params, search_params)
        else:
            # Brute-force with Hamming distance — exact, slower
            return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    else:
        raise ValueError(
            f"Unknown descriptor_type '{descriptor_type}'. Use 'float' or 'binary'."
        )


# ──────────────────────────────────────────────
# Lowe's ratio test
# ──────────────────────────────────────────────

def apply_ratio_test(
    knn_matches: List[List[cv2.DMatch]],
    ratio: float = 0.75
) -> List[cv2.DMatch]:
    """
    Filter kNN matches (k=2) using Lowe's ratio test.

    A match is kept only if the best match distance is significantly
    smaller than the second-best, indicating a distinctive match.

    Parameters
    ----------
    knn_matches : list of [DMatch, DMatch] pairs
        Result of matcher.knnMatch(des1, des2, k=2).
    ratio : float
        Lowe's ratio threshold.  Typical values:
          0.75  -> standard (recommended by Lowe)
          0.70  -> stricter, fewer but more reliable matches
          0.80  -> more permissive, more matches but noisier

    Returns
    -------
    list of DMatch
        Filtered list of good matches.
    """
    good = []
    for pair in knn_matches:
        # Guard: knnMatch may return fewer than k matches near edges
        if len(pair) == 2:
            m, n = pair
            if m.distance < ratio * n.distance:
                good.append(m)
    return good


# ──────────────────────────────────────────────
# Convenience: match two descriptor arrays end-to-end
# ──────────────────────────────────────────────

def match_descriptors(
    des_template: np.ndarray,
    des_frame: np.ndarray,
    descriptor_type: str,
    ratio: float = 0.75,
    use_flann: bool = True
) -> Tuple[List[cv2.DMatch], int]:
    """
    Full matching pipeline: create matcher -> knnMatch -> ratio test.

    Parameters
    ----------
    des_template : np.ndarray
        Descriptors from the template image.
    des_frame : np.ndarray
        Descriptors from the current video frame.
    descriptor_type : str
        'float' or 'binary'.
    ratio : float
        Lowe's ratio threshold.
    use_flann : bool
        Whether to use FLANN (True) or BFMatcher (False, binary only).

    Returns
    -------
    good_matches : list of DMatch
    total_matches : int
        Number of kNN match pairs before ratio filtering.
    """
    if des_template is None or des_frame is None:
        return [], 0
    if len(des_template) < 2 or len(des_frame) < 2:
        return [], 0

    matcher      = get_matcher(descriptor_type, use_flann=use_flann)
    knn_matches  = matcher.knnMatch(des_template, des_frame, k=2)
    good_matches = apply_ratio_test(knn_matches, ratio=ratio)
    return good_matches, len(knn_matches)
