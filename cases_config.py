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
        'label'          : 'Plaid Notebook on Wooden Table – Texture Confusion',
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
        'difficulty_notes': 'Plaid (grid-pattern) notebook on a wooden table. '
                            'Expected to succeed: high-contrast blue grid lines on the notebook '
                            'produce sharp edges and corner-like intersections that detectors favour. '
                            'Actually fails: the wooden table also has high-frequency line texture '
                            '(wood grain) whose SIFT descriptors are mathematically similar to the '
                            'notebook grid. The matcher produces massive numbers of cross-surface '
                            'outliers; RANSAC cannot separate them, so the computed homography is '
                            'wildly wrong or fails validation.',
        'detector_kwargs' : {}
    },

    'u2': {
        'category'       : 'unexpected_fail',
        'label'          : 'Oreo Wrapper – Shadow-induced Feature Distortion',
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
        'difficulty_notes': 'Oreo snack wrapper on a white background. '
                            'Expected to succeed: deep navy blue wrapper against bright white '
                            'background gives 100% contrast; the Oreo logo is a highly unique pattern. '
                            'Actually fails: cast shadows cross the wrapper during the video, '
                            'locally altering the gradient magnitude and direction. '
                            'Keypoints that existed in the shadow-free template either disappear '
                            'or shift in descriptor space, causing match failure in shadowed frames.',
        'detector_kwargs' : {}
    },

    'u3': {
        'category'       : 'unexpected_fail',
        'label'          : 'Playing Card on Dark Cloth – Background Feature Dominance',
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
        'difficulty_notes': 'Playing card placed on dark-gray cloth. '
                            'Expected to succeed: bright white card on dark background creates '
                            'extreme value contrast, making object boundaries easy to isolate. '
                            'Actually fails: the cloth has wrinkles and fabric texture that '
                            'generate more keypoints than the largely white, low-information card face. '
                            'The detector prioritises background features; the bounding box jumps '
                            'across the cloth wrinkles rather than tracking the card.',
        'detector_kwargs' : {}
    },

    'u4': {
        'category'       : 'unexpected_fail',
        'label'          : 'Penguin on Snow – Background Clutter Over-segmentation',
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
        'difficulty_notes': 'Single penguin template; video shows the same penguin among rocks '
                            'and a group of other penguins against snow. '
                            'Expected to succeed: black penguin on white snow is near-binary contrast. '
                            'Actually fails: other penguins and dark rocks share the same black/white '
                            'texture signature as the template. The matcher finds inliers scattered '
                            'across multiple penguins and rocks; RANSAC forms a homography that '
                            'covers the whole group, producing an over-expanded bounding box that '
                            'engulfs unrelated objects.',
        'detector_kwargs' : {}
    },

    'u5': {
        'category'       : 'unexpected_fail',
        'label'          : 'Elephant Herd Crossing River – Low Contrast Camouflage',
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
        'difficulty_notes': 'Herd of elephants crossing a river. '
                            'Expected to succeed: elephants are large with distinctive silhouettes; '
                            'skin folds and shadows should create detectable features. '
                            'Actually fails: elephant skin and riverbank mud share the same '
                            'gray/brown tone (low contrast camouflage). The detector cannot extract '
                            'stable edges or corners at the object boundary because pixel gradients '
                            'are negligible. Descriptors from skin wrinkles on the template match '
                            'spuriously with similar-looking mud/rock texture in the video, '
                            'causing severe mismatch or complete detection failure.',
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
