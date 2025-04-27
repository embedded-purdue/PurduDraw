from PIL import Image, ImageOps, ImageFilter
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

def reshape(image: Image.Image, size, padding=10):
    
    target_w, target_h = size

    # Calculate target area after removing padding
    inner_w = target_w - 2 * padding
    inner_h = target_h - 2 * padding

    # Resize while preserving aspect ratio
    image.thumbnail((inner_w, inner_h), Image.Resampling.LANCZOS)

    # Create white background and paste image centered
    bg = Image.new("RGB", (inner_w, inner_h), "white")
    offset = ((inner_w - image.width) // 2, (inner_h - image.height) // 2)
    bg.paste(image, offset)

    # Add outer padding
    final = ImageOps.expand(bg, border=padding, fill="white")
    return final
   
def image_to_graph(image: Image.Image, image_name, size=(850, 600)):
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
    image = reshape(image, size=size)
    raw_img = np.array(image)

    # image = image.filter(ImageFilter.GaussianBlur(radius=0))
    # plt.imshow(image,cmap='gray')
    # plt.show()
    raw_img = np.array(image)
    laplaced = cv2.Laplacian(raw_img, cv2.CV_8U)
    # plt.imshow(laplaced,cmap = 'gray')
    # plt.show()

    gray = cv2.cvtColor(laplaced, cv2.COLOR_RGB2GRAY)
    plt.imshow(gray,cmap = 'gray')
    plt.show()

    graph = nx.Graph()
    nodes = dict()
    nx.MultiGraph
    
    # add nodes for light pixels
    for y in range(gray.shape[0]):
        for x in range(gray.shape[1]):
            if (gray[y,x] > 100):
                nodes[(x, size[1] - y)] = (x, size[1] - y)
    nodes[(0, size[1])] = (0, size[1])
    graph.add_nodes_from(nodes.keys())

    # connect neighboring nodes
    for (x, y) in nodes:
        nc = 0
        for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if p in nodes:
                dist = np.sqrt((x - p[0]) ** 2 + (y - p[1]) ** 2)
                graph.add_edge((x, y), p, weight=dist)
                nc += 1
        if (nc == 0):
            for p in ((x + 1, y + 1), (x - 1, y + 1), (x + 1, y + 1), (x - 1, y - 1)):
                if p in nodes:
                    dist = np.sqrt((x - p[0]) ** 2 + (y - p[1]) ** 2)
                    graph.add_edge((x, y), p, weight=dist)
                    nc += 1

        
        # neighbor_count = 0
        # for dx in [-1, 0, 1]:
        #     for dy in [-1, 0, 1]:
        #         if dx == 0 and dy == 0:
        #             continue
        #         neighbor = (x + dx, y + dy)
        #         if neighbor in nodes:
        #             neighbor_count += 1
        #             dist = np.sqrt(dx ** 2 + dy ** 2)
        #             graph.add_edge((x, y), neighbor, weight=dist)
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

    nx.draw(graph, nodes, node_size=10)
    plt.show()
    plt.savefig("processed/" + image_name)
        
    return graph

def tsp(graph, start_node=(0, 600), method=nx.approximation.greedy_tsp):
    """
    Run the traveling salesman problem algorithm.
    
    Args:
        graph: a networkx graph object
        
    Returns:
    """

    # print("Running TSP algorithm...")
    # return nx.approximation.traveling_salesman_problem(graph, method=method, cycle=False)

    print("Quick walk (running)...")
    if start_node is None:
        start_node = list(graph.nodes)[0]
    path = [start_node]
    visited = set(path)

    for u, v in nx.dfs_edges(graph, source=start_node):
        if v not in visited:
            path.append(v)
            visited.add(v)

    return path
    
def make_dict(nodelist):
    dict = {}
    for node in nodelist:
        dict[node] = node
    return dict

def delta_path(path):

    d_path = []
    for i in range(len(path)):
        if i == 0:
            continue
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        d_path.append((dx, dy))
    return d_path

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

