"""
detector.py
-----------
Feature detector factory.
Returns a configured cv2.Feature2D object by name.

Detectors available (all traditional, no ML):
  - 'sift'  : SIFT  – scale and rotation invariant, 128-dim float descriptor
  - 'orb'   : ORB   – fast binary descriptor, no patent
  - 'akaze' : AKAZE – non-linear scale space, binary/float descriptor
"""

import cv2


def get_detector(name: str, **kwargs) -> cv2.Feature2D:
    """
    Create and return a configured feature detector/descriptor.

    Parameters
    ----------
    name : str
        One of 'sift', 'orb', 'akaze' (case-insensitive).
    **kwargs : dict
        Override default parameters for the chosen detector.

    Returns
    -------
    cv2.Feature2D
        Configured detector that supports .detectAndCompute(img, mask).
    """
    name = name.lower()

    if name == 'sift':
        # SIFT: scale-invariant, rotation-invariant, 128-dim float descriptor
        # nfeatures=0 -> detect as many as possible (auto)
        # contrastThreshold: lower = more keypoints (may include weaker ones)
        # edgeThreshold: higher = fewer edge-like keypoints rejected
        nfeatures       = kwargs.get('nfeatures', 0)
        contrast_thresh = kwargs.get('contrastThreshold', 0.04)
        edge_thresh     = kwargs.get('edgeThreshold', 10)
        sigma           = kwargs.get('sigma', 1.6)
        return cv2.SIFT_create(
            nfeatures=nfeatures,
            contrastThreshold=contrast_thresh,
            edgeThreshold=edge_thresh,
            sigma=sigma
        )

    elif name == 'orb':
        # ORB: FAST keypoints + BRIEF descriptor (rotation-aware)
        # Binary 256-bit descriptor -> use Hamming distance
        nfeatures  = kwargs.get('nfeatures', 1500)
        scale      = kwargs.get('scaleFactor', 1.2)
        nlevels    = kwargs.get('nlevels', 8)
        score_type = kwargs.get('scoreType', cv2.ORB_HARRIS_SCORE)
        return cv2.ORB_create(
            nfeatures=nfeatures,
            scaleFactor=scale,
            nlevels=nlevels,
            scoreType=score_type
        )

    elif name == 'akaze':
        # AKAZE: non-linear scale space, robust to noise
        # Descriptor type MLDB_UPRIGHT is rotation-sensitive; MLDB handles rotation
        descriptor_type = kwargs.get('descriptor_type', cv2.AKAZE_DESCRIPTOR_MLDB)
        descriptor_size = kwargs.get('descriptor_size', 0)   # 0 = full size
        threshold       = kwargs.get('threshold', 0.001)
        diffusivity     = kwargs.get('diffusivity', cv2.KAZE_DIFF_PM_G2)
        return cv2.AKAZE_create(
            descriptor_type=descriptor_type,
            descriptor_size=descriptor_size,
            threshold=threshold,
            diffusivity=diffusivity
        )

    else:
        raise ValueError(
            f"Unknown detector '{name}'. Choose from: 'sift', 'orb', 'akaze'."
        )


def descriptor_dtype(name: str) -> str:
    """
    Return 'float' or 'binary' for the descriptor type produced by the named detector.
    Used by matcher.py to select the appropriate matching strategy.
    """
    name = name.lower()
    if name == 'sift':
        return 'float'
    elif name in ('orb', 'akaze'):
        return 'binary'
    else:
        raise ValueError(f"Unknown detector '{name}'.")
