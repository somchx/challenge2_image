"""
run_case.py
-----------
Run the object detection pipeline on a single case.

Usage:
    python run_case.py <case_id> [--show] [--no-output] [--max-frames N]

Examples:
    python run_case.py e1
    python run_case.py d3 --show
    python run_case.py f1 --no-output --max-frames 60
    python run_case.py u4 --show

Arguments:
    case_id      : One of e1–e5, d1–d5, f1–f5, u1–u5
    --show       : Display annotated video in a window (press 'q' to quit)
    --no-output  : Do not write output video file (useful for quick testing)
    --max-frames : Stop after N frames
"""

import sys
import os
import argparse

# Allow running from project root without installing as package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cases_config import get_case
from src.pipeline import ObjectDetectionPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description='Object Detection – single case runner'
    )
    parser.add_argument('case_id', type=str,
                        help='Case ID (e.g., e1, d3, f2, u5)')
    parser.add_argument('--show', action='store_true',
                        help='Display output video live (cv2.imshow)')
    parser.add_argument('--no-output', action='store_true',
                        help='Skip writing output video')
    parser.add_argument('--max-frames', type=int, default=None,
                        help='Process at most N frames')
    return parser.parse_args()


def main():
    args = parse_args()

    # Load case configuration
    try:
        case = get_case(args.case_id)
    except KeyError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Case   : {args.case_id.upper()} – {case['label']}")
    print(f"Category: {case['category']}")
    print(f"Expected: {case['expected_outcome'].upper()}")
    print(f"Template: {case['template']}")
    print(f"Video  : {case['video']}")
    print(f"{'='*60}\n")

    # Verify files exist
    if not os.path.exists(case['template']):
        print(f"ERROR: Template not found: {case['template']}")
        print("  -> Place the template image at the path above.")
        sys.exit(1)
    if not os.path.exists(case['video']):
        print(f"ERROR: Video not found: {case['video']}")
        print("  -> Place the input video at the path above.")
        sys.exit(1)

    # Build pipeline
    pipeline = ObjectDetectionPipeline(
        template_path  = case['template'],
        detector_name  = case['detector'],
        ratio          = case['ratio'],
        min_matches    = case['min_matches'],
        min_inliers    = case['min_inliers'],
        ransac_thresh  = case['ransac_thresh'],
        use_clahe      = case['use_clahe'],
        **case.get('detector_kwargs', {})
    )

    # Determine output path
    output_path = None if args.no_output else case['output']

    # Run
    results = pipeline.run_on_video(
        video_path  = case['video'],
        output_path = output_path,
        draw        = True,
        max_frames  = args.max_frames,
        show_live   = args.show,
        verbose     = True
    )

    # Final assessment
    detection_rate = sum(1 for r in results if r['found']) / max(len(results), 1)
    actual_outcome = 'success' if detection_rate >= 0.4 else 'fail'
    match_expected = (actual_outcome == case['expected_outcome'])

    print(f"\n{'─'*60}")
    print(f"RESULT  : {actual_outcome.upper()} (detection rate {detection_rate*100:.1f}%)")
    print(f"Expected: {case['expected_outcome'].upper()}")
    print(f"Match   : {'✓ AS EXPECTED' if match_expected else '✗ UNEXPECTED'}")
    print(f"{'─'*60}\n")


if __name__ == '__main__':
    main()
