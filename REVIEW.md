# SPEC Compliance Review

1. [PASS] **Initial Load – empty square window spanning -1 to 1**: Canvas initializes with no particles (`appState.particles = []`) and square rendering region maps simulation coordinates in `[-1, 1]^2` to canvas space (`index.html:560-563`, `index.html:817-821`, `index.html:1413-1420`).
2. [FAIL] **Initial Load – axes labeled similar to matplotlib plots**: Only two `1.0` labels are rendered; `-1` labels/ticks are missing, so the displayed axis labeling is incomplete (`index.html:424-425`).
3. [WARN] **Initial Load – all controls present and functional upon load**: Controls are present, but at least one feature behind a control (Volume RSD checkbox) is broken by a backend bug when used (`index.html:403-547`, `app.py:568-570`).
4. [PASS] **Initial Load – default parameters s=3, k=6, n=200, maxstep=0.02, noise=0**: Defaults match spec in UI state and inputs (`index.html:464`, `index.html:477`, `index.html:490`, `index.html:499`, `index.html:512`, `index.html:565-569`).
5. [PASS] **Initial Load – default density distribution is uniform**: Uniform option is marked active and `appState.densityType` defaults to `"uniform"` (`index.html:527-529`, `index.html:572`).
6. [PASS] **Initial Load – pause/play starts paused**: `isPlaying` starts false and button starts in paused style/text (`index.html:443`, `index.html:576`, `index.html:1092-1095`).
7. [PASS] **Initial Load – statistics checkboxes unchecked by default**: Neither checkbox has `checked` set, and internal flags default to false (`index.html:406`, `index.html:411`, `index.html:588-590`).
8. [PASS] **Initial Load – FPS target defaults to 30**: Input and state both initialize to 30 (`index.html:434`, `index.html:580`).
9. [PASS] **Initial Load – point tool defaults to ‘x’/none**: None button is active and initialization sets tool to `null` (`index.html:449`, `index.html:1420`).

10. [PASS] **s parameter – default slider range 0 to 10**: `sSlider` is initialized with min 0 and max 10 (`index.html:466`).
11. [PASS] **s parameter – text box accepts real numbers**: Numeric input with decimal step and `parseFloat` synchronization supports real values (`index.html:464`, `index.html:893-896`).
12. [PASS] **s parameter – bidirectional sync between textbox and slider**: Input updates slider and slider updates input (`index.html:892-912`, `index.html:1222-1226`).
13. [PASS] **s parameter – slider bounds manually editable**: Min/max bound inputs exist and update slider bounds on change (`index.html:468-469`, `index.html:1227-1245`).
14. [PASS] **s parameter – bounds only accepted when left < right**: Bound update logic enforces strict inequality (`index.html:1230-1235`, `index.html:1240-1245`).
15. [WARN] **s parameter – out-of-range text updates bounds/extreme behavior**: Bounds are expanded, but new bound may be floored/ceiled rather than exactly the entered value (e.g., `-5.2` becomes `-6`) (`index.html:898-905`).
16. [PASS] **s parameter – changing s immediately affects motion when unpaused**: Current `s` is sent on every simulation step request (`index.html:1116-1123`).

17. [WARN] **k parameter – text box accepts only positive integer inputs**: UI uses integer parsing, but decimal input is truncated (e.g., `2.8 -> 2`) rather than explicitly rejected (`index.html:477`, `index.html:929-934`).
18. [PASS] **k parameter – slider quantized to positive integer steps**: Slider has `step="1"` and min `1` (`index.html:479`).
19. [PASS] **k parameter – text box and slider stay synchronized**: Sync functions update both controls from state (`index.html:926-936`, `index.html:941-945`, `index.html:1262-1266`).
20. [FAIL] **k parameter – if k > n, treat k as n**: Backend clamps to `len(particles) - 1`, not `n`, so this criterion is not met as written (`app.py:549-551`).
21. [PASS] **k parameter – “all points” unchecked by default**: Checkbox has no `checked` attribute and lock flag starts false (`index.html:481`, `index.html:1249`).
22. [PASS] **k parameter – checking “all points” locks k to n**: On check, k is forced to n (`index.html:1252-1254`).
23. [PASS] **k parameter – when locked, k controls disabled**: Input and slider are disabled while lock is active (`index.html:1254-1256`).
24. [PASS] **k parameter – when n changes while locked, k follows n**: n-sync updates k when lock is enabled (`index.html:972-976`).
25. [PASS] **k parameter – when unlocked, k and n independent again**: Controls are re-enabled when checkbox is unchecked (`index.html:1256-1259`).
26. [PASS] **k parameter – changing k immediately affects motion when unpaused**: Current k is included in each `/step` payload (`index.html:1119`).

27. [WARN] **n parameter – text box accepts only positive integer inputs**: Uses `parseInt` so non-integer numeric input is coerced rather than rejected (`index.html:490`, `index.html:951-953`).
28. [PASS] **n parameter – slider quantized to positive integer steps**: Slider min is 1 and step is 1 (`index.html:492`).
29. [PASS] **n parameter – text box and slider synchronized**: `syncNParameter` and `updateNParameterDisplay` keep them aligned (`index.html:950-989`, `index.html:1269-1274`).
30. [PASS] **n parameter – “place points” visible when no points exist**: Button text is set to “Place Points” when particles array is empty (`index.html:721-724`).
31. [FAIL] **n parameter – clicking “place points” creates n points with uniform distribution**: It creates points using the currently selected density, not always uniform (`index.html:701-703`, `index.html:665-689`).
32. [PASS] **n parameter – button changes to “clear points” when points exist**: Dynamic label switching implemented (`index.html:725-728`).
33. [PASS] **n parameter – clicking “clear points” removes points instantly**: Points are cleared immediately and canvas redrawn (`index.html:710-716`).
34. [PASS] **n parameter – changing n with points displayed adds/removes instantly**: Existing particles are adjusted immediately when n changes (`index.html:956-966`).
35. [PASS] **n parameter – added points via n change use current density**: New points come from `generatePointsByDensity` (`index.html:959-961`).
36. [PASS] **n parameter – removed points use consistent method**: Deterministic truncation (`slice`) is a consistent removal strategy (`index.html:963-965`).

37. [PASS] **maxstep – slider range includes 0 to 1**: Slider configured from 0 to 1 (`index.html:501`).
38. [PASS] **maxstep – changes reflected immediately when unpaused**: Updated maxstep is sent in each step request (`index.html:1277-1281`, `index.html:1121`).
39. [PASS] **maxstep – decreasing value slows movement**: Backend scales updates by `maxstep / max_step_magnitude` when needed (`app.py:404-412`).
40. [PASS] **maxstep – increasing value speeds movement**: Same scaling logic permits larger per-step motion with higher maxstep (`app.py:404-412`).

41. [PASS] **noise – slider range 0 to 1**: Noise slider and input are bounded 0..1 (`index.html:512-514`).
42. [PASS] **noise – at 0, deterministic (no jitter)**: Backend only samples/adds noise when `noise_level > 0` (`app.py:414-417`).
43. [PASS] **noise – increasing value adds visible random jitter**: Gaussian noise scaled by noise level is applied each step (`app.py:415-416`).
44. [PASS] **noise – changes take effect next iteration**: Current noise value is read from UI state in each `/step` request (`index.html:1122`, `index.html:1284-1288`).

45. [PASS] **Density menu – visible to right of parameter panel**: Layout places density panel after parameter panel in main flex row (`index.html:454-547`).
46. [PASS] **Density menu – uniform default selection**: Uniform option marked `.active` initially (`index.html:527-529`).
47. [PASS] **Density menu – Gaussian option available**: Explicit Gaussian option exists (`index.html:530-532`).
48. [PASS] **Density menu – selecting Gaussian reveals sigma controls**: Toggle logic adds/removes active class for Gaussian parameters (`index.html:1354-1358`).
49. [PASS] **Density menu – sigma has textbox + slider**: Both controls are present and wired (`index.html:539-545`, `index.html:1363-1367`).
50. [PASS] **Density menu – sigma adjustable in real time while running**: Sigma updates app state immediately and is sent every step (`index.html:1015-1037`, `index.html:1124`).
51. [WARN] **Density menu – accommodates future options**: Structure is somewhat extensible (`.density-options` + `data-density`) but behavior is still hardcoded for only two densities (`index.html:344-359`, `index.html:1353-1358`).
52. [FAIL] **Density menu – changing density should only affect newly placed/added points**: Current density is used in backend movement equations for all existing points, so existing trajectories change too (`index.html:1123-1124`, `app.py:390`, `app.py:446`, `app.py:479`).

53. [PASS] **Window/canvas – square with equal x/y scaling**: Canvas container is square and draw mapping is symmetric (`index.html:75`, `index.html:1398-1400`, `index.html:817-820`).
54. [FAIL] **Window/canvas – axis labels show full -1 to 1 range on both axes**: Only “1.0” labels are shown; full range labels/ticks are not present (`index.html:424-425`).
55. [PASS] **Window/canvas – points rendered as small dots**: Particles drawn as radius-3 circles (`index.html:873-881`).
56. [PASS] **Window/canvas – torus wrapping implemented**: Backend wraps updated coordinates with modulo mapping to `[-1, 1]` (`app.py:418-421`).

57. [PASS] **Statistics bar – visible above window**: Stats bar is rendered before main content (`index.html:402-415`).
58. [PASS] **Statistics – Riesz Energy checkbox unchecked by default and no value shown**: Starts unchecked and value placeholder is em dash (`index.html:406-409`).
59. [PASS] **Statistics – Volume RSD checkbox unchecked by default and no value shown**: Starts unchecked and value placeholder is em dash (`index.html:411-414`).
60. [PASS] **Statistics – checking Riesz Energy calculates and displays value**: Frontend requests it and backend computes `calculate_total_energy` (`index.html:1329-1334`, `index.html:1147-1149`, `app.py:563-567`).
61. [FAIL] **Statistics – checking Volume RSD calculates and displays value**: Backend crashes due bool/function name collision (`calculate_volume_rsd` shadowed by request flag) (`app.py:539`, `app.py:568-570`).
62. [FAIL] **Statistics – enabled stats update in real time**: Energy can update, but Volume RSD cannot due backend bug, so criterion is not fully met (`index.html:1147-1153`, `app.py:568-570`).
63. [PASS] **Statistics – unchecking hides value and stops calculation**: UI resets display and request flags control backend calculation (`index.html:1331-1340`, `index.html:1125-1126`).
64. [WARN] **Statistics – calculation accuracy vs reference code**: Energy math is structurally similar, but k-clamping mismatch (`k -> n-1`) and broken Volume RSD path prevent full confidence (`app.py:549-551`, `app.py:429-454`, `app.py:457-499`).

65. [PASS] **Point tools – three mutually exclusive buttons visible**: Pencil, eraser, and none buttons are present (`index.html:446-450`).
66. [PASS] **Point tools – pencil button selects placement mode**: Click handler sets point tool to `'pencil'` (`index.html:1296`).
67. [PASS] **Point tools – pencil mode places point at cursor**: Canvas click maps cursor location and calls `addPoint` (`index.html:1304-1308`).
68. [PASS] **Point tools – prevent same-location placement**: Placement guard rejects near-overlap (`index.html:737-742`).
69. [PASS] **Point tools – pencil placement increments n**: `n` is set to new particle count (`index.html:744-747`).
70. [PASS] **Point tools – eraser button selects deletion mode**: Click handler sets `'eraser'` (`index.html:1297`).
71. [PASS] **Point tools – eraser mode deletes nearest point**: `removeNearestPoint` finds minimum-distance particle and removes it (`index.html:764-778`).
72. [PASS] **Point tools – deletion decrements n**: `n` updated to `particles.length` after removal (`index.html:778-780`).
73. [PASS] **Point tools – x tool disables placement/deletion**: Click handler sets `pointTool = null`; canvas handler exits when tool is null (`index.html:1298`, `index.html:1302`).
74. [PASS] **Point tools – only one active at a time**: `setPointTool` clears all active classes before setting one (`index.html:1059-1070`).
75. [PASS] **Point tools – active tool has visual indicator**: `.active` class is applied to selected button (`index.html:203-207`, `index.html:1064-1070`).

76. [PASS] **Pause/Play – button visible in required control area**: Button appears in control bar between FPS monitor and tools (`index.html:429-450`).
77. [PASS] **Pause/Play – starts paused**: Initial state false + paused button styling (`index.html:443`, `index.html:576`).
78. [PASS] **Pause/Play – clicking toggles paused/unpaused**: `togglePlayPause` flips `isPlaying` (`index.html:1080-1083`, `index.html:1294`).
79. [PASS] **Pause/Play – visual indicator of current state**: Button text/icon and class switch between play/pause states (`index.html:1089-1095`).
80. [PASS] **Pause/Play – while paused, particles do not move**: `stepSimulation` exits early when not playing (`index.html:1107`).
81. [PASS] **Pause/Play – while unpaused, particles move by gradient descent**: Animation loop triggers backend step updates when playing (`index.html:1178-1180`, `app.py:363-423`).
82. [PASS] **Pause/Play – pause state persists across parameter changes**: Parameter listeners do not alter `isPlaying` (`index.html:1221-1387`).

83. [PASS] **FPS monitor – displays target and actual FPS**: Both values are rendered in monitor (`index.html:434-438`).
84. [PASS] **FPS monitor – target FPS input defaults to 30**: Input default and state default are 30 (`index.html:434`, `index.html:580`).
85. [PASS] **FPS monitor – target FPS accepts positive integers**: Change handler validates integer range >=1 (`index.html:1316-1323`).
86. [PASS] **FPS monitor – actual FPS updates during run loop**: Frame counting and periodic FPS updates are implemented (`index.html:1185-1192`).
87. [PASS] **FPS monitor – border green by default**: Default border color is green in CSS (`index.html:117-123`).
88. [PASS] **FPS monitor – border turns yellow when actual < target**: Class assignment logic applies `yellow` for this case (`index.html:1212-1214`).
89. [PASS] **FPS monitor – border turns red when actual < target/2**: Red threshold implemented (`index.html:1210-1212`).
90. [PASS] **FPS monitor – returns green when performance recovers**: Color classes are removed before re-evaluating state (`index.html:1208`).
91. [PASS] **FPS monitor – redraw waits when faster than target interval**: Loop gate enforces `deltaTime >= 1000 / targetFps` (`index.html:1171-1176`).
92. [PASS] **FPS monitor – user can push system to low FPS**: No throttling to force target attainment; heavy workloads can lower actual FPS (`index.html:1172-1195`).

93. [PASS] **Particle simulation – follows Riesz energy minimization with gradient descent-like updates**: Backend computes pointwise gradients and applies normalized steps (`app.py:323-356`, `app.py:392-412`).
94. [PASS] **Particle simulation – paused state allows stationary points with manual editing**: Movement halts while canvas click tools remain active (`index.html:1107`, `index.html:1300-1313`).
95. [PASS] **Particle simulation – unpaused updates at FPS-driven intervals**: Animation loop controls update cadence from target FPS (`index.html:1169-1199`).
96. [WARN] **Particle simulation – no point moves > maxstep per step**: Gradient step obeys maxstep, but post-step noise can increase net displacement beyond maxstep (`app.py:404-417`).
97. [PASS] **Particle simulation – if any point exceeds maxstep, all moves are proportionally scaled**: Global dampening based on max gradient norm is applied to every point (`app.py:404-412`).
98. [PASS] **Particle simulation – torus topology respected in movement**: Position wrapping and torus displacement are used (`app.py:168-183`, `app.py:418-421`).
99. [PASS] **Particle simulation – noise added after each step when enabled**: Noise is added after deterministic update (`app.py:411-417`).
100. [PASS] **Particle simulation – density weighting influences motion**: Gradient combines Riesz terms with density-derived weight/weight-gradient (`app.py:126-161`, `app.py:354`).
101. [PASS] **Particle simulation – k-nearest neighbors used in energy calculations**: Neighbor selection and k-based potential/gradient are implemented (`app.py:227-257`, `app.py:259-317`).
102. [WARN] **Particle simulation – behavior matches reference functions**: Structure is close, but k edge-case mismatch (`k -> n-1`) and Volume RSD failure indicate divergence in edge behavior (`app.py:549-551`, `app.py:568-570`, `python reference code.py:427-445`).

103. [PASS] **Backend – accepts HTTP requests with particle state and parameters**: `/step` parses request JSON and parameter fields (`app.py:505-539`).
104. [PASS] **Backend – computes new positions via gradient step**: `step_state_torus` is called for each request (`app.py:553-557`).
105. [PASS] **Backend – returns updated particle positions**: Response includes `particles` as JSON list (`app.py:574-577`).
106. [PASS] **Backend – calculates Riesz energy when requested**: Conditional energy computation path implemented (`app.py:563-567`).
107. [FAIL] **Backend – calculates volume RSD when requested**: Name collision causes runtime failure when volume RSD is enabled (`app.py:539`, `app.py:568-570`).
108. [PASS] **Backend – uses torus distances/wrapping**: Torus displacement and wrap-around formulas are present and used (`app.py:168-183`, `app.py:418-421`).
109. [PASS] **Backend – uses k-nearest neighbor implementation**: k-nearest selection is used by both potential and gradient (`app.py:227-257`, `app.py:277`, `app.py:306`).
110. [PASS] **Backend – implements density weighting**: Weight and weight-gradient functions are included in pointwise gradient (`app.py:126-161`, `app.py:350-355`).
111. [FAIL] **Backend – handles k > n by treating k as n**: Clamping to `len(particles) - 1` violates the criterion wording (`app.py:549-551`).
112. [WARN] **Backend – response speed sufficient for target FPS**: No performance safeguards/benchmarks are implemented; cannot confirm from code review alone (`app.py:505-585`).
113. [PASS] **Backend – based on reference stepStateTorus/ptWiseGradTorus_k approach**: Function decomposition and formulas closely mirror reference architecture (`app.py:323-423`, `python reference code.py:427-445`).

114. [WARN] **UI polish – controls respond immediately**: Most handlers are immediate, but functionality tied to broken backend paths (Volume RSD) is not reliable (`index.html:1221-1387`, `app.py:568-570`).
115. [WARN] **UI polish – no visible lag while dragging sliders**: Event wiring is lightweight, but visual lag cannot be verified without runtime profiling (`index.html:1222-1288`).
116. [WARN] **UI polish – rapid text input robustness**: Parsers guard invalid values, but coercion/truncation behavior (e.g., integer fields) is imperfect (`index.html:929-953`).
117. [PASS] **UI polish – button click reliability**: Controls are consistently event-driven with explicit handlers (`index.html:1294-1299`, `index.html:1329-1360`).
118. [PASS] **UI polish – layout stability during interaction**: CSS uses fixed panel structures and stable spacing; interaction handlers do not mutate layout structure (`index.html:21-397`).
119. [PASS] **UI polish – readable consistent typography/spacing**: Global typography and component spacing are consistently defined (`index.html:14-19`, `index.html:209-342`).

120. [FAIL] **Critical backend bug – `calculate_volume_rsd` name collision**: Request flag variable shadows the function, causing `bool is not callable` when Volume RSD is requested (`app.py:539`, `app.py:568-570`).
121. [WARN] **Error handling – missing robust JSON validation**: `request.get_json()` is not validated before `.get(...)`, so malformed/non-JSON bodies rely on generic exception handling (`app.py:528-539`).
122. [WARN] **Error handling – broad exception leaks internals**: Endpoint prints stack traces and returns raw exception strings to clients (`app.py:580-584`).
123. [WARN] **Security – Flask debug mode enabled**: Running with `debug=True` is unsafe outside local development (`app.py:617`).
124. [WARN] **Security – permissive CORS configuration**: `CORS(app)` enables broad cross-origin access without restrictions (`app.py:25`).
125. [WARN] **Code quality – side effects on import in reference Python file**: `python reference code.py` executes plotting/simulation at module import time (`python reference code.py:1050`).
126. [WARN] **Code quality – unused import**: `json` is imported but never used in backend (`app.py:22`).
