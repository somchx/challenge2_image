"""
homography.py
-------------
RANSAC homography estimation and bounding-box projection.

Uses cv2.findHomography with RANSAC to robustly estimate the 3x3
perspective transformation matrix H that maps template coordinates
to frame coordinates.

Then cv2.perspectiveTransform maps the four corners of the template
rectangle into the frame, giving the projected bounding polygon.
"""

import cv2
import numpy as np
from typing import List, Optional, Tuple


# ──────────────────────────────────────────────
# Core homography computation
# ──────────────────────────────────────────────

def compute_homography(
    kp_template: List[cv2.KeyPoint],
    kp_frame:    List[cv2.KeyPoint],
    good_matches: List[cv2.DMatch],
    min_match_count: int = 10,
    ransac_thresh: float = 5.0
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], int]:
    """
    Estimate homography H from template -> frame using RANSAC.

    Parameters
    ----------
    kp_template : list of KeyPoint
        Keypoints detected in the template image.
    kp_frame : list of KeyPoint
        Keypoints detected in the current frame.
    good_matches : list of DMatch
        Matches that passed Lowe's ratio test.
    min_match_count : int
        Minimum number of good matches required.  If fewer, return None.
    ransac_thresh : float
        Maximum reprojection error (pixels) for RANSAC inlier classification.

    Returns
    -------
    H : np.ndarray (3x3) or None
    dst_corners : np.ndarray (4,1,2) or None
        Projected corners of the template in frame space.
    inlier_count : int
        Number of inliers found by RANSAC (0 if computation failed).
    """
    if len(good_matches) < min_match_count:
        return None, None, 0

    # Build Nx2 arrays of matched point coordinates
    src_pts = np.float32(
        [kp_template[m.queryIdx].pt for m in good_matches]
    ).reshape(-1, 1, 2)

    dst_pts = np.float32(
        [kp_frame[m.trainIdx].pt for m in good_matches]
    ).reshape(-1, 1, 2)

    # RANSAC homography: robust to outliers among the matched points
    H, mask = cv2.findHomography(
        src_pts, dst_pts,
        cv2.RANSAC,
        ransacReprojThreshold=ransac_thresh
    )

    if H is None or mask is None:
        return None, None, 0

    inlier_count = int(mask.ravel().sum())
    return H, mask, inlier_count


def project_corners(H: np.ndarray, template_shape: Tuple[int, int]) -> np.ndarray:
    """
    Project the four corners of the template into the frame using H.

    Parameters
    ----------
    H : np.ndarray (3x3)
        Homography matrix mapping template -> frame.
    template_shape : (h, w)
        Height and width of the template image.

    Returns
    -------
    dst_corners : np.ndarray shape (4,1,2) float32
        The four projected corner points in frame coordinates.
        Order: top-left, top-right, bottom-right, bottom-left.
    """
    h, w = template_shape[:2]
    # Four corners of the template (clockwise from top-left)
    src_corners = np.float32([
        [0,   0  ],
        [w-1, 0  ],
        [w-1, h-1],
        [0,   h-1]
    ]).reshape(-1, 1, 2)

    dst_corners = cv2.perspectiveTransform(src_corners, H)
    return dst_corners


# ──────────────────────────────────────────────
# Geometry validation
# ──────────────────────────────────────────────

def validate_homography(
    H: np.ndarray,
    template_shape: Tuple[int, int],
    frame_shape:    Tuple[int, int],
    min_area_ratio: float = 0.005,
    max_area_ratio: float = 10.0
) -> Tuple[bool, str]:
    """
    Validate that a computed homography produces a sensible bounding box.

    Checks:
    1. Determinant of top-left 2x2 submatrix > 0  (no mirroring / extreme skew)
    2. Projected area is between min_area_ratio and max_area_ratio times template area
    3. The projected quadrilateral is convex
    4. All projected corners are within 2x the frame dimensions (not exploding off-screen)

    Parameters
    ----------
    H : np.ndarray (3x3)
    template_shape : (h, w)
    frame_shape : (h, w)
    min_area_ratio : float
    max_area_ratio : float

    Returns
    -------
    valid : bool
    reason : str
        'ok' if valid; otherwise a short description of why it failed.
    """
    # Check 1: no mirroring
    det = H[0, 0] * H[1, 1] - H[0, 1] * H[1, 0]
    if det <= 0:
        return False, f"negative_determinant({det:.3f})"

    # Project corners
    dst = project_corners(H, template_shape)
    pts = dst.reshape(4, 2)

    # Check 2: area within reasonable bounds
    template_area = template_shape[0] * template_shape[1]
    projected_area = cv2.contourArea(pts.astype(np.float32))
    ratio = projected_area / max(template_area, 1)
    if ratio < min_area_ratio:
        return False, f"area_too_small(ratio={ratio:.4f})"
    if ratio > max_area_ratio:
        return False, f"area_too_large(ratio={ratio:.2f})"

    # Check 3: convexity
    hull = cv2.convexHull(pts.astype(np.float32))
    if len(hull) < 4:
        return False, "degenerate_hull"
    if not cv2.isContourConvex(hull):
        return False, "non_convex"

    # Check 4: corners within 2x frame dimensions
    fh, fw = frame_shape[:2]
    margin = 2.0
    for pt in pts:
        x, y = pt
        if x < -fw * margin or x > fw * (1 + margin):
            return False, f"corner_out_of_frame_x({x:.0f})"
        if y < -fh * margin or y > fh * (1 + margin):
            return False, f"corner_out_of_frame_y({y:.0f})"

    return True, "ok"


# ──────────────────────────────────────────────
# Convenience: full pipeline step
# ──────────────────────────────────────────────

def find_object(
    kp_template:    List[cv2.KeyPoint],
    kp_frame:       List[cv2.KeyPoint],
    good_matches:   List[cv2.DMatch],
    template_shape: Tuple[int, int],
    frame_shape:    Tuple[int, int],
    min_match_count: int = 10,
    ransac_thresh:   float = 5.0,
    min_inliers:     int = 8,
    min_area_ratio:  float = 0.005,
    max_area_ratio:  float = 10.0
) -> dict:
    """
    Full homography step: estimate -> validate -> project corners.

    Returns
    -------
    dict with keys:
        'found'         : bool
        'corners'       : np.ndarray (4,1,2) or None
        'H'             : np.ndarray (3x3) or None
        'inlier_count'  : int
        'reason'        : str  ('ok' or failure reason)
    """
    H, mask, inlier_count = compute_homography(
        kp_template, kp_frame, good_matches,
        min_match_count=min_match_count,
        ransac_thresh=ransac_thresh
    )

    if H is None:
        n = len(good_matches)
        return {
            'found': False,
            'corners': None,
            'H': None,
            'inlier_count': 0,
            'reason': f'insufficient_matches({n}<{min_match_count})'
        }

    if inlier_count < min_inliers:
        return {
            'found': False,
            'corners': None,
            'H': H,
            'inlier_count': inlier_count,
            'reason': f'insufficient_inliers({inlier_count}<{min_inliers})'
        }

    valid, reason = validate_homography(
        H, template_shape, frame_shape,
        min_area_ratio=min_area_ratio,
        max_area_ratio=max_area_ratio
    )

    if not valid:
        return {
            'found': False,
            'corners': None,
            'H': H,
            'inlier_count': inlier_count,
            'reason': f'invalid_homography:{reason}'
        }

    corners = project_corners(H, template_shape)
    return {
        'found': True,
        'corners': corners,
        'H': H,
        'inlier_count': inlier_count,
        'reason': 'ok'
    }
