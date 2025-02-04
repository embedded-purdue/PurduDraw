import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

from image import *
from simulate import *

def main():

    # set image name
    image_name = "purdue_logo"
    ex = ".png"
    
    # load image
    image = load_image(image_name + ex)

    # create graph from image
    graph = image_to_graph(image, image_name + "_graph" + ex, threshold=0.2, size=(90, 60), invert=True)

    # # run TSP algorithm
    # path = tsp(graph)

    # # simulate
    # draw_path(path, image_name + "_path" + ex)
    methods = [(nx.approximation.greedy_tsp, "greedy_tsp"),
               (nx.approximation.christofides, "christofides")]
    for method, method_name in methods:
        print("Running", method_name)
        path = tsp(graph, method)
        draw_path(path, image_name + "_" + method_name + "_path"  + ex)

    print("Done.")


if __name__ == "__main__":
    main()
