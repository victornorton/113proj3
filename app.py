"""
Flask Backend for Riesz Potential Interactive Particle Simulator

This Flask application handles all simulation computations for the particle system.
It receives particle states and parameters from the frontend, performs a single step
of gradient descent to minimize Riesz potential energy, and returns updated positions.

Key responsibilities:
- Compute Riesz potential energy and gradients on a torus
- Support k-nearest neighbor energy calculations
- Implement multiple density distribution functions
- Add random noise to particle motion
- Calculate real-time statistics (energy, volume RSD)
- Maintain proper step size normalization and boundary wrapping
"""



import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend requests

# ============================================================================
# CONSTANTS AND GLOBAL PARAMETERS
# ============================================================================

DIM = 2  # Simulation is always 2D
RIESZ_EXPONENT_DEFAULT = 3  # Default Riesz exponent (not actively used by frontend choice)
MYSTERY_CONST = 1  # Multiplier for density weighting formula


# ============================================================================
# DENSITY FUNCTION IMPLEMENTATIONS
# ============================================================================

def density_uniform(point):
    """
    Uniform (constant) density distribution.
    Returns constant value of 1 everywhere in [-1, 1]^2.
    
    Args:
        point: [x, y] coordinate
        
    Returns:
        float: density value (always 1)
    """
    return 1.0


def density_uniform_grad(point):
    """
    Gradient of uniform density.
    Since density is constant, gradient is zero everywhere.
    
    Args:
        point: [x, y] coordinate
        
    Returns:
        np.array: [0, 0]
    """
    return np.array([0.0, 0.0])


def density_gaussian(point, sigma=1.0):
    """
    Gaussian (normal) density distribution centered at origin.
    p(x) = exp(-||x||^2 / sigma^2)
    
    Args:
        point: [x, y] coordinate
        sigma: standard deviation
        
    Returns:
        float: density value
    """
    norm_sq = np.sum(point ** 2)
    return np.exp(-norm_sq / (sigma ** 2))


def density_gaussian_grad(point, sigma=1.0):
    """
    Gradient of Gaussian density.
    ∇p(x) = -2x/sigma^2 * exp(-||x||^2 / sigma^2)
    
    Args:
        point: [x, y] coordinate
        sigma: standard deviation
        
    Returns:
        np.array: gradient vector
    """
    norm_sq = np.sum(point ** 2)
    exponential = np.exp(-norm_sq / (sigma ** 2))
    return (-2 * point / (sigma ** 2)) * exponential


# ============================================================================
# WEIGHT FUNCTION (density weighting for particle energy)
# ============================================================================

def get_density_functions(density_type, gaussian_sigma=1.0):
    """
    Return the appropriate density and gradient functions based on distribution type.
    
    Args:
        density_type: 'uniform' or 'gaussian'
        gaussian_sigma: standard deviation for Gaussian (ignored if uniform)
        
    Returns:
        tuple: (density_function, gradient_function)
    """
    if density_type == 'gaussian':
        p = lambda x: density_gaussian(x, gaussian_sigma)
        p_grad = lambda x: density_gaussian_grad(x, gaussian_sigma)
    else:  # default to uniform
        p = density_uniform
        p_grad = density_uniform_grad
    
    return p, p_grad


def get_weight_functions(s, dim, density_type, gaussian_sigma=1.0):
    """
    Convert density function to weight function used in particle energy.
    Weight relates to the Riesz potential through: w(x) = 1/p(x)^(s/dim)
    
    The gradient of the weight incorporates the density gradient.
    
    Args:
        s: Riesz exponent
        dim: dimension (always 2)
        density_type: 'uniform' or 'gaussian'
        gaussian_sigma: standard deviation for Gaussian
        
    Returns:
        tuple: (weight_function, weight_gradient_function)
    """
    p, p_grad = get_density_functions(density_type, gaussian_sigma)
    exp_factor = MYSTERY_CONST * s / dim
    
    def w(x):
        """Weight function"""
        p_val = p(x)
        if p_val <= 0:
            return float('inf')
        return 1.0 / (p_val ** exp_factor)
    
    def w_grad(x):
        """Gradient of weight function using chain rule"""
        p_val = p(x)
        if p_val <= 0:
            return np.array([0.0, 0.0])
        p_grad_val = p_grad(x)
        coeff = -exp_factor * (p_val ** (-exp_factor - 1))
        return coeff * p_grad_val
    
    return w, w_grad


def normalize_particle_density_params(
    particle_density_params, point_count, default_density_type='uniform', default_gaussian_sigma=1.0
):
    """
    Normalize per-particle density metadata to match the particle count.

    Each particle gets a metadata object:
    {
        "densityType": "uniform" | "gaussian",
        "gaussianSigma": <positive float>
    }

    If metadata is missing or malformed, default density settings are used.
    """
    default_density_type = default_density_type if default_density_type == 'gaussian' else 'uniform'
    default_gaussian_sigma = float(default_gaussian_sigma)
    if default_gaussian_sigma <= 0:
        default_gaussian_sigma = 1.0

    source = particle_density_params if isinstance(particle_density_params, list) else []
    normalized = []

    for idx in range(point_count):
        entry = source[idx] if idx < len(source) and isinstance(source[idx], dict) else {}

        density_type = entry.get('densityType', default_density_type)
        if density_type != 'gaussian':
            density_type = 'uniform'

        gaussian_sigma = entry.get('gaussianSigma', default_gaussian_sigma)
        try:
            gaussian_sigma = float(gaussian_sigma)
        except (TypeError, ValueError):
            gaussian_sigma = default_gaussian_sigma

        if gaussian_sigma <= 0:
            gaussian_sigma = default_gaussian_sigma

        normalized.append({
            'densityType': density_type,
            'gaussianSigma': gaussian_sigma
        })

    return normalized


# ============================================================================
# TORUS DISTANCE CALCULATIONS
# ============================================================================

def torus_displacement(p1, p2):
    """
    Calculate shortest displacement vector on torus [-1, 1]^2.
    The torus wraps: distance is measured considering wraparound at ±1.
    
    Args:
        p1: first point [x, y]
        p2: second point [x, y]
        
    Returns:
        np.array: displacement vector (shortest path on torus)
    """
    displacement = p1 - p2
    # Wrap each coordinate: if distance > 1, take the wrapped path
    displacement = displacement - 2 * np.round(displacement / 2)
    return displacement


def torus_distance_sq(p1, p2):
    """
    Calculate squared distance on torus.
    
    Args:
        p1: first point [x, y]
        p2: second point [x, y]
        
    Returns:
        float: squared distance on torus
    """
    disp = torus_displacement(p1, p2)
    return np.sum(disp ** 2)


def min_distance_to_neighbors(point, points):
    """
    Calculate distance to nearest neighbor on torus.
    Used for volume RSD calculation.
    
    Args:
        point: reference point [x, y]
        points: array of all point positions
        
    Returns:
        float: distance to nearest neighbor
    """
    min_dist = float('inf')
    for other_point in points:
        dist_sq = torus_distance_sq(point, other_point)
        if dist_sq > 1e-10:  # Ignore self and duplicates
            dist = np.sqrt(dist_sq)
            if dist < min_dist:
                min_dist = dist
    return min_dist if min_dist < float('inf') else 0.0


# ============================================================================
# RIESZ POTENTIAL ENERGY CALCULATIONS (k-nearest neighbors)
# ============================================================================

def k_nearest_indices(point_idx, points, k):
    """
    Find indices of k nearest neighbors on torus.
    
    Args:
        point_idx: index of reference point
        points: array of all point positions
        k: number of neighbors to find
        
    Returns:
        np.array: indices of k nearest neighbors
    """
    n = len(points)
    if n <= 1 or k <= 0:
        return np.array([])
    
    reference = points[point_idx]
    
    # Calculate squared distances to all other points
    distances_sq = []
    for i, other_point in enumerate(points):
        if i != point_idx:
            dist_sq = torus_distance_sq(reference, other_point)
            distances_sq.append((dist_sq, i))
    
    # Sort by distance and take k smallest
    distances_sq.sort(key=lambda x: x[0])
    k = min(k, len(distances_sq))
    
    return np.array([i for _, i in distances_sq[:k]])


def riesz_potential_k(point_idx, points, s, k):
    """
    Calculate Riesz potential energy from k-nearest neighbors.
    Energy = sum over k-nearest of 1/distance^s
    
    Args:
        point_idx: index of point to evaluate
        points: array of all point positions
        s: Riesz exponent
        k: number of nearest neighbors
        
    Returns:
        float: Riesz potential from k neighbors
    """
    if k <= 0:
        return 0.0
    
    reference = points[point_idx]
    neighbor_indices = k_nearest_indices(point_idx, points, k)
    
    energy = 0.0
    for neighbor_idx in neighbor_indices:
        dist_sq = torus_distance_sq(reference, points[neighbor_idx])
        if dist_sq > 1e-10:
            energy += 1.0 / (dist_sq ** (s / 2.0))
    
    return energy


def riesz_gradient_k(point_idx, points, s, k):
    """
    Calculate gradient of Riesz potential from k-nearest neighbors.
    
    Args:
        point_idx: index of point to evaluate
        points: array of all point positions
        s: Riesz exponent
        k: number of nearest neighbors
        
    Returns:
        np.array: gradient vector
    """
    n = len(points)
    if n <= 1 or k <= 0:
        return np.zeros(DIM)
    
    reference = points[point_idx]
    neighbor_indices = k_nearest_indices(point_idx, points, k)
    
    gradient = np.zeros(DIM)
    for neighbor_idx in neighbor_indices:
        displacement = torus_displacement(reference, points[neighbor_idx])
        dist_sq = np.sum(displacement ** 2)
        if dist_sq > 1e-10:
            divisor = dist_sq ** ((s + 2) / 2.0)
            gradient += displacement / divisor
    
    return gradient


# ============================================================================
# POINT-WISE ENERGY GRADIENT WITH DENSITY WEIGHTING
# ============================================================================

def pointwise_gradient(point_idx, points, s, k, w, w_grad):
    """
    Calculate total gradient experienced by a point using product rule.
    
    Combines Riesz potential gradient and density weight gradient:
    ∇E = (∇F) * w(x) + F(x) * (∇w)
    
    where F is Riesz potential and w is weight function.
    
    Args:
        point_idx: index of point
        points: array of all point positions
        s: Riesz exponent
        k: number of nearest neighbors
        w: weight function
        w_grad: weight gradient function
        
    Returns:
        np.array: gradient vector
    """
    point = points[point_idx]
    
    # Get Riesz potential and its gradient
    riesz_potential = riesz_potential_k(point_idx, points, s, k)
    riesz_grad = riesz_gradient_k(point_idx, points, s, k)
    
    # Get weight and its gradient
    w_val = w(point)
    w_grad_val = w_grad(point)
    
    # Product rule: (F * w)' = F' * w + F * w'
    total_grad = riesz_grad * w_val + riesz_potential * w_grad_val
    
    return total_grad


# ============================================================================
# SIMULATION STEP FUNCTION
# ============================================================================

def step_state_torus(points, maxstep, s, k, density_type, gaussian_sigma, noise_level, particle_density_params=None):
    """
    Perform one gradient descent step on the torus.
    
    Process:
    1. Calculate gradient for each point independently
    2. Normalize step sizes so fastest particle moves exactly maxstep
    3. Add Gaussian noise if requested
    4. Wrap coordinates to maintain torus topology
    
    Args:
        points: array of shape (n, 2) with point positions
        maxstep: upper bound on distance any point can move
        s: Riesz exponent
        k: number of nearest neighbors
        density_type: 'uniform' or 'gaussian'
        gaussian_sigma: sigma for Gaussian distribution
        noise_level: amount of Gaussian noise to add (0 = none, 1 = high)
        
    Returns:
        np.array: updated point positions
    """
    n = len(points)
    if n == 0:
        return points
    
    density_metadata = normalize_particle_density_params(
        particle_density_params, n, density_type, gaussian_sigma
    )
    weight_function_cache = {}
    
    # Calculate gradient for each point
    gradients = np.zeros_like(points)
    max_step_magnitude = 0
    
    for i in range(n):
        density_config = density_metadata[i]
        cache_key = (density_config['densityType'], density_config['gaussianSigma'])
        if cache_key not in weight_function_cache:
            weight_function_cache[cache_key] = get_weight_functions(
                s, DIM, density_config['densityType'], density_config['gaussianSigma']
            )
        w, w_grad = weight_function_cache[cache_key]

        grad = pointwise_gradient(i, points, s, k, w, w_grad)
        gradients[i] = grad
        
        # Track maximum step magnitude for normalization
        step_magnitude = np.linalg.norm(grad)
        max_step_magnitude = max(max_step_magnitude, step_magnitude)
    
    # Normalize step sizes to respect maxstep
    if max_step_magnitude > 0:
        dampening = min(maxstep / max_step_magnitude, 1.0)
    else:
        dampening = 1.0
    
    # Apply step and add noise
    new_points = points + gradients * dampening
    
    # Add Gaussian noise if requested
    if noise_level > 0:
        noise = np.random.normal(0, 0.1 * noise_level, size=points.shape)
        new_points += noise
    
    # Wrap coordinates to torus [-1, 1]^2
    # Formula: ((x + 1) % 2) - 1 maps any value to [-1, 1]
    new_points = ((new_points + 1) % 2) - 1
    
    return new_points


# ============================================================================
# STATISTICS CALCULATIONS
# ============================================================================

def calculate_total_energy(points, s, k, density_type, gaussian_sigma, particle_density_params=None):
    """
    Calculate total Riesz potential energy of the system.
    
    Args:
        points: array of point positions
        s: Riesz exponent
        k: number of nearest neighbors
        density_type: 'uniform' or 'gaussian'
        gaussian_sigma: sigma for Gaussian distribution
        
    Returns:
        float: total energy
    """
    if len(points) == 0:
        return 0.0
    
    density_metadata = normalize_particle_density_params(
        particle_density_params, len(points), density_type, gaussian_sigma
    )
    weight_function_cache = {}
    
    total_energy = 0.0
    for i in range(len(points)):
        density_config = density_metadata[i]
        cache_key = (density_config['densityType'], density_config['gaussianSigma'])
        if cache_key not in weight_function_cache:
            weight_function_cache[cache_key] = get_weight_functions(
                s, DIM, density_config['densityType'], density_config['gaussianSigma']
            )
        w, _ = weight_function_cache[cache_key]

        riesz_pot = riesz_potential_k(i, points, s, k)
        weight = w(points[i])
        total_energy += riesz_pot * weight
    
    return total_energy


def calculate_volume_rsd(points, density_type, gaussian_sigma, particle_density_params=None):
    """
    Calculate relative standard deviation of particle volumes.
    
    For each point:
    - Find nearest neighbor distance d
    - Calculate "volume": p(x) * d^2
    - In theory, this should be constant across all points
    
    Returns the relative standard deviation (std / mean) of volumes.
    
    Args:
        points: array of point positions
        density_type: 'uniform' or 'gaussian'
        gaussian_sigma: sigma for Gaussian distribution
        
    Returns:
        float: relative standard deviation
    """
    if len(points) < 2:
        return 0.0
    
    density_metadata = normalize_particle_density_params(
        particle_density_params, len(points), density_type, gaussian_sigma
    )
    density_function_cache = {}
    
    volumes = []
    for idx, point in enumerate(points):
        density_config = density_metadata[idx]
        cache_key = (density_config['densityType'], density_config['gaussianSigma'])
        if cache_key not in density_function_cache:
            density_function_cache[cache_key], _ = get_density_functions(
                density_config['densityType'], density_config['gaussianSigma']
            )
        p = density_function_cache[cache_key]

        min_dist = min_distance_to_neighbors(point, points)
        density = p(point)
        # Volume = density * distance^2
        volume = density * (min_dist ** 2)
        volumes.append(volume)
    
    volumes = np.array(volumes)
    mean_vol = np.mean(volumes)
    
    if mean_vol < 1e-10:
        return 0.0
    
    std_vol = np.std(volumes)
    rsd = std_vol / mean_vol
    
    return rsd


# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/step', methods=['POST'])
def step_endpoint():
    """
    Main simulation step endpoint.
    
    Receives JSON with:
    - particles: array of [x, y] positions
    - s: Riesz exponent
    - k: number of nearest neighbors
    - n: total number of points (informational)
    - maxstep: maximum step size
    - noise: noise level
    - densityType: 'uniform' or 'gaussian'
    - gaussianSigma: sigma for Gaussian
    - calculateEnergy: whether to compute total energy
    - calculateVolumeRsd: whether to compute volume RSD
    
    Returns JSON with:
    - particles: updated positions
    - energy: (optional) total Riesz energy if requested
    - volumeRsd: (optional) volume RSD if requested
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        particles = np.array(data.get('particles', []))
        s = float(data.get('s', 3.0))
        k = int(data.get('k', 6))
        maxstep = float(data.get('maxstep', 0.02))
        noise = float(data.get('noise', 0.0))
        density_type = data.get('densityType', 'uniform')
        gaussian_sigma = float(data.get('gaussianSigma', 1.0))
        calculate_energy = data.get('calculateEnergy', False)
        should_calculate_volume_rsd = data.get('calculateVolumeRsd', False)
        
        # Validate inputs
        if len(particles) == 0:
            return jsonify({
                'particles': [],
                'particleDensityParams': [],
                'energy': None,
                'volumeRsd': None
            })
        
        particle_density_params = normalize_particle_density_params(
            data.get('particleDensityParams', []), len(particles), density_type, gaussian_sigma
        )

        # Ensure k doesn't exceed n
        k = min(k, len(particles))
        k = max(k, 1)  # At least 1 neighbor
        
        # Perform simulation step
        new_particles = step_state_torus(
            particles, maxstep, s, k,
            density_type, gaussian_sigma, noise, particle_density_params
        )
        
        # Calculate statistics if requested
        energy = None
        volume_rsd = None
        
        if calculate_energy:
            energy = float(calculate_total_energy(
                new_particles, s, k, density_type, gaussian_sigma, particle_density_params
            ))
        
        if should_calculate_volume_rsd:
            volume_rsd = float(calculate_volume_rsd(
                new_particles, density_type, gaussian_sigma, particle_density_params
            ))
        
        # Return response
        return jsonify({
            'particles': new_particles.tolist(),
            'particleDensityParams': particle_density_params,
            'energy': energy,
            'volumeRsd': volume_rsd
        })
    
    except Exception as e:
        print(f"Error in /step endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for verifying backend is running.
    """
    return jsonify({'status': 'ok', 'message': 'Backend is running'})


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("Riesz Potential Particle Simulator - Flask Backend")
    print("=" * 70)
    print("\nConstants:")
    print(f"  Dimension: {DIM}")
    print(f"  Mystery Constant (density weighting): {MYSTERY_CONST}")
    print("\nEndpoints:")
    print("  POST /step           - Perform one simulation step")
    print("  GET  /health         - Health check")
    print("\nStarting Flask server on http://localhost:5000")
    print("Make sure the frontend (index.html) is served on the same host.")
    print("=" * 70)
    print()
    
    # Start Flask development server
    # In production, use a WSGI server like gunicorn instead:
    # gunicorn -w 1 -b 0.0.0.0:5000 app:app
    app.run(debug=True, host='localhost', port=5000)
