import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
import math


class Heatmap: 
    
    
    def __init__(self):
        pass
    
    def make_heatmap(self, coord_image, screen):
        with open('coor.txt', 'r') as read_file:
            coordinates = [tuple(map(int, line.strip().split(','))) for line in read_file]

    
        x1=coord_image[0][0]
        y1=coord_image[0][1]
        x2=coord_image[1][0]
        y2=coord_image[1][1]
        w = screen[0]
        h = screen[1]
        frame_calibration_size = (w, h)
        coordinates = [(x, -y) for x, y in coordinates]

        background = plt.imread("oeuvres/LA_VIERGE_A_L_ENFANT_ENTRE_SAINT_GEORGES_ET_SAINT_JACQUES.jpg")

        
        
        #x1=487.5&y1=0&x2=1432.5&y2=945
        bins = 1000
        heatmap, xedges, yedges = np.histogram2d(*zip(*coordinates), bins=(bins, bins))
        heatmap_smooth = gaussian_filter(heatmap, sigma=10)
        fig, ax = plt.subplots()

        #ax.axis("equal")
        ax.set_xlim(0, w)
        ax.set_ylim(-h, 0)

        ax.imshow(background,cmap='gray',extent=[x1, x2, -y2, y1] ,aspect='auto')
        fig.gca().set_aspect('equal', adjustable='box')
        pcm = ax.pcolormesh(xedges, yedges, heatmap_smooth.T, cmap='viridis', shading='auto', alpha=0.7)
        fig.colorbar(pcm, ax=ax, label='Nombre de points')

        image_path = "heatmap.png"
        plt.savefig(image_path)
        return image_path
    
    def make_heatmap2(self, coord_image, screen):
        
        with open('coor.txt', 'r') as read_file:
            coordinates = [tuple(map(int, line.strip().split(','))) for line in read_file]

        coordinates = [(x, -y) for x, y in coordinates]
        
        x1=int(math.floor(float(coord_image[0][0])))
        y1=int(math.floor(float(coord_image[0][1])))
        x2=int(math.floor(float(coord_image[1][0])))
        y2=int(math.floor(float(coord_image[1][1])))
        w = int(screen[0])
        h = int(screen[1])
        
        
        img_width = math.floor(float(x2)-float(x1))
        img_height = math.floor(float(y2)-float(y1))
        
        tab = np.zeros((h, w))
        
        for x, y in coordinates:
            for i in range(-5, 5):
                for j in range(-5, 5):
                    try:
                        
                        tab[-(y+j)][(x+i)] += 1000
                    except Exception as e:
                        pass
            for i in range(-10, 10):
                for j in range(-10, 10):
                    try:
                        tab[-(y+j)][(x+i)] += 500
                    except Exception as e:
                        pass
            for i in range(-50, 50):
                for j in range(-50, 50):
                    try:
                        tab[-(y+j)][(x+i)] += 100
                    except Exception as e:
                        pass
            for i in range(-100, 100):
                for j in range(-100, 100):
                    try:
                        tab[-(y+j)][(x+i)] += 50
                    except Exception as e:
                        pass
                        
        background = plt.imread("oeuvres/LA_VIERGE_A_L_ENFANT_ENTRE_SAINT_GEORGES_ET_SAINT_JACQUES.jpg")
        fig, ax = plt.subplots()
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)
        ax.imshow(background,cmap='gray',extent=[x1, x2, y2, y1] ,aspect='auto')
        ax.imshow(tab, cmap="viridis", interpolation="nearest", alpha=0.5, vmin=1)
        fig.gca().set_aspect('equal', adjustable='box')
        
        
        image_path = "heatmap.png"
        plt.savefig(image_path)
        return image_path
        