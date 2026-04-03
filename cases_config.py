"""
cases_config.py
---------------
Central configuration for all 20 test cases.

Categories:
  e1–e5 : Easy Success        (5 cases)
  d1–d5 : Difficult Success   (5 cases)
  f1–f5 : Expected Fail       (5 cases)
  u1–u5 : Unexpected Fail     (5 cases)

Each entry has:
  category       : 'easy' | 'difficult' | 'expected_fail' | 'unexpected_fail'
  label          : Human-readable description
  template       : Path to template image (relative to project root)
  video          : Path to input video
  output         : Path to write annotated output video
  detector       : 'sift' | 'orb' | 'akaze'
  ratio          : Lowe's ratio threshold (0.70–0.80)
  min_matches    : Minimum good matches for homography attempt
  min_inliers    : Minimum RANSAC inliers for valid detection
  ransac_thresh  : RANSAC reprojection threshold (pixels)
  use_clahe      : Whether to apply CLAHE preprocessing
  expected_outcome: 'success' | 'fail'
  difficulty_notes: Brief description of challenging factor (or failure mode)
  detector_kwargs: Extra kwargs passed to detector constructor

INSTRUCTIONS FOR POPULATING:
  1. Place template images in templates/<category>/ and name them as below.
  2. Place input videos   in videos/<category>/    and name them as below.
  3. Run: python run_case.py <case_id>     (single case)
     Or:  python run_all.py               (all 20 cases)
"""

CASES = {

    # ──────────────────────────────────────────
    # EASY SUCCESS CASES (e1 – e5)
    # ──────────────────────────────────────────
    # High-texture flat objects, good lighting, minimal motion.
    # SIFT finds 500+ keypoints on template; hundreds of matches per frame.

    'e1': {
        'category'       : 'easy',
        'label'          : 'Book Cover – Frontal Steady',
        'template'       : 'templates/easy/template_e1.jpg',
        'video'          : 'videos/easy/video_e1.mp4',
        'output'         : 'outputs/easy/output_e1.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'High-texture flat object (book cover). SIFT finds many stable keypoints. '
                            'Camera held steady; gentle 5–10° tilt over 10 seconds.',
        'detector_kwargs' : {}
    },

    'e2': {
        'category'       : 'easy',
        'label'          : 'Printed A4 Poster – Slow Pan',
        'template'       : 'templates/easy/template_e2.jpg',
        'video'          : 'videos/easy/video_e2.mp4',
        'output'         : 'outputs/easy/output_e2.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Colorful printed poster pinned to a neutral wall. '
                            'Slow horizontal camera pan. Dense print = extreme keypoint density.',
        'detector_kwargs' : {}
    },

    'e3': {
        'category'       : 'easy',
        'label'          : 'Cereal Box Front – Static Camera',
        'template'       : 'templates/easy/template_e3.jpg',
        'video'          : 'videos/easy/video_e3.mp4',
        'output'         : 'outputs/easy/output_e3.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Cereal box on table, camera overhead slightly tilted, static 15 s clip. '
                            'Logo, text, and cartoon art provide hundreds of SIFT keypoints.',
        'detector_kwargs' : {}
    },

    'e4': {
        'category'       : 'easy',
        'label'          : 'Magazine Cover – Frontal, Well-lit',
        'template'       : 'templates/easy/template_e4.jpg',
        'video'          : 'videos/easy/video_e4.mp4',
        'output'         : 'outputs/easy/output_e4.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Magazine cover with rich typography and imagery. '
                            'Camera slowly zooms in and out (mild scale change, well within SIFT range).',
        'detector_kwargs' : {}
    },

    'e5': {
        'category'       : 'easy',
        'label'          : 'Playing Card (Face Card) – Overhead',
        'template'       : 'templates/easy/template_e5.jpg',
        'video'          : 'videos/easy/video_e5.mp4',
        'output'         : 'outputs/easy/output_e5.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Face playing card (Jack/Queen/King) on white table. '
                            'Camera slowly approaches and retreats (scale change). '
                            'Card art contains fine detail ideal for SIFT.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # DIFFICULT SUCCESS CASES (d1 – d5)
    # ──────────────────────────────────────────
    # Pipeline still works but must overcome one challenging factor per case.
    # Tighter ratio (0.70) and more keypoints used.

    'd1': {
        'category'       : 'difficult',
        'label'          : 'Book Cover – 35% Hand Occlusion',
        'template'       : 'templates/difficult/template_d1.jpg',
        'video'          : 'videos/difficult/video_d1.mp4',
        'output'         : 'outputs/difficult/output_d1.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.70,
        'min_matches'    : 8,
        'min_inliers'    : 6,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Same book cover template. Person holds book with ~35% of cover '
                            'hidden behind hand. Remaining visible keypoints must be sufficient '
                            'for RANSAC. Tighter ratio (0.70) rejects ambiguous matches.',
        'detector_kwargs' : {}
    },

    'd2': {
        'category'       : 'difficult',
        'label'          : 'Poster – Warm/Yellow Illumination Shift',
        'template'       : 'templates/difficult/template_d2.jpg',
        'video'          : 'videos/difficult/video_d2.mp4',
        'output'         : 'outputs/difficult/output_d2.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.70,
        'min_matches'    : 8,
        'min_inliers'    : 6,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Poster photographed under neutral white light for template. '
                            'Video filmed under warm incandescent light (color temperature shift). '
                            'SIFT uses grayscale gradients so color shift is tolerated; CLAHE '
                            'compensates for contrast changes.',
        'detector_kwargs' : {}
    },

    'd3': {
        'category'       : 'difficult',
        'label'          : 'Cereal Box – Large Viewing Angle (50–60°)',
        'template'       : 'templates/difficult/template_d3.jpg',
        'video'          : 'videos/difficult/video_d3.mp4',
        'output'         : 'outputs/difficult/output_d3.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.70,
        'min_matches'    : 8,
        'min_inliers'    : 6,
        'ransac_thresh'  : 6.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Camera rotates around the cereal box, reaching 50–60° viewing angle. '
                            'Homography is a planar approximation; at large angles it degrades but '
                            'enough inliers survive for detection. Relaxed ransac_thresh (6px).',
        'detector_kwargs' : {}
    },

    'd4': {
        'category'       : 'difficult',
        'label'          : 'Textbook – Slight Spine Bend (Non-planar)',
        'template'       : 'templates/difficult/template_d4.jpg',
        'video'          : 'videos/difficult/video_d4.mp4',
        'output'         : 'outputs/difficult/output_d4.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.70,
        'min_matches'    : 8,
        'min_inliers'    : 6,
        'ransac_thresh'  : 7.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'Textbook bent gently (~15–20° flex along spine). Introduces slight '
                            'non-planar deformation. Homography approximates the curved surface '
                            'as a plane; mild flex still produces enough inliers. Relaxed '
                            'ransac_thresh (7px) accommodates local deviation from planarity.',
        'detector_kwargs' : {}
    },

    'd5': {
        'category'       : 'difficult',
        'label'          : 'CD/DVD Label – Slight Glare from Reflection',
        'template'       : 'templates/difficult/template_d5.jpg',
        'video'          : 'videos/difficult/video_d5.mp4',
        'output'         : 'outputs/difficult/output_d5.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.70,
        'min_matches'    : 8,
        'min_inliers'    : 6,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'success',
        'difficulty_notes': 'CD/DVD printed label side. Filmed flat on table at slight angle '
                            'with minor specular reflection glare. CLAHE reduces the impact '
                            'of local overexposure; printed label area still yields stable keypoints.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # EXPECTED FAIL CASES (f1 – f5)
    # ──────────────────────────────────────────
    # The template object has no distinguishable feature points.
    # SIFT/ORB find very few keypoints on the template; matching is impossible.

    'f1': {
        'category'       : 'expected_fail',
        'label'          : 'Plain White Wall – No Texture',
        'template'       : 'templates/expected_fail/template_f1.jpg',
        'video'          : 'videos/expected_fail/video_f1.mp4',
        'output'         : 'outputs/expected_fail/output_f1.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Template = photo of a plain white wall. Near-zero gradient → '
                            'SIFT finds almost no keypoints. No matches possible regardless '
                            'of scene. Expected to fail because feature-point methods require texture.',
        'detector_kwargs' : {}
    },

    'f2': {
        'category'       : 'expected_fail',
        'label'          : 'Solid-color T-shirt – No Features',
        'template'       : 'templates/expected_fail/template_f2.jpg',
        'video'          : 'videos/expected_fail/video_f2.mp4',
        'output'         : 'outputs/expected_fail/output_f2.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Uniform-color cotton T-shirt (no print/logo). '
                            'Fabric has no local gradient structure → no keypoints on template. '
                            'Feature matching is fundamentally inapplicable here.',
        'detector_kwargs' : {}
    },

    'f3': {
        'category'       : 'expected_fail',
        'label'          : 'Blank Notebook Cover – Smooth, Featureless',
        'template'       : 'templates/expected_fail/template_f3.jpg',
        'video'          : 'videos/expected_fail/video_f3.mp4',
        'output'         : 'outputs/expected_fail/output_f3.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Plain notebook cover, single flat color, no embossing or print. '
                            'Smooth surface → no corners or blobs for SIFT/ORB. '
                            'Keypoint count on template expected to be 0–5.',
        'detector_kwargs' : {}
    },

    'f4': {
        'category'       : 'expected_fail',
        'label'          : 'Clear Glass Bottle – Transparent, View-dependent',
        'template'       : 'templates/expected_fail/template_f4.jpg',
        'video'          : 'videos/expected_fail/video_f4.mp4',
        'output'         : 'outputs/expected_fail/output_f4.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Clear glass water bottle. The "features" detected on the template '
                            'belong to the background visible through the glass, not the bottle '
                            'itself. When the background changes between template and video, '
                            'these features do not match. Transparent objects are a known '
                            'failure mode for appearance-based methods.',
        'detector_kwargs' : {}
    },

    'f5': {
        'category'       : 'expected_fail',
        'label'          : 'Uniform Carpet Patch – No Distinct Pattern',
        'template'       : 'templates/expected_fail/template_f5.jpg',
        'video'          : 'videos/expected_fail/video_f5.mp4',
        'output'         : 'outputs/expected_fail/output_f5.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Patch of plain carpet or floor tile. Uniform or near-uniform texture '
                            'yields no stable keypoints with unique descriptors. Any apparent '
                            'keypoints are unstable across viewpoints.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # UNEXPECTED FAIL CASES (u1 – u5)
    # ──────────────────────────────────────────
    # Objects that appear similar to easy cases but fail due to subtle factors.
    # These are the most instructive cases for the report discussion.

    'u1': {
        'category'       : 'unexpected_fail',
        'label'          : 'Book Cover – Severe Motion Blur',
        'template'       : 'templates/unexpected_fail/template_u1.jpg',
        'video'          : 'videos/unexpected_fail/video_u1.mp4',
        'output'         : 'outputs/unexpected_fail/output_u1.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Same book cover as an easy case. Camera is waved quickly — '
                            'fast panning motion causes severe motion blur on most frames. '
                            'Blur smears keypoints; SIFT detects far fewer stable points '
                            'in blurred frames, dropping below min_matches threshold. '
                            'Expected to succeed (same object as easy case) but fails due to blur.',
        'detector_kwargs' : {}
    },

    'u2': {
        'category'       : 'unexpected_fail',
        'label'          : 'Poster – Sudden Lights Off Mid-Video',
        'template'       : 'templates/unexpected_fail/template_u2.jpg',
        'video'          : 'videos/unexpected_fail/video_u2.mp4',
        'output'         : 'outputs/unexpected_fail/output_u2.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Poster template photographed under good lighting. '
                            'Video starts well (detection works), then mid-video room light is '
                            'switched off and only dim ambient/phone light remains. '
                            'Severe underexposure destroys gradient information. '
                            'Detection fails for all dark frames despite object still being present.',
        'detector_kwargs' : {}
    },

    'u3': {
        'category'       : 'unexpected_fail',
        'label'          : 'Tiny Logo Crop – Template Too Small',
        'template'       : 'templates/unexpected_fail/template_u3.jpg',
        'video'          : 'videos/unexpected_fail/video_u3.mp4',
        'output'         : 'outputs/unexpected_fail/output_u3.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Template is a very tightly cropped small logo (~80×80 px) from a '
                            'larger product. Video shows the full product from normal distance. '
                            'The template has too few pixels → very few SIFT keypoints. '
                            'In the video, the logo region is tiny relative to the frame, '
                            'making reliable homography estimation impossible. '
                            'Surprise: the same product in an easy case succeeds with full-frame template.',
        'detector_kwargs' : {}
    },

    'u4': {
        'category'       : 'unexpected_fail',
        'label'          : 'Brick Wall – Repetitive Texture Confusion',
        'template'       : 'templates/unexpected_fail/template_u4.jpg',
        'video'          : 'videos/unexpected_fail/video_u4.mp4',
        'output'         : 'outputs/unexpected_fail/output_u4.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Template = close-up of a brick wall section (looks textured, should work). '
                            'Video = camera pans over the same wall. '
                            'Repetitive regular pattern confuses the matcher: many bricks look '
                            'near-identical, so ratio test passes spuriously with wrong correspondences. '
                            'RANSAC receives many inliers but they map to the wrong brick, '
                            'producing a degenerate or incorrect homography that fails validation. '
                            'Surprise: the template has detectable keypoints, so naive inspection '
                            'suggests it should work.',
        'detector_kwargs' : {}
    },

    'u5': {
        'category'       : 'unexpected_fail',
        'label'          : 'Phone Back / Mirror – View-dependent Reflections',
        'template'       : 'templates/unexpected_fail/template_u5.jpg',
        'video'          : 'videos/unexpected_fail/video_u5.mp4',
        'output'         : 'outputs/unexpected_fail/output_u5.mp4',
        'detector'       : 'sift',
        'ratio'          : 0.75,
        'min_matches'    : 10,
        'min_inliers'    : 8,
        'ransac_thresh'  : 5.0,
        'use_clahe'      : True,
        'expected_outcome': 'fail',
        'difficulty_notes': 'Template = photo of a polished phone back / small mirror from one angle. '
                            'Video = camera moves slightly around the same surface. '
                            'The "features" detected on the shiny surface are reflections of '
                            'the surrounding environment, which change completely with viewpoint. '
                            'Template and frame descriptors do not match because the reflected '
                            'image is different. Breaks the appearance constancy assumption. '
                            'Surprise: the surface has detectable features in both template and '
                            'video, but they correspond to different reflected content.',
        'detector_kwargs' : {}
    },
}


# ──────────────────────────────────────────────
# Helper accessors
# ──────────────────────────────────────────────

def get_case(case_id: str) -> dict:
    if case_id not in CASES:
        valid = ', '.join(sorted(CASES.keys()))
        raise KeyError(f"Unknown case '{case_id}'. Valid IDs: {valid}")
    return CASES[case_id]


def get_cases_by_category(category: str) -> dict:
    return {k: v for k, v in CASES.items() if v['category'] == category}


def all_case_ids() -> list:
    return sorted(CASES.keys())
