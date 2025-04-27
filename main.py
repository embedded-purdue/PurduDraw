import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

from image import *
from simulate import *

import time

def main():

    # set image name
    image_name = "pikachu"
    ex = ".jpg"
    
    # load image
    image = load_image(image_name + ex)

    # create graph from image
    graph = image_to_graph(image, image_name + "_graph" + ex)

    # run TSP algorithm
    path = tsp(graph)

    # simulate
    # draw_path(path, image_name + "_path" + ex)

    data = delta_path(path)

    # print("Running Chinese Postman")
    # start = time.time()
    # # path = tsp(graph, method)
    # edge_path = cpp(graph)
    # end = time.time()
    # print("Postman executed in", end-start, "seconds")
    # draw_edgepath(edge_path, image_name + "_postman_path"  + ex)
    # # draw_path(path, image_name + "_postman_path"  + ex)

    print("Done.")


if __name__ == "__main__":
    main()
