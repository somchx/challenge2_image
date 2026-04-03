"""
pipeline.py
-----------
Full object detection pipeline: template preprocessing -> per-frame detection.

Usage example:
    from src.pipeline import ObjectDetectionPipeline

    pipeline = ObjectDetectionPipeline('templates/easy/template_e1.jpg',
                                        detector_name='sift',
                                        ratio=0.75,
                                        min_matches=10)
    results = pipeline.run_on_video('videos/easy/video_e1.mp4',
                                     output_path='outputs/easy/output_e1.mp4')
"""

import os
import cv2
import numpy as np
from typing import List, Optional

from src.detector  import get_detector, descriptor_dtype
from src.matcher   import match_descriptors
from src.homography import find_object
from src.utils     import preprocess, draw_bounding_box, draw_hud, \
                          create_video_writer, get_video_info, summarize_results


class ObjectDetectionPipeline:
    """
    Template-based object detection using feature point matching + homography.

    Steps (template, done once at init):
        1. Load template image
        2. Preprocess: grayscale + CLAHE
        3. Detect keypoints and compute descriptors

    Steps (per frame, called in run_on_video):
        1. Preprocess frame identically to template
        2. Detect keypoints and compute descriptors
        3. Match descriptors: knnMatch + Lowe's ratio test
        4. Estimate homography with RANSAC
        5. Validate homography geometry
        6. Project template corners -> bounding box in frame
    """

    def __init__(
        self,
        template_path:  str,
        detector_name:  str   = 'sift',
        ratio:          float = 0.75,
        min_matches:    int   = 10,
        min_inliers:    int   = 8,
        ransac_thresh:  float = 5.0,
        use_clahe:      bool  = True,
        use_flann:      bool  = True,
        min_area_ratio: float = 0.005,
        max_area_ratio: float = 10.0,
        **detector_kwargs
    ):
        """
        Parameters
        ----------
        template_path : str
            Path to the template (reference) image.
        detector_name : str
            Feature detector: 'sift', 'orb', or 'akaze'.
        ratio : float
            Lowe's ratio threshold for filtering matches.
        min_matches : int
            Minimum good matches to attempt homography.
        min_inliers : int
            Minimum RANSAC inliers for a valid detection.
        ransac_thresh : float
            Reprojection error threshold for RANSAC (pixels).
        use_clahe : bool
            Whether to apply CLAHE contrast enhancement on both template and frames.
        use_flann : bool
            Use FLANN matcher (True) or BFMatcher (False, binary descriptors only).
        min_area_ratio / max_area_ratio : float
            Bounds for the projected bounding-box area relative to template area.
        **detector_kwargs :
            Forwarded to the detector constructor (e.g., nfeatures=2000).
        """
        self.detector_name  = detector_name.lower()
        self.ratio          = ratio
        self.min_matches    = min_matches
        self.min_inliers    = min_inliers
        self.ransac_thresh  = ransac_thresh
        self.use_clahe      = use_clahe
        self.use_flann      = use_flann
        self.min_area_ratio = min_area_ratio
        self.max_area_ratio = max_area_ratio

        # Load and preprocess template
        template_bgr = cv2.imread(template_path)
        if template_bgr is None:
            raise FileNotFoundError(f"Template not found: {template_path}")
        self.template_shape = template_bgr.shape
        self.template_gray  = preprocess(template_bgr, use_clahe=use_clahe)

        # Detector
        self.detector      = get_detector(self.detector_name, **detector_kwargs)
        self.desc_type     = descriptor_dtype(self.detector_name)

        # Compute template features once
        self.kp_template, self.des_template = \
            self.detector.detectAndCompute(self.template_gray, None)

        if self.des_template is None or len(self.kp_template) == 0:
            raise ValueError(
                f"No keypoints found in template '{template_path}'. "
                f"The template may lack sufficient texture for '{detector_name}'."
            )

        print(f"[Pipeline] Template '{os.path.basename(template_path)}': "
              f"{len(self.kp_template)} keypoints detected ({detector_name.upper()})")

    # ──────────────────────────────────────────
    # Per-frame processing
    # ──────────────────────────────────────────

    def process_frame(self, frame: np.ndarray) -> dict:
        """
        Detect and localize the template object in a single video frame.

        Parameters
        ----------
        frame : np.ndarray
            Raw BGR frame from the video.

        Returns
        -------
        dict with keys:
            'found'             : bool
            'corners'           : np.ndarray (4,1,2) or None
            'H'                 : np.ndarray (3x3) or None
            'inlier_count'      : int
            'num_good_matches'  : int
            'num_total_matches' : int
            'num_kp_frame'      : int
            'reason'            : str
        """
        # Step 1: preprocess frame (same as template)
        frame_gray = preprocess(frame, use_clahe=self.use_clahe)

        # Step 2: detect keypoints and descriptors in frame
        kp_frame, des_frame = self.detector.detectAndCompute(frame_gray, None)

        if des_frame is None or len(kp_frame) == 0:
            return {
                'found': False, 'corners': None, 'H': None,
                'inlier_count': 0, 'num_good_matches': 0,
                'num_total_matches': 0, 'num_kp_frame': 0,
                'reason': 'no_keypoints_in_frame'
            }

        # Step 3: match descriptors
        good_matches, total_matches = match_descriptors(
            self.des_template, des_frame,
            descriptor_type=self.desc_type,
            ratio=self.ratio,
            use_flann=self.use_flann
        )

        # Step 4+5+6: homography + validation + projection
        result = find_object(
            self.kp_template, kp_frame, good_matches,
            template_shape=self.template_shape,
            frame_shape=frame.shape,
            min_match_count=self.min_matches,
            ransac_thresh=self.ransac_thresh,
            min_inliers=self.min_inliers,
            min_area_ratio=self.min_area_ratio,
            max_area_ratio=self.max_area_ratio
        )

        result['num_good_matches']  = len(good_matches)
        result['num_total_matches'] = total_matches
        result['num_kp_frame']      = len(kp_frame)
        return result

    # ──────────────────────────────────────────
    # Video processing
    # ──────────────────────────────────────────

    def run_on_video(
        self,
        video_path:   str,
        output_path:  Optional[str] = None,
        draw:         bool = True,
        max_frames:   Optional[int] = None,
        show_live:    bool = False,
        verbose:      bool = True
    ) -> List[dict]:
        """
        Run the detection pipeline on every frame of a video.

        Parameters
        ----------
        video_path : str
            Path to the input video file.
        output_path : str or None
            If provided, write annotated video to this path.
        draw : bool
            Whether to draw bounding box and HUD on output frames.
        max_frames : int or None
            Stop after this many frames (useful for quick testing).
        show_live : bool
            Display frames in a window as they are processed (press 'q' to quit).
        verbose : bool
            Print progress every 30 frames and a summary at the end.

        Returns
        -------
        list of dict
            Per-frame result dicts (same structure as process_frame output).
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video: {video_path}")

        info   = get_video_info(video_path)
        fps    = info['fps'] or 30.0
        width  = info['width']
        height = info['height']

        writer = None
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            writer = create_video_writer(output_path, fps, width, height)

        results    = []
        frame_idx  = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if max_frames is not None and frame_idx >= max_frames:
                    break

                result = self.process_frame(frame)
                results.append(result)

                if draw or output_path or show_live:
                    vis = frame.copy()
                    if result['found'] and result['corners'] is not None:
                        vis = draw_bounding_box(vis, result['corners'])
                    if draw or show_live:
                        vis = draw_hud(
                            vis,
                            num_good_matches=result['num_good_matches'],
                            total_matches=result['num_total_matches'],
                            inlier_count=result['inlier_count'],
                            found=result['found'],
                            reason=result.get('reason', ''),
                            detector_name=self.detector_name
                        )
                    if writer:
                        writer.write(vis)
                    if show_live:
                        cv2.imshow('Object Detection', vis)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                else:
                    if writer:
                        writer.write(frame)

                if verbose and frame_idx % 30 == 0:
                    status = 'FOUND' if result['found'] else 'NOT FOUND'
                    print(f"  Frame {frame_idx:4d}: {status} | "
                          f"matches={result['num_good_matches']} | "
                          f"inliers={result['inlier_count']}")

                frame_idx += 1

        finally:
            cap.release()
            if writer:
                writer.release()
            if show_live:
                cv2.destroyAllWindows()

        # Summary
        summary = summarize_results(results)
        if verbose:
            print(f"\n[Summary] {video_path}")
            print(f"  Total frames    : {summary['total_frames']}")
            print(f"  Detected frames : {summary['detected_frames']}")
            print(f"  Detection rate  : {summary['detection_rate']*100:.1f}%")
            print(f"  Avg good matches: {summary['avg_good_matches']:.1f}")
            print(f"  Avg inliers     : {summary['avg_inliers']:.1f}")
            if output_path:
                print(f"  Output saved to : {output_path}")

        return results
