"""
utils.py
--------
Drawing helpers and video I/O utility functions.
"""

import cv2
import numpy as np
from typing import List, Optional, Tuple


# ──────────────────────────────────────────────
# Drawing
# ──────────────────────────────────────────────

def draw_bounding_box(
    frame: np.ndarray,
    corners: np.ndarray,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 3
) -> np.ndarray:
    """
    Draw a quadrilateral bounding box from the four projected corners.

    Parameters
    ----------
    frame : np.ndarray  BGR image
    corners : np.ndarray  shape (4,1,2) float32 — result of perspectiveTransform
    color : (B, G, R) tuple
    thickness : int  line thickness in pixels

    Returns
    -------
    frame : np.ndarray  annotated copy of the input frame
    """
    frame = frame.copy()
    pts = np.int32(corners).reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=thickness)
    return frame


def draw_hud(
    frame: np.ndarray,
    num_good_matches: int,
    total_matches: int,
    inlier_count: int,
    found: bool,
    reason: str = '',
    detector_name: str = ''
) -> np.ndarray:
    """
    Overlay a heads-up display with detection statistics in the top-left corner.
    """
    frame = frame.copy()
    status_text  = 'FOUND' if found else 'NOT FOUND'
    status_color = (0, 255, 0) if found else (0, 0, 255)

    lines = [
        (f"Detector : {detector_name.upper()}",       (200, 200, 200)),
        (f"Matches  : {num_good_matches}/{total_matches}", (200, 200, 200)),
        (f"Inliers  : {inlier_count}",                 (200, 200, 200)),
        (f"Status   : {status_text}",                  status_color),
    ]
    if not found and reason:
        lines.append((f"Reason   : {reason[:40]}", (100, 100, 255)))

    y0 = 28
    for i, (text, color) in enumerate(lines):
        y = y0 + i * 22
        # Dark background for readability
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        cv2.rectangle(frame, (8, y - th - 2), (8 + tw + 4, y + 4), (0, 0, 0), -1)
        cv2.putText(frame, text, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)

    return frame


def draw_keypoints_on_frame(
    frame: np.ndarray,
    keypoints: List[cv2.KeyPoint],
    color: Tuple[int, int, int] = (0, 255, 255)
) -> np.ndarray:
    """Draw keypoints on the frame (small circles at each keypoint location)."""
    return cv2.drawKeypoints(
        frame, keypoints, None,
        color=color,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )


# ──────────────────────────────────────────────
# Image preprocessing
# ──────────────────────────────────────────────

def to_gray(img: np.ndarray) -> np.ndarray:
    """Convert BGR to grayscale. If already grayscale, return as-is."""
    if img.ndim == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def apply_clahe(gray: np.ndarray, clip_limit: float = 2.0,
                tile_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization).
    Improves local contrast — helps feature detection under uneven lighting.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    return clahe.apply(gray)


def preprocess(img: np.ndarray, use_clahe: bool = True) -> np.ndarray:
    """Convert to grayscale and optionally apply CLAHE."""
    gray = to_gray(img)
    if use_clahe:
        gray = apply_clahe(gray)
    return gray


# ──────────────────────────────────────────────
# Video I/O
# ──────────────────────────────────────────────

def get_video_info(video_path: str) -> dict:
    """Return basic properties of a video file."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")
    info = {
        'fps':          cap.get(cv2.CAP_PROP_FPS),
        'frame_count':  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width':        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height':       int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    info['duration_sec'] = info['frame_count'] / max(info['fps'], 1)
    cap.release()
    return info


def create_video_writer(
    output_path: str, fps: float, width: int, height: int
) -> cv2.VideoWriter:
    """Create a VideoWriter for .mp4 output using mp4v codec."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not writer.isOpened():
        raise IOError(f"Cannot open VideoWriter at: {output_path}")
    return writer


# ──────────────────────────────────────────────
# Results aggregation
# ──────────────────────────────────────────────

def summarize_results(results: List[dict]) -> dict:
    """
    Aggregate per-frame result dicts from pipeline.run_on_video().

    Parameters
    ----------
    results : list of dicts, each with keys:
        'found', 'num_good_matches', 'inlier_count', 'reason'

    Returns
    -------
    dict with summary statistics
    """
    if not results:
        return {
            'total_frames': 0,
            'detected_frames': 0,
            'detection_rate': 0.0,
            'avg_good_matches': 0.0,
            'avg_inliers': 0.0,
        }

    total     = len(results)
    detected  = sum(1 for r in results if r['found'])
    avg_good  = np.mean([r['num_good_matches'] for r in results])
    avg_inliers = np.mean([r['inlier_count'] for r in results])

    return {
        'total_frames':    total,
        'detected_frames': detected,
        'detection_rate':  detected / total,
        'avg_good_matches': float(avg_good),
        'avg_inliers':     float(avg_inliers),
    }
