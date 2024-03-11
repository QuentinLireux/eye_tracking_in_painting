import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

with open('coor.txt', 'r') as read_file:
    coordinates = [tuple(map(int, line.strip().split(','))) for line in read_file]

frame_calibration_size = (1880, 950)
coordinates = [(x, -y) for x, y in coordinates]

background = plt.imread("oeuvres/LA_VIERGE_A_L_ENFANT_ENTRE_SAINT_GEORGES_ET_SAINT_JACQUES.jpg")


#x1=487.5&y1=0&x2=1432.5&y2=945
bins = 1000
heatmap, xedges, yedges = np.histogram2d(*zip(*coordinates), bins=(bins, bins))
heatmap_smooth = gaussian_filter(heatmap, sigma=10)
fig, ax = plt.subplots()

#ax.axis("equal")
ax.set_xlim(0, 1880)
ax.set_ylim(-950, 0)

ax.imshow(background,cmap='gray',extent=[487.5, 1432.5, -945, 0] ,aspect='auto')
fig.gca().set_aspect('equal', adjustable='box')
pcm = ax.pcolormesh(xedges, yedges, heatmap_smooth.T, cmap='viridis', shading='auto', alpha=0.7)
fig.colorbar(pcm, ax=ax, label='Nombre de points')

plt.savefig('heatmap.png')
plt.show()
