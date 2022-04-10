# https://towardsdatascience.com/simple-but-stunning-animated-cellular-automata-in-python-c912e0c156a9
import numpy as np
import matplotlib.pyplot as plt
import ffmpeg
from IPython.display import HTML

Glidergun = np.loadtxt('gosbel', dtype=np.int8)
plt.imshow(Glidergun, cmap='Greys')

def tick(matrix):
    new_state = np.copy(matrix)
    for i in range(np.size(matrix,0)-1):
        for j in range(np.size(matrix,1)-1):
            north = matrix[i][j-1] if j>0 else 0
            south = matrix[i][j+1] if j<np.size(matrix,1)-2 else 0
            west = matrix[i+1][j] if i<np.size(matrix,0)-2 else 0
            east = matrix[i-1][j] if i>0 else 0
            se = matrix[i+1][j+1] if i<np.size(matrix,0)-2 and j<np.size(matrix,1)-2 else 0
            sw = matrix[i+1][j-1] if i<np.size(matrix,0)-2 and j>0 else 0
            ne = matrix[i-1][j+1] if i>0 and j<np.size(matrix,1)-2 else 0
            nw = matrix[i-1][j-1] if i>0 and j>0 else 0

            neighbours = np.sum([north, south, east, west, se, sw, ne, nw])

            #rules
            
            
                        