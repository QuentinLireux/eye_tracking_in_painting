import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np



class Video:
    
    def __init__(self, coord, image_path, screen, coord_image):
        self.coord = np.loadtxt(coord, delimiter=',')
        self.screen = screen
        self.coord_image = coord_image
        print(image_path)
        self.img = plt.imread(image_path)
        
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], color='blue', lw=1)
    
    
    def initialisation(self):
        #Place l'image dans l'ecran
        self.ax.imshow(self.img, extent=[self.coord_image[0][0],
                                         self.coord_image[1][0],
                                         self.coord_image[0][1],
                                         self.coord_image[1][1]],
                        )#aspect='auto'
        self.line.set_data([], [])
        return self.line,
    
    def update(self, i):
        self.line.set_data(self.coord[:(1*i),0],self.screen[1]-self.coord[:(1*i),1])    
        return self.line,
    
    def make_video(self):
        #self.ax.imshow(self.img, extent=[0, 1920, 0, 1200], aspect='auto')
        self.ax.axis([0, self.screen[0], 0, self.screen[1]])
        x, y = self.coord.shape
        anim = animation.FuncAnimation(self.fig, self.update, x, init_func=self.initialisation, blit=True)
        anim.save("video.mp4", fps=15)
        return "video.mp4"