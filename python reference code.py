#PROJECT INFO

#List of functions to call and their descriptions:

'''
test2(n,iters, dim = dim, maxstep = 0.02,temper = 10, decay = 0.95):

  In a space that is the enclosed box [-1,1]^"dim", places "n" points and moves
  them for "iters" steps of gradient descent. The step length for each iteration
  is normalized so that the fastest moving particle travels no more than "maxstep"
  distance. For the last "temper" steps, this maxstep value decays exponentially at 
  rate "decay". Doesn't return anything and displays a plot of the final state.



animate(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Animates each step of the process described in test2. Returns the animation as
  an object that can be displayed with plt.show().

  

testTorus(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95, plotDist = False):
  
  When plotDist = False, does same thing as Test2, but instead of being an enclosed box, [-1,1]^"dim"
  behaves as a torus. When true, it also colors the points by by their nearest neighbor
  distance. 

  

def animateTorus(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Does the same thing as animate() but with in a Torus instead of an enclosed box.

  
  
testTorusDist(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Runs the same gradient descent process at testTorus, but instead of initial and final 
  states, it prints two plots of the points in the final state. On the left the points
  are colored according to thier nearest neighbor distance (NND), on the right they are colored 
  according to the "volume" obtained by rasing the NND to the power of dim and multiplying by
  the value of the density function at that point. In theory this volume should be constant
  across all the points. The plot displayed includes the min,max,mean,std, and rsv of the volumes, 
  and these values are also printed in the terminal.  



testTorusDist_k(n, iters, k, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95, plotDist = True):

  Does the same thing as testTorusDist, but only the energy from the "k" nearest neighbors
  of a point is included in the riesz energy. 

  

estDist(x, n, coeff = 1.0, vol = 4):

  Given only n and the density function (which is defined globally in
  this file), returns and estimate for what the nearest neighbor distance would 
  be for a given point if it was part of the a set of n points that were distributed
  according to the density with reisz energy minimization. It works by assuming 
  that points form an approximately hexagonal lattice locally. It becomes more 
  accurate for a given density as n increases. Coeff must be the result of integrating 
  the density function across the entire region. For the uniform density function
  p(x)=1 this coeff is equal to 4, because that is the volume of the region. This volume
  is assumed to be 4 but could be changed if we ever work with differently sized region.

  

eDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Runs the gradient descent process seen in testTorus, printing on the left the 
  final points colored by the NNDs observed, and on the right colored by the distances that
  estDist predicted they would have.



dDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Runs the gradient descent process seen in testTorus, printing on the left the 
  final points colored by the NNDs observed, and on the right colored by the signed
  difference between the observed and estDist-predicted distances.


relDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):

  Runs the gradient descent process seen in testTorus, printing on the left the 
  final points colored by the NNDs observed, and on the right colored by the 
  relative absolute difference between the observeed and estimated NNDs.

'''



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
#import scipy as sp

#riesz exponent
s = 3

#knn
k = 4

#dimension
dim = 2

#random seed
np.random.seed(21410)

#cures us of all evil
mysteryConst = 1

"------------------------------------------------------------------------------"




def squareGrid(N):
  pts = np.zeros((N**2,2))
  dist = 1/N
  for ii in range(N):
    for jj in range(N):
      pts[N * ii + jj] = np.array([dist*ii,dist*jj])
      
  return pts

"------------------------------------------------------------------------------"
#density function and gradient

def p(x):
  #in: point, out: desired density at that point
  return 1
  return pGauss(x)


def pGrad(x):
  #in: point, out: density gradient at point
  
  return 0
  return pGaussGrad(x)


def pGauss(x):
  #coeff is 2.23098
  norm_sq = np.sum(x**2)
  return np.exp(-norm_sq)

def pGaussGrad(x):
  norm_sq = np.sum(x**2)
  return 2 * x * np.exp(-norm_sq)

def pRadius(x):
  #coeff is 14/3
  return (.5 + np.linalg.norm(x)**2)

def pRadiusGrad(x):
  return -np.array([2*x[0], 2*x[1]])
"------------------------------------------------------------------------------"
#convert to wieght function and gradient

def densityToWeight(p, pGrad, s = s, dim = dim ):
  #w ~~ d^-(s/d)
  # w ~~ d^=(mystery*s/d)
  

  def w(x):
    return 1/p(x)**(mysteryConst*s/dim)

  def wGrad(x):
    return -(mysteryConst*s/dim) * p(x)**(-mysteryConst*s/dim - 1) * pGrad(x)

  return w, wGrad


w, wGrad = densityToWeight(p, pGrad, s = s, dim = dim)

"------------------------------------------------------------------------------"
#Riesz potential and gradient

def r(ii, pts, s = s):
  mask = np.ones(len(pts), dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  dist_sq = np.sum(disps**2, axis=1)
  dist_sq[dist_sq == 0] = np.inf
  return np.sum(1.0 / (dist_sq**(s/2.0)))


def rGrad(ii, pts, s = s):
  mask = np.ones(len(pts), dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  dist_sq = np.sum(disps**2, axis=1, keepdims=True)
  dist_sq[dist_sq == 0] = np.inf
  divisor = dist_sq**((s+2)/2.0)
  return np.sum(disps / divisor, axis=0)

"------------------------------------------------------------------------------"

#uses product rule to find gradient experienced by given point
def ptWiseGrad(ii, pts, s = s):
  return rGrad(ii, pts, s) * w(pts[ii]) + wGrad(pts[ii]) * r(ii,pts)


def movePt2(ii: int, pts, func):
#Takes state and index of point being considered, returns how the particle
#should be moved to minimize energy, considers step size
  dx = func(ii, pts)
  norm = np.sqrt(np.sum(dx**2))
  return pts[ii] + dx, norm


def crunch(x):
#O(n*dim) - vectorized with np.clip
  return np.clip(x, -1, 1)



def stepState2(pts, maxstep = 0.03, func = ptWiseGrad):
#Takes state, independently looks at how each particle should be moved to
#minimize energy given the others being fixed, and steps in all directions simultaneously
#looks at largest step taken by individual point and normalizes it to maxstep
#any point outside bounds is 'crunched' back in
  res = np.empty_like(pts)
  n = len(pts)
  maxv = np.zeros(n)

  for ii in range(n):
    res[ii], maxv[ii] = movePt2(ii, pts, func)

  dampening = min(maxstep/np.max(maxv),1)
  cand = pts + (res-pts)*dampening
  return crunch(cand)






#I added tempering for the maxstep. temper is the how many of the last steps
#experience the decay factor.
def test2(n,iters, dim = dim, maxstep = 0.02,temper = 10, decay = 0.95):

  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepState2(state, maxstep = maxstep)
  for ii in range(temper):
    state = stepState2(state, maxstep = maxstep * decay**ii)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  #print("INITIAL STATE:\n")
  ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15)
  ax1.set_aspect(1.0)
  ax1.set_title(f"Initial State\nPoints: {n}, Riesz Exponent: {s}")
  
  #print("FINAL STATE:\n")
  ax2.scatter(state[:, 0], state[:, 1], s=15)
  ax2.set_aspect(1.0)
  ax2.set_title(f"Final State\nPoints: {n}, Steps: {iters}, Riesz Exponent: {s}")
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Enclosed Box", ha='center', fontsize=11)
  
  plt.show(block=False)




def animate(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  
  state = 2*(np.random.rand(n, dim) - np.array([0.5]*dim))
  initial_state = state.copy()
  
  # Store states at each iteration
  states = [state.copy()]
  
  start_time = time.time()
  for ii in range(iters - temper):
    state = stepState2(state, maxstep=maxstep)
    states.append(state.copy())
  for ii in range(temper):
    state = stepState2(state, maxstep=maxstep * decay**ii)
    states.append(state.copy())
  runtime = time.time() - start_time
  
  # Create figure and axis
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.set_xlim(-1.1, 1.1)
  ax.set_ylim(-1.1, 1.1)
  ax.set_aspect(1.0)
  
  scatter = ax.scatter([], [], s=15)
  title = ax.set_title("")
  
  def update(frame):
    scatter.set_offsets(states[frame])
    title.set_text(f"Iteration {frame}/{len(states)-1}\nPoints: {n}, Riesz Exponent: {s}")
    return scatter, title
  
  anim = animation.FuncAnimation(fig, update, frames=len(states), 
                                  interval=50, blit=False, repeat=True)
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Enclosed Box", ha='center', fontsize=10)
  plt.show(block=False)
  
  return anim



#test2(400,55)

#anim = animate(200, 200, temper=100)
#plt.show()



#anim.save("animation1.gif", writer = 'pillow', fps=20)  

"______________________________________________________________________________"

"------------------------------------------------------------------------------"
#Torus version of Riesz potential and gradient, made with copilot
def rTorus(ii, pts, s = s):
  mask = np.ones(len(pts), dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  disps = disps - 2 * np.round(disps / 2) 
  dist_sq = np.sum(disps**2, axis=1)
  dist_sq[dist_sq == 0] = np.inf
  return np.sum(1.0 / (dist_sq**(s/2.0)))



def rGradTorus(ii, pts, s = s):
  mask = np.ones(len(pts), dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  disps = disps - 2 * np.round(disps / 2)
  dist_sq = np.sum(disps**2, axis=1, keepdims=True)
  dist_sq[dist_sq == 0] = np.inf
  divisor = dist_sq**((s+2)/2.0)
  return np.sum(disps / divisor, axis=0)


def kTorus(ii, pts, k=6, s = s):
  n = len(pts)
  if n <= 1 or k <= 0:
    return 0.0

  mask = np.ones(n, dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  disps = disps - 2 * np.round(disps / 2)

  dist_sq = np.sum(disps**2, axis=1)
  dist_sq[dist_sq == 0] = np.inf

  k = min(k, len(dist_sq))
  idx = np.argpartition(dist_sq, k-1)[:k]

  return np.sum(1.0 / (dist_sq[idx]**(s/2.0)))


def kGradTorus(ii, pts, k=6, s = s):
  n = len(pts)
  if n <= 1 or k <= 0:
    return np.zeros(pts.shape[1])

  mask = np.ones(n, dtype=bool)
  mask[ii] = False
  disps = pts[ii] - pts[mask]
  disps = disps - 2 * np.round(disps / 2)

  dist_sq = np.sum(disps**2, axis=1)
  dist_sq[dist_sq == 0] = np.inf

  k = min(k, len(dist_sq))
  idx = np.argpartition(dist_sq, k-1)[:k]

  div = dist_sq[idx]**((s+2)/2.0)
  return np.sum(disps[idx] / div[:, None], axis=0)

"------------------------------------------------------------------------------"

#Total Riesz potential energy on torus, copilot
def torusEnergy(pts, k=None, s=s):
  """
  Computes the total Riesz potential energy of points on a torus.
  
  Parameters:
  pts: array of shape (n, dim) containing n points on a torus in [-1, 1]^dim
  k: optional number of nearest neighbors to consider for each point.
     If None (default), uses all other points.
  s: Riesz exponent (optional, defaults to global s)
  
  Returns:
  Total Riesz potential energy of the system
  
  The result is equivalent to summing rTorus(ii, pts, s) over all points ii,
  or summing kTorus(ii, pts, k, s) if k is specified.
  """
  n = len(pts)
  
  if k is None:
    # Use all other points (equivalent to rTorus)
    return sum(rTorus(ii, pts, s=s) for ii in range(n))
  else:
    # Use k nearest neighbors
    return sum(kTorus(ii, pts, k=k, s=s) for ii in range(n))

"------------------------------------------------------------------------------"


#Product rule again, torus version
def ptWiseGradTorus(ii, pts, s = s):
  return rGradTorus(ii, pts, s) * w(pts[ii]) + wGrad(pts[ii]) * rTorus(ii,pts)


def ptWiseGradTorus_k(ii, pts,k=2, s = s):
  return kGradTorus(ii, pts, k, s=s) * w(pts[ii]) + wGrad(pts[ii]) * kTorus(ii,pts,k, s=s)



def stepStateTorus(pts, maxstep = 0.03, func = ptWiseGradTorus):
#Takes state and steps particles; instead of crunching back to bounds,
#wraps coordinates around
  res = np.empty_like(pts)
  n = len(pts)
  maxv = np.zeros(n)

  for ii in range(n):
    res[ii], maxv[ii] = movePt2(ii, pts, func)

  dampening = min(maxstep/np.max(maxv),1)
  cand = pts + (res-pts)*dampening
  # Wrap coordinates to [-1, 1]
  return ((cand + 1) % 2) - 1


def minDist(pts):
#For each point, finds the distance to its closest neighbor in the torus
  n = len(pts)
  min_distances = []
  
  for ii in range(n):
    mask = np.ones(n, dtype=bool)
    mask[ii] = False
    disps = pts[ii] - pts[mask]
    disps = disps - 2 * np.round(disps / 2)
    distances = np.sqrt(np.sum(disps**2, axis=1))
    min_distances.append(np.min(distances))
  
  return min_distances


#returns the number of points in the tighest distance 1 packing
#centered on (0,0) inside the region [0,x]^2
def ptsInSquare(x):

  return (np.floor(x + 1) * np.floor(x/np.sqrt(3) + 1) 
        + np.floor(x + 0.5) * np.floor(x/np.sqrt(3) + 0.5))

#I conjecture that this is equal to ptsInSquare + O(x)
#only a matters in this question but I also believe b is the 'best choice'
def ptsInSquareEst(x):

  a = 2/np.sqrt(3)
  b = -1/3
  return a * (x-b)**2

#vol is the area/volume of the region, currently 4
#coeff is the result of integrating p(x) over the entire region.
#if P is unnormalized you need to determine coeff and include it in the call
def estDist(x, n, coeff = 1.0, vol = 4):
  
  a = 2/np.sqrt(3)
  b = -1/3

  def h(x):
    return b + np.sqrt(x/a)
  
  w = vol * p(x) * n / coeff
  return 1/h(w) * np.sqrt(vol)


"------------------------------------------------------------------------------"

#Creates 2 plots of before and after
def testTorus(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95, plotDist = False):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  if plotDist:
    initial_dists = minDist(initial_state)
    final_dists = minDist(state) 
    
    
    sc1 = ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15, c=initial_dists, cmap='nipy_spectral')
    plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
    sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
    plt.colorbar(sc2, ax=ax2, label='Distance to Nearest Neighbor')

  else:
    ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15)
    ax2.scatter(state[:, 0], state[:, 1], s=15)
  
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  ax1.set_title(f"Initial State \nPoints: {n}, Riesz Exponent: {s}, Steps: {iters}, MC: {mysteryConst}")
  ax2.set_title(f"Final State")

  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, mstp: {maxstep}, temp: {temper}, dec: {decay}, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)






def testTorus_k(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95, plotDist = False):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  if plotDist:
    initial_dists = minDist(initial_state)
    final_dists = minDist(state) 
    
    
    sc1 = ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15, c=initial_dists, cmap='nipy_spectral')
    plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
    sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
    plt.colorbar(sc2, ax=ax2, label='Distance to Nearest Neighbor')

  

  else:
    ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15)
    ax2.scatter(state[:, 0], state[:, 1], s=15)
  
  initial_energy = torusEnergy(initial_state, k)
  final_energy = torusEnergy(state,k)

  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  ax1.set_title(f"Initial State \nPoints: {n}, k:{k}, Riesz Exponent: {s}, \n Steps: {iters}, MC: {mysteryConst}, energy: {initial_energy:.3e}")
  ax2.set_title(f"Final State \n energy: {final_energy:.3e}")

  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, mstp: {maxstep}, temp: {temper}, dec: {decay}, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)



def animateTorus(n, iters, k, dim = dim, maxstep = 0.025, temper = 10, decay = 0.95):
  
  state = 2*(np.random.rand(n, dim) - np.array([0.5]*dim))
  initial_state = state.copy()
  

  states = [state.copy()]
  
  start_time = time.time()
  for ii in range(iters - temper):
    state = stepStateTorus(state, maxstep=maxstep, func = ptWiseGradTorus_k)
    states.append(state.copy())
  for ii in range(temper):
    state = stepStateTorus(state, maxstep=maxstep * decay**ii, func = ptWiseGradTorus_k)
    states.append(state.copy())
  runtime = time.time() - start_time
  
  # Create figure and axis
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.set_xlim(-1.1, 1.1)
  ax.set_ylim(-1.1, 1.1)
  ax.set_aspect(1.0)
  
  scatter = ax.scatter([], [], s=15)
  title = ax.set_title("")
  
  def update(frame):
    scatter.set_offsets(states[frame])
    title.set_text(f"Iteration {frame}/{len(states)-1}\nPoints: {n}, Steps: {frame}, Riesz Exponent: {s}, MC: {mysteryConst}")
    return scatter, title
  
  anim = animation.FuncAnimation(fig, update, frames=len(states), 
                                  interval=50, blit=False, repeat=True)
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, mstp: {maxstep}, temp: {temper}, dec: {decay}, Region Type: Torus", ha='center', fontsize=10)
  plt.show(block=False)
  
  return anim



#Lazily copied from testTorus lol
def testTorusDist(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  if True: #lol
    initial_dists = minDist(initial_state)
    final_dists = minDist(state) 
    vols = np.zeros_like(final_dists)
    #final_dists = np.array(p(state[ii]) * final_dists[ii]**2 for ii in range(n))
    for ii in range(n):
        vols[ii] = p(state[ii]) * final_dists[ii]**dim
    dec = 9
    mn = round(np.min(vols), dec)
    mx = round(np.max(vols), dec)
    mean = round(np.mean(vols), dec)
    std = round(np.std(vols), dec)
    rsd = round(np.std(vols)/np.mean(vols), dec)
    


    print(f"min: {mn}")
    print(f"max: {mx}")
    print(f"mean: {mean}")
    print(f"std: {std}")
    print(f"rsv: {rsd}")

    textstr = (f"""min: {mn}
max: {mx}
mean: {mean}
std: {std}
rsd: {rsd}""")
               

    sc1 = ax1.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
    plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
    sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=vols, cmap='nipy_spectral')
    plt.colorbar(sc2, ax=ax2, label='D^2 * p')

    #sc2 = ax2.bar(np.arange(n), vols )

    #sc3 = ax3.scatter(state[:, 0], state[:, 1], s=15, c=vols, cmap='viridis')
    #plt.colorbar(sc2, ax=ax2, label='D^2 * p')

  
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  
  ax1.set_title(f"Final State Distances \nPoints: {n}, Riesz Exponent: {s}, steps: {iters}, MC: {mysteryConst} \nmstp: {maxstep}, temp: {temper}, dec: {decay}")
  
  
  ax2.set_title(f"Final State Vols (should be constant) ")

  #these lines to make the text box were appropriated from some online tutorial 
  #website
  props = dict(boxstyle='round', facecolor='blue', alpha=0.15)
  fig.text(0.906, 0.97 , textstr, fontsize=8,ha = 'left',
        verticalalignment='top', bbox=props)
  #if plotDist:
    #ax3.set_aspect(1.0)
    #ax3.set_title(f"Final State \nPoints: {n}, Steps: {iters}, Riesz Exponent: {s}")
     
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)





def testTorusDist_k(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus_k)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus_k)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  if True: #lol
    initial_dists = minDist(initial_state)
    final_dists = minDist(state) 
    vols = np.zeros_like(final_dists)
    #final_dists = np.array(p(state[ii]) * final_dists[ii]**2 for ii in range(n))
    for ii in range(n):
        vols[ii] = p(state[ii]) * final_dists[ii]**2
    dec = 9
    mn = round(np.min(vols), dec)
    mx = round(np.max(vols), dec)
    mean = round(np.mean(vols), dec)
    std = round(np.std(vols), dec)
    rsd = round(np.std(vols)/np.mean(vols), dec)
    


    print(f"min: {mn}")
    print(f"max: {mx}")
    print(f"mean: {mean}")
    print(f"std: {std}")
    print(f"rsv: {rsd}")

    textstr = (f"""min: {mn}
max: {mx}
mean: {mean}
std: {std}
rsd: {rsd}""")
               

    sc1 = ax1.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
    plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
    sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=vols, cmap='nipy_spectral')
    plt.colorbar(sc2, ax=ax2, label='D^2 * p')

    #sc2 = ax2.bar(np.arange(n), vols )

    #sc3 = ax3.scatter(state[:, 0], state[:, 1], s=15, c=vols, cmap='viridis')
    #plt.colorbar(sc2, ax=ax2, label='D^2 * p')

  
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  
  ax1.set_title(f"Final State Distances \nPoints: {n}, k:{k}, Riesz Exponent: {s}, steps: {iters}, MC: {mysteryConst} \nmstp: {maxstep}, temp: {temper}, dec: {decay}")
  
  
  ax2.set_title(f"Final State Vols (should be constant) ")

  #these lines to make the text box were appropriated from some online tutorial 
  #website
  props = dict(boxstyle='round', facecolor='blue', alpha=0.15)
  fig.text(0.906, 0.97 , textstr, fontsize=8,ha = 'left',
        verticalalignment='top', bbox=props)
  #if plotDist:
    #ax3.set_aspect(1.0)
    #ax3.set_title(f"Final State \nPoints: {n}, Steps: {iters}, Riesz Exponent: {s}")
     
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)



#anim = animateTorus(200, 200, maxstep=0.05, temper=100, decay = 0.95)
#plt.show()
#anim.save("animationTorus1000.gif", writer = 'pillow', fps=20)
#test2(100, 100)
#prob of gaussian pt in torus is ~0.5864

def eDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

  final_dists = minDist(state)

  ests = np.zeros(n)
  for ii in range(n):
    ests[ii] = estDist(state[ii] ,n, coeff)

  sc1 = ax1.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
  plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
  sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=ests, cmap='nipy_spectral')
  plt.colorbar(sc2, ax=ax2, label='d(x)')
   
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  
  ax1.set_title(f"Final State Distances \nPoints: {n}, Riesz Exponent: {s}, Steps: {iters}, MC: {mysteryConst} \nmstp: {maxstep}, temp: {temper}, dec: {decay}")
  
  
  ax2.set_title(f"Estimated Distances (should be similar) ")

  
     
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)



def dDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

  final_dists = minDist(state)

  ests = np.zeros(n)
  for ii in range(n):
    ests[ii] = estDist(state[ii] ,n, coeff)
  
  diffs = final_dists - ests

  sc1 = ax1.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
  plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
  sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=diffs, cmap='nipy_spectral')
  plt.colorbar(sc2, ax=ax2, label='d(x)')
   
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  
  ax1.set_title(f"Final State Distances \nPoints: {n}, Riesz Exponent: {s}, Steps: {iters}, MC: {mysteryConst} \nmstp: {maxstep}, temp: {temper}, dec: {decay}")
  
  
  ax2.set_title(f"Observed-Estimated dists (should be small) ")

  
     
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)


def relDist(n, iters, coeff = 1.0, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95):
  state =   2*(np.random.rand(n,dim)- np.array([0.5]*dim))
  
  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

  final_dists = minDist(state)

  ests = np.zeros(n)
  for ii in range(n):
    ests[ii] = estDist(state[ii] ,n, coeff)
  
  diffs = final_dists - ests

  for ii in range(n):
    diffs[ii] = np.abs(diffs[ii]/final_dists[ii])

  sc1 = ax1.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
  plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
  sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=diffs, cmap='nipy_spectral')
  plt.colorbar(sc2, ax=ax2, label='d(x)')
   
  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  
  ax1.set_title(f"Final State Distances \nPoints: {n}, Riesz Exponent: {s}, Steps: {iters}, MC: {mysteryConst} \nmstp: {maxstep}, temp: {temper}, dec: {decay}")
  
  
  ax2.set_title(f"relative errors by point (should be small) ")

  
     
  


  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)



def animSquare(n, iters, dim = dim, maxstep = 0.0025, temper = 10, decay = 0.95):
  
  state = 2*(squareGrid(n) - np.array([0.5]*dim))
  initial_state = state.copy()

  state[0] = [0.13,0.11]
  

  states = [state.copy()]
  
  start_time = time.time()
  for ii in range(iters - temper):
    state = stepStateTorus(state, maxstep=maxstep, func = ptWiseGradTorus)
    states.append(state.copy())
  for ii in range(temper):
    state = stepStateTorus(state, maxstep=maxstep * decay**ii, func = ptWiseGradTorus)
    states.append(state.copy())
  runtime = time.time() - start_time
  
  # Create figure and axis
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.set_xlim(-1.1, 1.1)
  ax.set_ylim(-1.1, 1.1)
  ax.set_aspect(1.0)
  
  scatter = ax.scatter([], [], s=15)
  title = ax.set_title("")
  
  def update(frame):
    scatter.set_offsets(states[frame])
    title.set_text(f"Iteration {frame}/{len(states)-1}\nPoints: {n}, Steps: {frame}, Riesz Exponent: {s}, MC: {mysteryConst}")
    return scatter, title
  
  anim = animation.FuncAnimation(fig, update, frames=len(states), 
                                  interval=50, blit=False, repeat=True)
  
  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, mstp: {maxstep}, temp: {temper}, dec: {decay}, Region Type: Torus", ha='center', fontsize=10)
  plt.show(block=False)
  
  return anim



def testTorusSquare_k(n, iters, dim = dim, maxstep = 0.05, temper = 10, decay = 0.95, plotDist = False):



  state = 2*(squareGrid(n) - np.array([0.5]*dim))
  

  state[0] = [0.13,0.11]

  initial_state = state.copy()

  start_time = time.time()
  for ii in range(iters-temper):
    state = stepStateTorus(state, maxstep = maxstep, func = ptWiseGradTorus)
  for ii in range(temper):
    state = stepStateTorus(state, maxstep = maxstep * decay**ii, func = ptWiseGradTorus)
  runtime = time.time() - start_time

  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  if plotDist:
    initial_dists = minDist(initial_state)
    final_dists = minDist(state) 
    
    
    sc1 = ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15, c=initial_dists, cmap='nipy_spectral')
    plt.colorbar(sc1, ax=ax1, label='Distance to Nearest Neighbor')
    
    sc2 = ax2.scatter(state[:, 0], state[:, 1], s=15, c=final_dists, cmap='nipy_spectral')
    plt.colorbar(sc2, ax=ax2, label='Distance to Nearest Neighbor')

  

  else:
    ax1.scatter(initial_state[:, 0], initial_state[:, 1], s=15)
    ax2.scatter(state[:, 0], state[:, 1], s=15)
  
  initial_energy = torusEnergy(initial_state, k)
  final_energy = torusEnergy(state,k)

  for ax in (ax1, ax2):
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect(1.0)

  ax1.set_title(f"Initial State \nPoints: {n}, k:{k}, Riesz Exponent: {s}, \n Steps: {iters}, MC: {mysteryConst}, energy: {initial_energy:.3e}")
  ax2.set_title(f"Final State \n energy: {final_energy:.3e}")

  fig.text(0.5, 0.02, f"Runtime: {runtime:.3f} seconds, mstp: {maxstep}, temp: {temper}, dec: {decay}, Region Type: Torus", ha='center', fontsize=11)
  
  plt.show(block=False)


#eDist(200,200, coeff=14/3 ,maxstep = 0.02, temper = 100, decay = 0.95)
#dDist(200,200, coeff=14/3 ,maxstep = 0.02, temper = 100, decay = 0.95)
#relDist(200,200, coeff=14/3 ,maxstep = 0.02, temper = 100, decay = 0.95)
testTorusSquare_k(16,400, maxstep = 0.001, temper = 100, decay = 0.99, plotDist = True)


#anim = animSquare(16,200)
#anim = animateTorus(100,100)

#plt.show()
#anim.save("defective_square_grid2.gif", writer = 'pillow', fps=20)  

#anim = animateTorus(100,100)
#anim.save("k4s6_from_unif_preliminary_anim.gif", writer = 'pillow', fps=20) 
#plt.show()
#checking k nearest neighbors
#using tighter gaussian
#go back and search for mathematical explanation of the mystery const
#consider the global  mass movement problem

