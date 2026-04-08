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
        'label'          : 'Spiral Notebook Cover (oo pplus) – Hand-held Frontal',
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
        'source'         : 'self-recorded',
        'difficulty_notes': 'Navy-blue spiral notebook cover ("oo pplus") held in hand against plain wall. '
                            'IoT/cloud icons and cityscape illustration provide rich SIFT keypoints. '
                            'Camera held steady with gentle tilt; flat surface, good contrast.',
        'detector_kwargs' : {}
    },

    'e2': {
        'category'       : 'easy',
        'label'          : 'Airbus A380 – Approaching Landing',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=d-p1UFcj14U&t=633s',
        'difficulty_notes': 'Airbus A380 filmed head-on against plain sky during final approach. '
                            'Aircraft underside has rich structural detail (engines, landing gear, wing edges). '
                            'Uniform sky background minimises false matches. '
                            'Object undergoes mild scale increase as plane approaches camera.',
        'detector_kwargs' : {}
    },

    'e3': {
        'category'       : 'easy',
        'label'          : 'Joker Playing Card – Overhead on Grey Surface',
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
        'source'         : 'self-recorded',
        'difficulty_notes': 'Joker card (rose illustration + portrait) placed on grey surface. '
                            'Fine-line artwork provides dense SIFT keypoints. '
                            'Neutral grey background has low texture so background keypoints are minimal. '
                            'Camera slightly overhead; flat rigid card makes homography exact.',
        'detector_kwargs' : {}
    },

    'e4': {
        'category'       : 'easy',
        'label'          : 'USB-C Hub (ADAN) – Static on White Background',
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
        'source'         : 'self-recorded',
        'difficulty_notes': 'Small USB-C hub (ADAN brand) on plain white background. '
                            'Metal chassis edges, logo text, and port openings supply stable keypoints. '
                            'White background produces almost no competing keypoints. '
                            'Camera position is near-constant; minimal scale or rotation change.',
        'detector_kwargs' : {}
    },

    'e5': {
        'category'       : 'easy',
        'label'          : 'Oreo Snack Wrapper – Hand-held Against White Background',
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
        'source'         : 'self-recorded',
        'difficulty_notes': 'Individual Oreo snack wrapper (Chinese packaging) held in hand against white background. '
                            'High-contrast blue wrapper with Oreo logo and Chinese text supplies rich keypoints. '
                            'White background prevents false matches from surroundings. '
                            'Slight hand movement introduces mild translation; wrapper surface remains flat.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # DIFFICULT SUCCESS CASES (d1 – d5)
    # ──────────────────────────────────────────
    # Pipeline still works but must overcome one challenging factor per case.
    # Tighter ratio (0.70) and more keypoints used.

    'd1': {
        'category'       : 'difficult',
        'label'          : 'Plaid Notebook – Partial Hand Occlusion on Wooden Table',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=DD7lU3S_jpY',
        'difficulty_notes': 'Blue plaid (grid-pattern) notebook held with both hands on wooden table. '
                            'Two challenges: (1) hands occlude ~30% of the notebook edges; '
                            '(2) wood-grain texture has horizontal lines similar to the plaid grid, '
                            'producing competing keypoints. Tighter ratio (0.70) rejects ambiguous '
                            'cross-surface matches; sufficient unoccluded keypoints survive for RANSAC.',
        'detector_kwargs' : {}
    },

    'd2': {
        'category'       : 'difficult',
        'label'          : 'Pigeons in Flight – Dynamic Cloudy Sky Background',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=wZVbPe5HVvg',
        'difficulty_notes': 'Two pigeons in flight against a changing cloudy sky. '
                            'Challenges: (1) shifting clouds generate spurious keypoints in the background; '
                            '(2) repetitive feather texture yields ambiguous descriptors; '
                            '(3) wing motion partially deforms the bird silhouette each frame. '
                            'CLAHE boosts contrast on the bird body against bright sky; '
                            'tighter ratio (0.70) suppresses cloud false-matches; '
                            'bird torso remains rigid enough for homography to hold.',
        'detector_kwargs' : {}
    },

    'd3': {
        'category'       : 'difficult',
        'label'          : 'White Cat in Dark Car Scene – Low Light & Cluttered Background',
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
        'source'         : 'YouTube: https://youtu.be/ZH7umQiTBlI?si=gX_j9VFGwV1NfnQ9',
        'difficulty_notes': 'White cat wearing a gold outfit filmed inside a dark car with two passengers. '
                            'Challenges: (1) very low ambient light suppresses gradient magnitudes; '
                            '(2) complex background (passengers, car interior) competes with cat features; '
                            '(3) white cat fur has low internal contrast (few keypoints on plain white areas). '
                            'CLAHE performs tile-level contrast stretching, recovering edges in dark regions; '
                            'gold outfit and face features provide discriminative keypoints; '
                            'relaxed ransac_thresh (6px) tolerates minor viewpoint change.',
        'detector_kwargs' : {}
    },

    'd4': {
        'category'       : 'difficult',
        'label'          : 'Sea Turtle Underwater – Color Cast & Coral Background Clutter',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=klK6mX8jnHQ',
        'difficulty_notes': 'Green sea turtle swimming above coral reef. '
                            'Challenges: (1) water introduces blue-green color cast and mild blur; '
                            '(2) textured coral background generates competing keypoints; '
                            '(3) turtle changes viewing angle as it swims, altering apparent shape. '
                            'SIFT operates on grayscale gradients so color cast has limited effect; '
                            'CLAHE recovers edge detail softened by water; '
                            'shell scutes and head features provide stable keypoints; '
                            'relaxed ransac_thresh (7px) accommodates perspective change from swimming motion.',
        'detector_kwargs' : {}
    },

    'd5': {
        'category'       : 'difficult',
        'label'          : 'Elephant Herd Crossing River – Similar-instance Confusion & Low Contrast',
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
        'source'         : 'Kaggle: https://www.kaggle.com/code/mistag/play-video-in-notebook/input',
        'difficulty_notes': 'Single elephant template; video shows a herd of elephants crossing a muddy river. '
                            'Challenges: (1) multiple elephants share identical gray texture and silhouette; '
                            '(2) elephant skin and muddy riverbank have similar gray-brown tone (low contrast boundary); '
                            '(3) water ripples and reflections add noisy keypoints near the legs. '
                            'Tighter ratio (0.70) reduces cross-individual false matches; '
                            'CLAHE enhances skin-fold edge detail; '
                            'RANSAC isolates the inlier cluster belonging to one elephant.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # EXPECTED FAIL CASES (f1 – f5)
    # ──────────────────────────────────────────
    # Objects/scenes that are fundamentally incompatible with feature-point
    # matching: non-rigid deformation, transparent/reflective surfaces,
    # dynamic crowds, or extreme background clutter.

    'f1': {
        'category'       : 'expected_fail',
        'label'          : 'Pedestrian on Busy Street – Non-rigid Moving Object & Background Dominance',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=YzcawvDGe4Y',
        'difficulty_notes': 'Template = single pedestrian (rear view, white top, brown trousers); '
                            'video = busy London street with many pedestrians and buildings. '
                            'Failure reasons: (1) person is non-rigid — arms swing, posture changes '
                            'every frame, violating homography planarity assumption; '
                            '(2) shop facades and signs behind the person produce far more stable '
                            'and numerous SIFT keypoints than clothing, so matcher locks onto '
                            'architecture instead of the target; '
                            '(3) other pedestrians with similar clothing frequently occlude the target. '
                            'Technique needed: person re-identification (deep appearance embedding) '
                            'or pose-estimation-based tracking.',
        'detector_kwargs' : {}
    },

    'f2': {
        'category'       : 'expected_fail',
        'label'          : 'White Van on Highway – Rapid 3D Perspective Change & Repetitive Road Background',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=nt3D26lrkho&t=22s',
        'difficulty_notes': 'Template = white delivery van (overhead bird-eye shot); '
                            'video = highway traffic filmed from an overpass (side/top view). '
                            'Failure reasons: (1) vehicles pass through the frame in 1–2 seconds, '
                            'providing too few frames for stable matching; '
                            '(2) multiple white vans and trucks look nearly identical — '
                            'descriptor matching cannot distinguish the target from lookalikes; '
                            '(3) road lane markings, barriers and trees create repetitive background '
                            'keypoints that overwhelm the few keypoints on the target vehicle; '
                            '(4) SIFT homography model cannot handle multiple independently moving vehicles. '
                            'Technique needed: multi-object tracking (e.g. SORT/DeepSORT) or '
                            'vehicle detector + re-ID.',
        'detector_kwargs' : {}
    },

    'f3': {
        'category'       : 'expected_fail',
        'label'          : 'EU Flag Waving – Non-rigid Surface Deformation',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=cAgyPg1gEPA',
        'difficulty_notes': 'Template = EU flag flat photo; video = EU flag waving in wind. '
                            'Failure reasons: (1) waving fabric undergoes continuous non-rigid '
                            'deformation — bending, folding and self-occlusion every frame; '
                            '(2) homography is a planar (2D projective) model; any non-planar '
                            'warp fundamentally violates this assumption; '
                            '(3) stars on the flag disappear behind folds and reappear in different '
                            'positions, breaking point correspondences; '
                            '(4) uniform blue sky background adds sparse but misleading keypoints. '
                            'The bounding box appears but is severely distorted and unstable. '
                            'Technique needed: thin-plate-spline or mesh-based non-rigid '
                            'registration; or texture-flow estimation.',
        'detector_kwargs' : {}
    },

    'f4': {
        'category'       : 'expected_fail',
        'label'          : 'Shark Underwater – Extreme Low Contrast & Camouflage',
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
        'source'         : 'YouTube: https://youtu.be/eoTpdTU8nTA?si=N3zjon83FwVY4fNC',
        'difficulty_notes': 'Template = shark in clear water (side view); '
                            'video = open ocean footage with divers and shark in deep blue water. '
                            'Failure reasons: (1) shark body blends completely into the blue water '
                            'background — gradient magnitude at object boundary is near zero '
                            '(counter-shading camouflage); '
                            '(2) deep water absorbs red/green wavelengths; both shark and background '
                            'become the same blue-grey tone in grayscale; '
                            '(3) SIFT finds keypoints on light caustic patterns on the sandy floor '
                            'and on divers rather than the shark itself; '
                            '(4) shark is non-rigid (tail undulation) and the body silhouette '
                            'changes with each stroke. No detection in any frame. '
                            'Technique needed: infrared or contrast-enhanced imaging; '
                            'silhouette-based shape matching; or underwater-specific detectors.',
        'detector_kwargs' : {}
    },

    'f5': {
        'category'       : 'expected_fail',
        'label'          : 'Smoke / Steam – Textureless Non-rigid Object',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=KEN6S2beTc0',
        'difficulty_notes': 'Template = white smoke/steam on black background; '
                            'video = white coffee/tea cup with steam rising on wooden table. '
                            'Failure reasons: (1) smoke and steam have no fixed texture — '
                            'they are purely amorphous gas with smoothly varying intensity gradients; '
                            '(2) SIFT requires repeatable keypoints at stable corners/blobs; '
                            'a smoke cloud has no such structure — detected keypoints shift '
                            'to a completely different location in every frame; '
                            '(3) smoke is fully non-rigid and transparent; '
                            'homography cannot model its deformation; '
                            '(4) template background (black) vs video background (wooden table) '
                            'creates a descriptor domain gap even if shape were stable. '
                            'Zero good matches in every frame. '
                            'Technique needed: optical flow / dense motion estimation; '
                            'temporal difference methods; or generative model of smoke appearance.',
        'detector_kwargs' : {}
    },

    # ──────────────────────────────────────────
    # UNEXPECTED FAIL CASES (u1 – u5)
    # ──────────────────────────────────────────
    # Objects that appear similar to easy cases but fail due to subtle factors.
    # These are the most instructive cases for the report discussion.

    'u1': {
        'category'       : 'unexpected_fail',
        'label'          : 'Gold Jewelry (Earring/Pendant) – Reflective Surface & 3D Viewpoint Change',
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
        'source'         : 'YouTube: https://youtube.com/shorts/hz8xmkeo8qU',
        'difficulty_notes': 'Gold ornamental earrings/pendant with purple-red gemstones and filigree metalwork. '
                            'Expected to succeed: intricate filigree and gemstone facets produce 1150+ '
                            'SIFT keypoints — the highest template keypoint count in this study. '
                            'Actually fails: (1) the highly reflective gold surface exhibits viewpoint-dependent '
                            'specular highlights — as the jewelry rotates in the video the bright spots '
                            'shift position entirely, altering gradient direction and magnitude at those '
                            'keypoint locations; '
                            '(2) the jewelry is a 3D object; any tilt reveals a completely different '
                            'arrangement of facets not seen in the 2D template, breaking descriptor '
                            'correspondence; '
                            '(3) homography assumes a planar surface — the convex dome of each gemstone '
                            'violates this assumption. Rich keypoints exist on the template but none '
                            'survive matching when the object rotates.',
        'detector_kwargs' : {}
    },

    'u2': {
        'category'       : 'unexpected_fail',
        'label'          : 'Orange Fruit – Smooth Curved Surface & Insufficient Gradient',
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
        'source'         : 'YouTube: https://youtu.be/GDk7Z9zkFws',
        'difficulty_notes': 'Single orange fruit against a plain background. '
                            'Expected to succeed: the dimpled peel texture appears visually rich '
                            'and the orange colour is highly distinctive. '
                            'Actually fails: (1) SIFT detects only 193 keypoints — far fewer than '
                            'expected — because the peel pores are gentle bumps with low gradient '
                            'magnitude, not sharp corners or blobs; '
                            '(2) the uniform orange hue means descriptors from any two peel regions '
                            'are nearly identical (repetitive texture), so ratio test rejects almost '
                            'every match as ambiguous; '
                            '(3) the orange is a convex 3D sphere — as it moves or rotates in the '
                            'video the visible surface patch changes completely, violating the planar '
                            'homography assumption; '
                            '(4) CLAHE has little effect because gradient information is genuinely '
                            'absent, not merely suppressed by poor contrast.',
        'detector_kwargs' : {}
    },

    'u3': {
        'category'       : 'unexpected_fail',
        'label'          : 'Clownfish (Nemo) – Non-rigid Swimming & Coral Background Dominance',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=RCOH9SD5obw&t=6744s',
        'difficulty_notes': 'Clownfish (Amphiprioninae) with distinctive orange/white/black stripe pattern. '
                            'Expected to succeed: the high-contrast stripe pattern yields 1293 SIFT keypoints '
                            '— keypoint density comparable to an easy case — and the colours are visually unique. '
                            'Actually fails: (1) the fish body is non-rigid; tail, fins and body flex with '
                            'every swimming stroke, deforming the stripe pattern in ways homography cannot model; '
                            '(2) the template background is plain black (isolated specimen photo) while '
                            'the video background is a densely textured coral reef — this descriptor '
                            'domain gap means matches from the coral far outnumber matches from the fish; '
                            '(3) underwater caustic light patterns on the reef surface produce additional '
                            'time-varying keypoints that overwhelm the few stable matches on the fish body; '
                            '(4) other reef fish with similar colouring cause further instance confusion.',
        'detector_kwargs' : {}
    },

    'u4': {
        'category'       : 'unexpected_fail',
        'label'          : 'Ink Dissolving in Water – Non-rigid Morphing & No Stable Texture',
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
        'source'         : 'YouTube: https://www.youtube.com/watch?v=pGbIOC83-So',
        'difficulty_notes': 'Blue ink or paint droplet dissolving and diffusing in water, '
                            'forming a complex cloud-like blob against a white background. '
                            'Expected to succeed: the ink cloud has complex branching structure '
                            'and SIFT detects 822 keypoints on it — a seemingly sufficient count '
                            'and higher than several successful cases. '
                            'Actually fails: (1) the ink cloud is a fully non-rigid fluid — its '
                            'shape, density, and internal texture change continuously every frame '
                            'as convection currents disperse the pigment; '
                            '(2) although 822 keypoints are detected on the static template, none '
                            'of these keypoints correspond to any stable or repeatable structure — '
                            'the "texture" is an instantaneous snapshot of a transient fluid state; '
                            '(3) this is conceptually similar to the smoke/steam expected-fail case (f5) '
                            'but visually deceptive because the blob appears richer and more structured; '
                            '(4) RANSAC cannot find even a minimal inlier set because no correspondence '
                            'between template frame and video frame is geometrically consistent.',
        'detector_kwargs' : {}
    },

    'u5': {
        'category'       : 'unexpected_fail',
        'label'          : 'Ant – Reflective Exoskeleton, Non-rigid Motion & Tiny Scale',
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
        'source'         : 'YouTube: https://youtu.be/AKQkuNifoas',
        'difficulty_notes': 'Single ant (Formicidae) on a plain white background. '
                            'Expected to succeed: the ant has a clearly segmented body (head, thorax, '
                            'abdomen) with distinct boundaries and 236 SIFT keypoints — sufficient '
                            'for many successful cases in this study. '
                            'Actually fails: (1) the ant exoskeleton is highly reflective (chitinous '
                            'shell) — specular highlights on the head and abdomen shift completely '
                            'with any change in lighting angle or camera position, changing descriptors '
                            'at those locations; '
                            '(2) the ant is non-rigid — six legs, antennae, and the gaster (abdomen) '
                            'move independently and continuously, so no single homography can model '
                            'the full body deformation; '
                            '(3) the ant is small relative to the frame; at reduced scale the template '
                            'region is tiny, making individual descriptor patches cover a larger '
                            'proportion of the object and become highly sensitive to any motion; '
                            '(4) the natural terrain background (soil, leaf litter) in the video '
                            'introduces competing textured keypoints that outnumber the ant\'s own features.',
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
