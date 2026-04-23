I am considering trying to make a an HTML page that can interactively display the behavior of the functions I've defined here. Specifically, I want there to be a display window with points inside, and a set of user friendly controls that allows one to change parameters such as reisz exponent in real time. Could this be feasible or is it doomed to be imipractically slow?
To clarify, I want the behavior of the points to change step-by-step, similar to how animateTorus looks. As such, as long it takes less than about 1/30 of a second to execute a single call the equivalent of stepStateTorus and plot the new point locations, the performance would be acceptable.
Can we further consider whether a backend is necessary? I am drawn to options that don't require a server, because I don't want to spend a lot of money, and I've found that free options like render.com have annoynig downsides like long spin-up times.
If I still want other people to access this project from their own devices at any time, what are the best remaing options?
Pre-computing is unfortunately not feasible. I am willing to reconsider a backend method if it is the only way to achieve true interactivity and good performance.
create a file, spec.md that gives a detailed description for each of the necessary components of the backend implementation of this project. Make sure to specify expected behavior, error handling, and include a set of acceptance conditions that must be passed.

*NOTE* I didn't like what I got from the above prompt so the SPEC.md file you see is still written entirely by me.


HERE IS A NEW INSTANCE:

Carefully read SPEC.md and add to it a list of acceptance criteria that must be passed to ensure the the project displayed all of the desired behavior. If any confusion arises from SPEC.md ask me to clarify. Do not attempt to create the actual files for index.html or app.py yet.

*never mind, after writing for a long time I decided to see if the AI could write acceptance criteria based on the description I had written so far.*

1: The text box/slider set up would be ideal. 2: The points should appear instantly, no animation is needed. 3: The energy and volume RSD statistics should be off be default, and those are the only ones that I have planned at the moment. 4: I leave it for the user to decide when the performance is poor, no official threshold is needed. 5: I should clarify that the target fps is only meant to be an upper, not lower limit. If the fsp dips below the target at any point the app doesn't need to intervene, it's just meant to serve as a tool for the user to see how well the app is handling the simulation. The user may very well push things until low fps occurs if they wish. Now that I think of it It would be nice if the border of the fps outline turns yellow whenever the fps dips below the target and red when less than half the target. The default color should probably be green in this case. Feel free to update SPEC.md to reflect this additional information I have given you.


HERE IS A NEW INSTANCE:
Carefully read SPEC.md and the python reference code. Then fully implement the project exactly as specified. Make sure that all the features described work properly. Leave generous explanatory comments in your output. If there are things that can't be completed until a backend hosting method is decided upon, tell me and leave a conspicous placeholder in every location that will need further work. Ask for clarification if any confusion arises.


HERE IS A NEW INSTANCE ON CURSOR (AS OPPOSED TO COPILOT)

Review the Python code in this project against the spec in SPEC.md.
For each item in the acceptance criteria, check whether the code
actually implements it correctly. Also check for:
- Bugs or logic errors
- Missing error handling
- Code quality issues (unclear naming, repeated code, etc.)
- Security concerns (e.g., unsafe file handling)

Format your review as a numbered list of findings, each marked as
[PASS], [FAIL], or [WARN]. Be specific — reference file names and
line numbers. Save this as REVIEW.md

Consult REVIEW.md and implement fixes for every FAIL instance.
