import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
m_earth = 5.972e24  # Earth mass (kg)
m_moon = 7.348e22  # Moon mass (kg)
d = 3.844e8  # Average Earth-Moon distance (meters)

# Calculate initial positions relative to the center of mass
total_mass = m_earth + m_moon
r_earth = (m_moon / total_mass) * d
r_moon = (m_earth / total_mass) * d

# Angular velocity for circular orbit
omega = np.sqrt(G * total_mass / d**3)
v_earth = omega * r_earth  # Earth's orbital velocity
v_moon = omega * r_moon    # Moon's orbital velocity

# Initial positions and velocities
earth_pos = np.array([-r_earth, 0.0])
moon_pos = np.array([r_moon, 0.0])
earth_vel = np.array([0.0, v_earth])  # Earth's velocity (upwards)
moon_vel = np.array([0.0, v_moon])    # Moon's velocity (upwards)

# Simulation parameters
dt = 100  # Time step (seconds)
steps = 10000  # Number of steps

# Store positions for plotting
earth_x, earth_y = [], []
moon_x, moon_y = [], []

for _ in range(steps):
    earth_x.append(earth_pos[0])
    earth_y.append(earth_pos[1])
    moon_x.append(moon_pos[0])
    moon_y.append(moon_pos[1])

    # Calculate gravitational force
    r_vector = moon_pos - earth_pos
    distance = np.linalg.norm(r_vector)
    if distance == 0:
        break  # Avoid division by zero

    force_magnitude = G * m_earth * m_moon / distance**2
    force_direction = r_vector / distance
    force_earth = force_magnitude * force_direction
    force_moon = -force_earth

    # Update velocities
    earth_vel += (force_earth / m_earth) * dt
    moon_vel += (force_moon / m_moon) * dt

    # Update positions
    earth_pos += earth_vel * dt
    moon_pos += moon_vel * dt

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(earth_x, earth_y, label='Earth', linewidth=2)
plt.plot(moon_x, moon_y, label='Moon', linewidth=1)
plt.scatter(0, 0, color='black', label='Center of Mass', zorder=5)
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('Earth and Moon Orbits Simulation')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()
