import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib.animation import FuncAnimation

# Fetching tidal data from the webpage
url = "https://www.hko.gov.hk/tide/WAGtextPH2025.htm"
response = requests.get(url)
tables = pd.read_html(response.text)
df = tables[0]  # Assuming the first table contains the desired data

# Cleaning the data
df_cleaned = df.iloc[2:, :].reset_index(drop=True)
tide_heights = df_cleaned.iloc[:, 1:].replace('---', np.nan).astype(float).values  # Convert to float
hours = np.arange(1, 25)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor('#2c2c2c')  # Dark background

# Create a color gradient for the sine waves
colors = plt.cm.viridis(np.linspace(0, 1, tide_heights.shape[1]))


# Animation function
def update(frame):
    ax.clear()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw sine waves with varying amplitude and color
    for j in range(tide_heights.shape[1]):
        x = np.linspace(-1, 1, 100) + (j / (tide_heights.shape[1] - 1)) * 2 - 1  # Adjust x position
        height = tide_heights[frame % tide_heights.shape[0], j]
        y = np.sin(x * (frame + j) * 2) * (height / 3)  # Dynamic height

        # Set alpha based on height, ensuring it's within the valid range
        alpha = max(0, min(0.8 * (height / 3), 1)) if not np.isnan(height) else 0
        ax.plot(x, y, color=colors[j], linewidth=3, alpha=alpha)

    # Add circular waves
    theta = np.linspace(0, 2 * np.pi, 100)
    radius = (frame % 30) / 30  # Changing radius
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color='cyan', alpha=0.3)

    # Create a dynamic starry background
    for _ in range(100):  # Adjust number of stars
        star_x = np.random.uniform(-1.5, 1.5)
        star_y = np.random.uniform(-1.5, 1.5)
        ax.scatter(star_x, star_y, color='white', s=np.random.randint(10, 30), alpha=np.random.rand())

    # Add a title
    ax.set_title('Dynamic Tidal Data Visualization', fontsize=28, color='white', fontweight='bold', loc='center')


# Create the animation
animation = FuncAnimation(fig, update, interval=100)
plt.show()