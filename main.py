import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

from image import *
from simulate import *

def main():

    # set image name
    image_name = "purdue_logo.png"
    
    # load image
    image = load_image(image_name)    

    # create graph from image
    graph = image_to_graph(image, "graph.png", 0.5, (100, 50))

    # run TSP algorithm
    path = tsp(graph)

    # simulate
    draw_path(path, "path.png")


if __name__ == "__main__":
    main()
