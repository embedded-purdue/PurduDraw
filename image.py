from PIL import Image
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import cv2

def load_image(image_name):
    try:
        path = "images/" + image_name
        image = Image.open(path).convert("L")
        return image
    except IOError:
        print("Unable to load image")
        return None
    
def image_to_graph(image: Image.Image, image_name, threshold=0.5, size=(60, 40), invert=False):
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
    # image = image.resize(size)

    t = 255 * threshold
    raw_img = np.array(image)

    print(raw_img)
    laplaced = cv2.Laplacian(raw_img, cv2.CV_8U)
    _,thresholded = cv2.threshold(laplaced, t, 255, cv2.THRESH_BINARY)
    # print(laplaced)
    plt.imshow(laplaced,cmap = 'gray')
    plt.imshow(thresholded,cmap = 'gray')
    plt.show()
    pixels = thresholded

    rows, cols = pixels.shape
    graph = nx.Graph()
    nodes = dict()
    nx.MultiGraph
    
    # add nodes for dark pixels
    for y in range(rows):
        for x in range(cols):
            brightness = pixels[y,x]
            if ((not invert) and (brightness <= t)) or ((invert and (brightness >= t))):
                nodes[(x, rows - y)] = (x, rows - y)
    graph.add_nodes_from(nodes.keys())

    # keep_lines = "horiz"
    # keep_lines = "vert"

    # connect neighboring nodes
    for (x, y) in nodes:
        neighbor_count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                if neighbor in nodes:
                    neighbor_count += 1
                    dist = np.sqrt(dx ** 2 + dy ** 2)
                    graph.add_edge((x, y), neighbor, weight=dist)
        # # If we're in the middle of the graph, the fastest route is basically always gonna be straight up/down
        # # So, just remove all other edges, and give the tsp less to search thru
        # if neighbor_count == 8:
        #     for dx in [-1, 0, 1]:
        #         for dy in [-1, 0, 1]:
        #             # remove everything where we are moving sideways
        #             if (keep_lines == "vert" and dx != 0) or (keep_lines == "horiz" and dy == 0):
        #                 neighbor = (x + dx, y + dy)
        #                 graph.remove_edge((x,y), neighbor)

    # connect all components
    components = list(nx.connected_components(graph))
    while(len(components) > 1):
        min_dist = float("inf")
        min_edge = None
        for pair1 in components[0]:
            for pair2 in components[1]:
                dist = np.sqrt((pair1[0] - pair2[0]) ** 2 + (pair1[1] - pair2[1]) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    min_edge = (pair1, pair2)
        graph.add_edge(min_edge[0], min_edge[1], weight=min_dist)
        components = list(nx.connected_components(graph))
        print("Connecting components... {} components left".format(len(components)))

    print(nodes)
    nx.draw(graph, nodes, node_size=10)
    plt.show()
    plt.savefig("processed/" + image_name)
        
    return graph

def tsp(graph, method=nx.approximation.greedy_tsp):
    """
    Run the traveling salesman problem algorithm.
    
    Args:
        graph: a networkx graph object
        
    Returns:
    """

    print("Running TSP algorithm...")
    return nx.approximation.traveling_salesman_problem(graph, method=method, cycle=False)
    
def make_dict(nodelist):
    dict = {}
    for node in nodelist:
        dict[node] = node
    return dict

def cpp(graph: nx.Graph):

    # nx.draw(graph, node_size=10)
    # plt.show()
    # print(graph.nodes)
    nx.draw(graph, make_dict(graph.nodes), node_size=10)
    plt.show()

    print("    eulerizing...", end="", flush=True)
    eulerized = nx.eulerize(graph)
    print("eulerized!")
    nx.draw(eulerized, make_dict(eulerized.nodes), node_size=10)
    plt.show()
    print("    finding circuit...")
    return nx.eulerian_circuit(eulerized)

