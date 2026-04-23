This project is to create a web app that interactively displays a system of interacting particles that seek to minimize their reisz potential energy. When unpaused, the points move in real time according to a gradient descent algorithm similar to stepStateTorus. 


index.html contains html that creates a webpage that when initially loaded an empty square window. The window is labeled with axis similar to those seen on the matplotlib plots made by functions like testTorus. The region of the window is the square spanning from -1 to 1 over both x and y axes. Below the window is a pause/play button that determines if points soon to be created in the window move or not. To the right side of the window is a vertical panel with the following parameters:

     - s: reisz exponent, plays a role in the potential energy calculation which in turn influences the particles motion. Can accept any real number. Displayed as a text box that says "s = ___" above a slider initially between 0 and 10. Users can change the value by either moving the slider or manually typing a value into the underlined part of the text box. Values outside the range of the slider should be accepted by the text box. If they are entered the slider should move all the way to the appropriate side and the new bound should be the number that was entered in. The bounds of the slider can be manually changed by clicking on where ther are displayed and typing in values, as long as the left bound is smaller than the right bound. Defaults to 3.

     - k: the number of the nearest neighbors that contribute to each point's energy. Rounds to only positive integer values. If the value is larger than the total number of points, n, the program should just behave as if it was set to n. Displayed as a text box that the user can type values into paired with a discretely stepped slider similar to s except it is quantized to positive integers and rejects lower bounds below 1. There is a small checkbox below that is labeled "all points" that is off by default and fixes k to n when checked. While the box is checked, changing k is not possible and changing n causes k to change with it. Defaults to 6.

     - n: The total number of points. If no points are on in the window changing this doesn't immediately do anything. At the top of the panel there will be a button labeled "place points" that will place n uniformly distributed points. If there are already points in the window this button will instead say "clear points" and will delete all points when pressed. If points have already been placed in the window, then regardless of if the points are paused or unpaused, changing this value causes points spontaneously disappear or appear to fit the new number. If points have to be added to fit the new number, they appear according to the currently selected distribution. Displayed with the same text box and slider structure as k, but doesn't have the "all points" checkbox. Defaults to 200

     - maxstep: an upper bound on how far the fastest moving particle is allowed to move. For each state update, if any particles try to move further than maxstep, the movements of ALL particles are normalized so that the fastest travels maxstep distance. Changing this while the points are unpaused should immediately cause them to move more slowly. 

     - noise: a bit of random movement may be added to the particles at each step. Specifically, after each iteration, for each point, a gaussian 2d vector with stdev equal to 0.1 is chosen, multiplied by the value of noise and added to its new position. A value of 0 means no noise, in which case a random vector needn't be sampled.
     displayed as slider between 0 and 1. Defaults to 0. 


Further to the right from the panel containing the above parameters, there should be a menu listing a number of possible densitiy distributions that the user can choose. The default should be the constant density distribution, and there should also be an option to choose a gaussian distribution with customizable standard deviation. There should be space in the menu to add more density distribution options in the future. 

Above the window, there should be a horizontal bar listing real-time statistics about the particle system. One number dislayed should be the total reisz energy of the system. Another should be the volume rsd value seen in testTorusDist_k, which is the relative standard deviation of the 'volumes' associated with each point as the product of the density function at that point and the square of that point's distance to its nearest neighbor. Some of these statistics may be expensive to calculate, so there should be checkboxes to disable these statistics in order to get better performance. 

Below the window, to the right the pause/play button there should be three mutually exclusive, toggleable buttons that allow the user to directly place and remove individual points in the window. While the button with a pencil icon is selected, clicking inside the widow places a point at the exact location of the cursor, although points cannot be placed in the exact same location as another. 
If the eraser button is selected, clicking on the window deletes the point that is closest to the cursor. If the 'x' button is clicked, the other two buttons are deselected and clicking in the window doesn't do anything. Changes to the number of points made using these tools should be relfected by the value of n in the parameter panel. 

Below the window to the left of the pause/play button should be a small menu displaying the target and actual fps of the points. The target fps should default to 30, but can be changed with a type box. If the updated position is found faster than that the site should wait to redraw the points until 1/fps seconds has passed. 



main.py






