import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # Gravitational constant (m³ kg⁻¹ s⁻²)
m_sun = 1.989e30  # Sun mass (kg)
m_earth = 5.972e24  # Earth mass (kg)
m_moon = 7.348e22  # Moon mass (kg)

# Initial positions and velocities
au = 1.496e11  # Astronomical unit (meters)
earth_orbit_radius = au
moon_orbit_radius = 3.844e8  # Earth-Moon distance (meters)

sun_pos = np.array([0.0, 0.0])
earth_pos = np.array([earth_orbit_radius, 0.0])
moon_pos = earth_pos + np.array([moon_orbit_radius, 0.0])

# Velocities for circular orbits
v_earth = np.sqrt(G * m_sun / earth_orbit_radius)
v_moon = np.sqrt(G * m_earth / moon_orbit_radius)

earth_vel = np.array([0.0, v_earth])
moon_vel = earth_vel + np.array([0.0, v_moon])

# Simulation parameters
dt = 3600  # Time step: 1 hour (seconds)
num_steps = 500  # Number of animation frames

# Create grid for spacetime visualization
x = np.linspace(-1.5*au, 1.5*au, 50)
y = np.linspace(-1.5*au, 1.5*au, 50)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

# Function to compute gravitational potential
def compute_potential(X, Y, sun_pos, earth_pos):
    r_sun = np.sqrt((X - sun_pos[0])**2 + (Y - sun_pos[1])**2 + 1e-10)
    r_earth = np.sqrt((X - earth_pos[0])**2 + (Y - earth_pos[1])**2 + 1e-10)
    phi_sun = -G * m_sun / r_sun
    phi_earth = -G * m_earth / r_earth
    return phi_sun + phi_earth

# Initialize figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 1]})

# Spacetime curvature plot (left)
Z = compute_potential(X, Y, sun_pos, earth_pos)
cf = ax1.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(cf, ax=ax1, label='Gravitational Potential')
ax1.set_title('Spacetime Curvature (2D Slice)')
ax1.set_xlabel('X (meters)')
ax1.set_ylabel('Y (meters)')

# Orbital plot (right)
ax2.set_xlim(-1.5*au, 1.5*au)
ax2.set_ylim(-1.5*au, 1.5*au)
ax2.set_aspect('equal')
ax2.set_title('Orbital Motion')
ax2.set_xlabel('X (meters)')
ax2.set_ylabel('Y (meters)')

# Plot celestial bodies
sun_dot, = ax2.plot(0, 0, 'o', color='yellow', markersize=15, label='Sun')
earth_dot, = ax2.plot(earth_pos[0], earth_pos[1], 'o', color='blue', markersize=5, label='Earth')
moon_dot, = ax2.plot(moon_pos[0], moon_pos[1], 'o', color='gray', markersize=3, label='Moon')
ax2.legend()

# Store trajectories
earth_trajectory_x, earth_trajectory_y = [], []
moon_trajectory_x, moon_trajectory_y = [], []
earth_line, = ax2.plot([], [], color='blue', alpha=0.5)
moon_line, = ax2.plot([], [], color='gray', alpha=0.5)

# Animation update function
def update(frame):
    global earth_pos, earth_vel, moon_pos, moon_vel

    # Update Earth's position (Euler-Cromer method)
    r_earth_sun = earth_pos - sun_pos
    dist_es = np.linalg.norm(r_earth_sun) + 1e-10
    force_es = -G * m_sun * m_earth / dist_es**3 * r_earth_sun
    earth_vel += (force_es / m_earth) * dt
    earth_pos += earth_vel * dt

    # Update Moon's position relative to Earth
    r_moon_earth = moon_pos - earth_pos
    dist_me = np.linalg.norm(r_moon_earth) + 1e-10
    force_me = -G * m_earth * m_moon / dist_me**3 * r_moon_earth
    moon_vel += (force_me / m_moon) * dt
    moon_pos += moon_vel * dt

    # Update spacetime curvature plot
    Z = compute_potential(X, Y, sun_pos, earth_pos)
    ax1.clear()
    cf = ax1.contourf(X, Y, Z, levels=50, cmap='viridis')
    ax1.set_title('Spacetime Curvature (2D Slice)')
    ax1.set_xlabel('X (meters)')
    ax1.set_ylabel('Y (meters)')

    # Update orbital plot
    earth_dot.set_data(earth_pos[0], earth_pos[1])
    moon_dot.set_data(moon_pos[0], moon_pos[1])

    # Update trajectories
    earth_trajectory_x.append(earth_pos[0])
    earth_trajectory_y.append(earth_pos[1])
    moon_trajectory_x.append(moon_pos[0])
    moon_trajectory_y.append(moon_pos[1])

    earth_line.set_data(earth_trajectory_x, earth_trajectory_y)
    moon_line.set_data(moon_trajectory_x, moon_trajectory_y)

    return earth_dot, moon_dot, earth_line, moon_line

# Create animation
ani = FuncAnimation(fig, update, frames=num_steps, interval=50, blit=False)

plt.tight_layout()
plt.show()
