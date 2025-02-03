from PIL import Image
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def load_image(image_name):
    try:
        path = "images/" + image_name
        image = Image.open(path).convert("RGBA")
        return image
    except IOError:
        print("Unable to load image")
        return None
    
def image_to_graph(image, image_name, threshold=0.5, size=(200, 300)):
    """
    Create a graph from an image.
    
    Args:
        image: a PIL Image object
        image_name: the name of the image file
        threshold: the threshold for pixel brightness
        
    Returns:
        graph: a networkx graph object
    """
    
    # resize the image
    image = image.resize(size)

    t = 255 * threshold
    pixels = image.load()
    width, height = image.size
    graph = nx.Graph()
    nodes = dict()
    
    # add nodes for dark pixels
    for y in range(0, height, 1):
        for x in range(0, width, 1):
            r, g, b, a = pixels[x, y]
            brightness = (r + g + b) / 3
            if brightness > t:
                nodes[(x, height - y)] = (x, height - y)
    graph.add_nodes_from(nodes.keys())

    # connect neighboring nodes
    for (x, y) in nodes:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                if neighbor in nodes:
                    dist = np.sqrt(dx ** 2 + dy ** 2)
                    graph.add_edge((x, y), neighbor, weight=dist)

    nx.draw(graph, nodes, node_size=1)
    plt.savefig("processed/" + image_name)

    return graph

def tsp(graph, method="christofides"):
    """
    Run the traveling salesman problem algorithm.
    
    Args:
        graph: a networkx graph object
        
    Returns:
    """

    return nx.approximation.traveling_salesman_problem(graph, cycle=False)

    