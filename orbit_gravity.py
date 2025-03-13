import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Constants
G = 6.67430e-11  # Gravitational constant (m³ kg⁻¹ s⁻²)
m_sun = 1.989e30  # Sun mass (kg)
m_earth = 5.972e24  # Earth mass (kg)
m_moon = 7.348e22  # Moon mass (kg)

# Initial positions and velocities (simplified)
au = 1.496e11  # Astronomical unit (meters)
earth_orbit_radius = au
moon_orbit_radius = 3.844e8  # Earth-Moon distance (meters)

# Sun is at origin
sun_pos = np.array([0.0, 0.0, 0.0])

# Earth's initial position and velocity (circular orbit around Sun)
earth_pos = np.array([earth_orbit_radius, 0.0, 0.0])
earth_vel = np.array([0.0, np.sqrt(G * m_sun / earth_orbit_radius), 0.0])

# Moon's initial position and velocity (circular orbit around Earth)
moon_pos = earth_pos + np.array([moon_orbit_radius, 0.0, 0.0])
moon_vel = earth_vel + np.array([0.0, np.sqrt(G * m_earth / moon_orbit_radius), 0.0])

# Simulation parameters
dt = 3600  # Time step: 1 hour (seconds)
num_steps = 500  # Number of steps (adjust for animation length)

# Create grid for spacetime visualization
x = np.linspace(-1.5*au, 1.5*au, 50)
y = np.linspace(-1.5*au, 1.5*au, 50)
X, Y = np.meshgrid(x, y)

# Function to compute gravitational potential
def compute_potential(X, Y, sun_pos, earth_pos):
    r_sun = np.sqrt((X - sun_pos[0])**2 + (Y - sun_pos[1])**2 + 1e-10)
    r_earth = np.sqrt((X - earth_pos[0])**2 + (Y - earth_pos[1])**2 + 1e-10)
    phi_sun = -G * m_sun / r_sun
    phi_earth = -G * m_earth / r_earth
    return phi_sun + phi_earth

# Initialize figure and 3D axis
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Initial potential and surface plot
Z = compute_potential(X, Y, sun_pos, earth_pos)
surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, alpha=0.6, linewidth=0)

# Plot celestial bodies
sun_dot, = ax.plot([sun_pos[0]], [sun_pos[1]], [0], 'o', color='yellow', markersize=15, label='Sun')
earth_dot, = ax.plot([earth_pos[0]], [earth_pos[1]], [0], 'o', color='blue', markersize=5, label='Earth')
moon_dot, = ax.plot([moon_pos[0]], [moon_pos[1]], [0], 'o', color='gray', markersize=3, label='Moon')

ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')
ax.set_zlabel('Gravitational Potential')
ax.set_title('Spacetime Curvature and Orbital Motion')
ax.legend()

# Set axis limits for better visualization
ax.set_xlim(-1.5*au, 1.5*au)
ax.set_ylim(-1.5*au, 1.5*au)
ax.set_zlim(-5e9, 5e9)  # Adjust based on potential scale

# Animation update function
def update(frame):
    global earth_pos, earth_vel, moon_pos, moon_vel

    # Update Earth's position (Euler-Cromer method)
    r_earth_sun = earth_pos[:2] - sun_pos[:2]
    distance_es = np.linalg.norm(r_earth_sun) + 1e-10
    force_es = -G * m_sun * m_earth / distance_es**3 * r_earth_sun
    earth_vel[:2] += (force_es / m_earth) * dt
    earth_pos[:2] += earth_vel[:2] * dt

    # Update Moon's position relative to Earth
    r_moon_earth = moon_pos[:2] - earth_pos[:2]
    distance_me = np.linalg.norm(r_moon_earth) + 1e-10
    force_me = -G * m_earth * m_moon / distance_me**3 * r_moon_earth
    moon_vel[:2] += (force_me / m_moon) * dt
    moon_pos[:2] += moon_vel[:2] * dt

    # Recompute potential and update surface
    Z = compute_potential(X, Y, sun_pos, earth_pos)
    ax.collections.clear()
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, alpha=0.6, linewidth=0)

    # Update body positions
    earth_dot.set_data([earth_pos[0]], [earth_pos[1]])
    earth_dot.set_3d_properties([0])

    moon_dot.set_data([moon_pos[0]], [moon_pos[1]])
    moon_dot.set_3d_properties([0])

    return surf, earth_dot, moon_dot

# Create animation
ani = FuncAnimation(fig, update, frames=num_steps, interval=50, blit=False)

plt.tight_layout()
plt.show()
