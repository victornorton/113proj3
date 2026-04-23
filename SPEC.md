This project is to create a web app that interactively displays a system of interacting particles that seek to minimize their reisz potential energy. When unpaused, the points move in real time according to a gradient descent algorithm similar to stepStateTorus. 


index.html contains html that creates a webpage that when initially loaded an empty square window. The window is labeled with axis similar to those seen on the matplotlib plots made by functions like testTorus. The region of the window is the square spanning from -1 to 1 over both x and y axes. Below the window is a pause/play button that determines if points soon to be created in the window move or not. To the right side of the window is a vertical panel with the following parameters:

     - s: reisz exponent, plays a role in the potential energy calculation which in turn influences the particles motion. Can accept any real number. Displayed as a text box that says "s = ___" above a slider initially between 0 and 10. Users can change the value by either moving the slider or manually typing a value into the underlined part of the text box. Values outside the range of the slider should be accepted by the text box. If they are entered the slider should move all the way to the appropriate side and the new bound should be the number that was entered in. The bounds of the slider can be manually changed by clicking on where ther are displayed and typing in values, as long as the left bound is smaller than the right bound. Defaults to 3.

     - k: the number of the nearest neighbors that contribute to each point's energy. Rounds to only positive integer values. If the value is larger than the total number of points, n, the program should just behave as if it was set to n. Displayed as a text box that the user can type values into paired with a discretely stepped slider similar to s except it is quantized to positive integers and rejects lower bounds below 1. There is a small checkbox below that is labeled "all points" that is off by default and fixes k to n when checked. While the box is checked, changing k is not possible and changing n causes k to change with it. Defaults to 6.

     - n: The total number of points. If no points are on in the window changing this doesn't immediately do anything. At the top of the panel there will be a button labeled "place points" that will place n uniformly distributed points. If there are already points in the window this button will instead say "clear points" and will delete all points when pressed. If points have already been placed in the window, then regardless of if the points are paused or unpaused, changing this value causes points to instantly appear or disappear to fit the new number. If points have to be added to fit the new number, they appear according to the currently selected distribution. Displayed with the same text box and slider structure as k, but doesn't have the "all points" checkbox. Defaults to 200

     - maxstep: an upper bound on how far the fastest moving particle is allowed to move. For each state update, if any particles try to move further than maxstep, the movements of ALL particles are normalized so that the fastest travels maxstep distance. Changing this while the points are unpaused should immediately cause them to move more slowly. 

     - noise: a bit of random movement may be added to the particles at each step. Specifically, after each iteration, for each point, a gaussian 2d vector with stdev equal to 0.1 is chosen, multiplied by the value of noise and added to its new position. A value of 0 means no noise, in which case a random vector needn't be sampled.
     displayed as slider between 0 and 1. Defaults to 0. 


Further to the right from the panel containing the above parameters, there should be a menu listing a number of possible densitiy distributions that the user can choose. The default should be the constant density distribution, and there should also be an option to choose a gaussian distribution with a customizable standard deviation. The Gaussian distribution option should have a text box and slider setup (similar to the s parameter) that allows real-time adjustment of the standard deviation. There should be space in the menu to add more density distribution options in the future. 

Above the window, there should be a horizontal bar listing real-time statistics about the particle system. One number displayed should be the total reisz energy of the system. Another should be the volume rsd value seen in testTorusDist_k, which is the relative standard deviation of the 'volumes' associated with each point as the product of the density function at that point and the square of that point's distance to its nearest neighbor. Both of these statistics should be disabled (unchecked) by default and can be toggled on/off with checkboxes to improve performance. Other statistics may be added in the future. 

Below the window, to the right the pause/play button there should be three mutually exclusive, toggleable buttons that allow the user to directly place and remove individual points in the window. While the button with a pencil icon is selected, clicking inside the widow places a point at the exact location of the cursor, although points cannot be placed in the exact same location as another. 
If the eraser button is selected, clicking on the window deletes the point that is closest to the cursor. If the 'x' button is clicked, the other two buttons are deselected and clicking in the window doesn't do anything. Changes to the number of points made using these tools should be relfected by the value of n in the parameter panel. 

Below the window to the left of the pause/play button should be a small menu displaying the target and actual fps of the points. The target fps should default to 30, but can be changed with a text box. The target fps serves as an upper limit: if the updated position is found faster than 1/fps seconds, the site should wait to redraw the points until that time has elapsed. If the actual fps falls below the target, no intervention is needed—the user may intentionally push the system to lower performance. The border of this fps display should be green by default, yellow when the actual fps dips below the target fps, and red when the actual fps falls below half the target fps. 


app.py is a python file that will be hosted on a tbd backend service that will accept requests from index.html that give the state of the particles and all the of the parameters, calculate the new position of points based on that information, and return the new position of points for index.html to quickly update. If extra statistics like total energy are requested, those are calculated here as well. The functions here should be based on those found in python reference code.py, particularly most up-to-date versions that treat the space like a torus and support k-nearest neighbor energies. stepStateTorus and ptWiseGradTorus_k are good examples.  

---

## ACCEPTANCE CRITERIA

### Initial Load
- [ ] Page loads with an empty square window spanning -1 to 1 on both x and y axes
- [ ] Axes are labeled similar to matplotlib plots from the reference code
- [ ] All controls are present and functional upon load
- [ ] All parameters have correct default values: s=3, k=6, n=200, maxstep=0.02, noise=0
- [ ] Default density distribution is uniform (constant density)
- [ ] Pause/play button starts in paused state
- [ ] Statistics checkboxes (energy, volume RSD) are unchecked by default
- [ ] FPS target defaults to 30
- [ ] Point manipulation tool defaults to 'x' (none selected)

### Parameter Panel - s (Riesz Exponent)
- [ ] Slider ranges from 0 to 10 by default
- [ ] Text box accepts any real number input
- [ ] Text box updates slider; slider updates text box
- [ ] Slider bounds can be manually changed by clicking on bounds and typing new values
- [ ] New slider bounds are only accepted if left bound < right bound
- [ ] Out-of-range text values cause slider to move to appropriate extreme and update bounds
- [ ] Changes to s immediately affect particle motion direction (if unpaused)

### Parameter Panel - k (Nearest Neighbors)
- [ ] Text box accepts only positive integer inputs
- [ ] Slider is quantized to positive integer steps
- [ ] Text box and slider stay synchronized
- [ ] If k > n, system treats k as equal to n
- [ ] "all points" checkbox is unchecked by default
- [ ] When "all points" is checked, k becomes locked to current n value
- [ ] When "all points" is checked, k text box and slider are disabled/non-functional
- [ ] When n changes while "all points" is checked, k changes to match the new n
- [ ] When "all points" is unchecked, k and n can change independently again
- [ ] Changes to k immediately affect particle motion (if unpaused)

### Parameter Panel - n (Number of Points)
- [ ] Text box accepts only positive integer inputs
- [ ] Slider is quantized to positive integer steps
- [ ] Text box and slider stay synchronized
- [ ] When no points exist, "place points" button is visible at top of panel
- [ ] Clicking "place points" instantly creates n points with uniform distribution
- [ ] When points exist, button changes label to "clear points"
- [ ] Clicking "clear points" removes all points instantly
- [ ] When points are displayed, changing n value causes points to instantly appear/disappear
- [ ] When points are added via n change, they use current density distribution
- [ ] When points are removed via n change, removal is random (or any consistent method)

### Parameter Panel - maxstep
- [ ] Slider ranges from 0 to some reasonable maximum (e.g., 1.0)
- [ ] Changes to maxstep are reflected immediately in particle animation (if unpaused)
- [ ] Decreasing maxstep visibly slows particle movement
- [ ] Increasing maxstep visibly speeds particle movement

### Parameter Panel - noise
- [ ] Slider ranges from 0 to 1
- [ ] At noise=0, particles move deterministically (no random jitter visible)
- [ ] Increasing noise adds visible random jitter to particle positions each step
- [ ] Changes to noise take effect on next iteration

### Density Distribution Menu
- [ ] Menu is visible to the right of the parameter panel
- [ ] "Uniform (constant density)" is the default selection
- [ ] "Gaussian" option is available in the menu
- [ ] Selecting "Gaussian" displays a text box/slider for standard deviation
- [ ] Standard deviation for Gaussian has both text box and slider (similar to s parameter)
- [ ] Gaussian standard deviation can be changed in real-time while simulation runs
- [ ] Menu is designed to accommodate additional distribution options in the future
- [ ] Changing density distribution only affects newly placed/added points, not existing points

### Window and Canvas
- [ ] Window displays as a square with equal x and y scaling
- [ ] Axis labels show -1 to 1 range on both axes
- [ ] Points are rendered as small dots
- [ ] Torus wrapping is correctly implemented (points wrap around boundaries)

### Statistics Bar (Above Window)
- [ ] Statistics bar is visible above the window
- [ ] "Riesz Energy" statistic has an unchecked checkbox by default and is not displayed
- [ ] "Volume RSD" statistic has an unchecked checkbox by default and is not displayed
- [ ] Checking "Riesz Energy" causes the total energy to be calculated and displayed
- [ ] Checking "Volume RSD" causes the volume RSD to be calculated and displayed
- [ ] Statistics update in real-time when calculation is enabled
- [ ] Unchecking a statistic hides it and stops calculation (improves performance)
- [ ] Statistics are accurate according to reference code calculations

### Point Manipulation Tools
- [ ] Three mutually exclusive buttons are visible below the window (pencil, eraser, x)
- [ ] Clicking the pencil button selects the "place points" mode
- [ ] While pencil is selected, clicking in window places a point at cursor location
- [ ] Points cannot be placed at the exact same location as existing points
- [ ] Placing a point via pencil increments n by 1
- [ ] Clicking the eraser button selects the "delete points" mode
- [ ] While eraser is selected, clicking in window deletes the closest point to cursor
- [ ] Deleting a point decrements n by 1
- [ ] Clicking the x button deselects all tools, disabling point placement/deletion
- [ ] Only one tool button can be selected at a time (mutually exclusive)
- [ ] When a tool is active, visual indicator shows which tool is selected

### Pause/Play Button
- [ ] Button is visible below the window, to the left of point manipulation tools
- [ ] Starts in paused state on page load
- [ ] Clicking pauses/unpauses the simulation
- [ ] Visual indicator (icon or label) clearly shows current state
- [ ] While paused, particles do not move
- [ ] While unpaused, particles move according to gradient descent algorithm
- [ ] Pause state persists when parameters are changed (doesn't auto-resume)

### FPS Monitor (Below Window, Left of Pause Button)
- [ ] FPS monitor displays both target fps and actual fps
- [ ] Target fps has a text box for user input (default 30)
- [ ] Target fps accepts positive integer values
- [ ] Actual fps updates in real-time during simulation
- [ ] FPS monitor border is green by default
- [ ] When actual fps < target fps, border turns yellow
- [ ] When actual fps < target fps / 2, border turns red
- [ ] Border returns to green when actual fps exceeds target
- [ ] If calculations complete before 1/target_fps seconds, page waits before redraw
- [ ] User can intentionally push system to low fps by increasing n or enabling expensive calculations

### Particle Simulation
- [ ] Particles follow Riesz potential energy minimization via gradient descent
- [ ] When paused, particles are stationary and can be manually placed/removed
- [ ] When unpaused, particles move smoothly at intervals determined by FPS target
- [ ] Movement respects maxstep limiter (no particle moves > maxstep distance per step)
- [ ] When any particle would exceed maxstep, all particles are scaled down proportionally
- [ ] Movement respects torus topology (particles wrap at ±1 boundaries)
- [ ] Noise is added to each particle's position after each step (if noise > 0)
- [ ] Density weighting affects particle motion based on selected distribution
- [ ] k-nearest neighbors are correctly identified and used in energy calculation
- [ ] Behavior matches reference code functions (stepStateTorus, ptWiseGradTorus_k)

### Backend (app.py)
- [ ] Accepts HTTP requests containing particle state and all parameters
- [ ] Calculates new particle positions using gradient descent
- [ ] Returns updated particle positions as response
- [ ] Calculates Riesz energy when requested
- [ ] Calculates volume RSD when requested
- [ ] Uses torus-based distance calculations (wrapping at ±1 boundaries)
- [ ] Uses k-nearest neighbor implementation for energy/gradient calculations
- [ ] Properly implements density function weighting
- [ ] Handles edge case where k > n (treats as k = n)
- [ ] Responses are fast enough to maintain target fps during simulation
- [ ] Code is based on reference code functions, particularly stepStateTorus and ptWiseGradTorus_k

### UI Responsiveness and Polish
- [ ] All controls respond immediately to user input
- [ ] No visible lag when dragging sliders
- [ ] Text input fields accept rapid input without errors
- [ ] Button clicks are registered reliably
- [ ] Page layout remains stable and doesn't shift/reflow during interaction
- [ ] Font sizes and spacing are consistent and readable  







