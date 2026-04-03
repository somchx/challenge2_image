"""
run_all.py
----------
Batch runner: process all 20 cases and write a summary CSV.

Usage:
    python run_all.py [--category CATEGORY] [--max-frames N] [--skip-missing]

Examples:
    python run_all.py                         # all 20 cases
    python run_all.py --category easy         # only e1–e5
    python run_all.py --max-frames 60         # quick test, 60 frames per video
    python run_all.py --skip-missing          # skip cases with missing files
"""

import sys
import os
import csv
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cases_config import CASES, get_cases_by_category
from src.pipeline import ObjectDetectionPipeline
from src.utils    import summarize_results


VALID_CATEGORIES = ['easy', 'difficult', 'expected_fail', 'unexpected_fail']


def parse_args():
    parser = argparse.ArgumentParser(description='Batch object detection runner')
    parser.add_argument('--category', type=str, default=None,
                        choices=VALID_CATEGORIES + [None],
                        help='Process only cases in this category')
    parser.add_argument('--max-frames', type=int, default=None,
                        help='Max frames per video (for quick testing)')
    parser.add_argument('--skip-missing', action='store_true',
                        help='Skip cases where template or video is missing')
    return parser.parse_args()


def run_single_case(case_id: str, case: dict, max_frames=None) -> dict:
    """Run one case and return a summary row dict."""
    row = {
        'case_id'          : case_id,
        'category'         : case['category'],
        'label'            : case['label'],
        'detector'         : case['detector'],
        'ratio'            : case['ratio'],
        'expected_outcome' : case['expected_outcome'],
        'actual_outcome'   : 'error',
        'detection_rate'   : 0.0,
        'detected_frames'  : 0,
        'total_frames'     : 0,
        'avg_good_matches' : 0.0,
        'avg_inliers'      : 0.0,
        'match_expected'   : False,
        'elapsed_sec'      : 0.0,
        'notes'            : ''
    }

    # File existence check
    for key, label in [('template', 'Template'), ('video', 'Video')]:
        if not os.path.exists(case[key]):
            row['notes'] = f'{label} missing: {case[key]}'
            row['actual_outcome'] = 'skipped'
            return row

    t0 = time.time()
    try:
        pipeline = ObjectDetectionPipeline(
            template_path = case['template'],
            detector_name = case['detector'],
            ratio         = case['ratio'],
            min_matches   = case['min_matches'],
            min_inliers   = case['min_inliers'],
            ransac_thresh = case['ransac_thresh'],
            use_clahe     = case['use_clahe'],
            **case.get('detector_kwargs', {})
        )

        results = pipeline.run_on_video(
            video_path  = case['video'],
            output_path = case['output'],
            draw        = True,
            max_frames  = max_frames,
            show_live   = False,
            verbose     = False
        )

        summary = summarize_results(results)
        detection_rate = summary['detection_rate']
        actual_outcome = 'success' if detection_rate >= 0.4 else 'fail'

        row.update({
            'actual_outcome'   : actual_outcome,
            'detection_rate'   : round(detection_rate, 4),
            'detected_frames'  : summary['detected_frames'],
            'total_frames'     : summary['total_frames'],
            'avg_good_matches' : round(summary['avg_good_matches'], 2),
            'avg_inliers'      : round(summary['avg_inliers'], 2),
            'match_expected'   : actual_outcome == case['expected_outcome'],
            'elapsed_sec'      : round(time.time() - t0, 1),
        })

    except Exception as exc:
        row['notes'] = str(exc)
        row['elapsed_sec'] = round(time.time() - t0, 1)

    return row


def main():
    args = parse_args()

    # Select cases to run
    if args.category:
        cases_to_run = get_cases_by_category(args.category)
    else:
        cases_to_run = CASES

    print(f"\n{'='*70}")
    print(f"Challenge 2 – Batch Object Detection")
    print(f"Running {len(cases_to_run)} case(s)"
          + (f" [{args.category}]" if args.category else ""))
    if args.max_frames:
        print(f"  (limited to {args.max_frames} frames per video for testing)")
    print(f"{'='*70}\n")

    rows = []
    for case_id, case in sorted(cases_to_run.items()):
        # Check for missing files
        template_ok = os.path.exists(case['template'])
        video_ok    = os.path.exists(case['video'])

        if not template_ok or not video_ok:
            if args.skip_missing:
                print(f"[SKIP] {case_id}: missing {'template' if not template_ok else 'video'}")
                rows.append({
                    'case_id': case_id, 'category': case['category'],
                    'label': case['label'], 'actual_outcome': 'skipped',
                    'expected_outcome': case['expected_outcome'],
                    'notes': f"missing: {'template' if not template_ok else 'video'}"
                })
                continue
            else:
                print(f"[MISSING] {case_id}: {'template' if not template_ok else 'video'} not found.")
                print(f"  Template: {case['template']}")
                print(f"  Video   : {case['video']}")
                print(f"  Run with --skip-missing to continue anyway.\n")
                rows.append(run_single_case(case_id, case, max_frames=args.max_frames))
                continue

        print(f"[{case_id.upper()}] {case['label']}")
        row = run_single_case(case_id, case, max_frames=args.max_frames)
        rows.append(row)

        # One-line result
        match_mark = '✓' if row.get('match_expected') else '✗'
        print(f"  {match_mark} {row['actual_outcome'].upper()} "
              f"(rate={row.get('detection_rate', 0)*100:.1f}%, "
              f"matches={row.get('avg_good_matches', 0):.0f}, "
              f"inliers={row.get('avg_inliers', 0):.0f}, "
              f"t={row.get('elapsed_sec', 0):.1f}s)")
        if row.get('notes'):
            print(f"  Note: {row['notes']}")
        print()

    # Write CSV
    csv_path = 'results_summary.csv'
    fieldnames = [
        'case_id', 'category', 'label', 'detector', 'ratio',
        'expected_outcome', 'actual_outcome', 'match_expected',
        'detection_rate', 'detected_frames', 'total_frames',
        'avg_good_matches', 'avg_inliers', 'elapsed_sec', 'notes'
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

    # Print summary table
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'─'*70}")
    print(f"{'ID':<6} {'Category':<18} {'Expected':<10} {'Actual':<10} {'Rate':>6}  {'Match'}")
    print(f"{'─'*70}")
    for row in rows:
        mark = '✓' if row.get('match_expected') else '✗'
        rate = f"{row.get('detection_rate', 0)*100:.0f}%"
        print(f"{row['case_id']:<6} {row['category']:<18} "
              f"{row.get('expected_outcome','?'):<10} {row.get('actual_outcome','?'):<10} "
              f"{rate:>6}  {mark}")
    print(f"{'─'*70}")

    # Count matches
    valid_rows = [r for r in rows if r.get('actual_outcome') not in ('skipped', 'error')]
    matches    = sum(1 for r in valid_rows if r.get('match_expected'))
    print(f"Matched expected outcome: {matches}/{len(valid_rows)}")
    print(f"\nResults saved to: {csv_path}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
