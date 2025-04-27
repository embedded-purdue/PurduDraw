from PIL import Image, ImageOps, ImageFilter
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import cv2
import csv

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

    raw_img = np.array(image)
    laplaced = cv2.Laplacian(raw_img, cv2.CV_8U)
    # plt.imshow(laplaced,cmap = 'gray')
    # plt.show()

    gray = cv2.cvtColor(laplaced, cv2.COLOR_RGB2GRAY)
    # plt.imshow(gray,cmap = 'gray')
    # plt.show()

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

    nx.draw(graph, nodes, node_size=10)
    print("nodes: ", len(nodes))
    plt.show()

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

    # connect all components
    # components = list(nx.connected_components(graph))
    # while(len(components) > 1):
    #     min_dist = float("inf")
    #     min_edge = None
    #     for pair1 in components[0]:
    #         for pair2 in components[1]:
    #             dist = np.sqrt((pair1[0] - pair2[0]) ** 2 + (pair1[1] - pair2[1]) ** 2)
    #             if dist < min_dist:
    #                 min_dist = dist
    #                 min_edge = (pair1, pair2)
    #     graph.add_edge(min_edge[0], min_edge[1], weight=min_dist)
    #     components = list(nx.connected_components(graph))
    #     print("Connecting components... {} components left".format(len(components)))

    components = list(nx.connected_components(graph))
    while len(components) > 1:
        components = sorted(components, key=len)
        small_comp = components[0]
        rest_nodes = set().union(*components[1:])
        best_dist = float("inf")
        best_edge = None
        for node in small_comp:
            for other in rest_nodes:
                dist = np.hypot(node[0] - other[0], node[1] - other[1])
                if dist < best_dist:
                    best_dist = dist
                    best_edge = (node, other)
        if best_edge:
            graph.add_edge(best_edge[0], best_edge[1], weight=best_dist)
        components = list(nx.connected_components(graph))
        print(f"Connecting components... {len(components)} components left")

    nx.draw(graph, nodes, node_size=10)
    plt.show()
    plt.savefig("processed/" + image_name)
        
    return graph

def dfs(graph, start_node=(0, 600)):
    """
    Perform DFS traversal, walking along edges properly (no teleporting).
    """

    visited = set()
    path = []
    stack = [start_node]

    while stack:
        current = stack.pop()
        if current not in visited:
            if path:
                # Find shortest path between last node and current
                try:
                    sp = nx.shortest_path(graph, source=path[-1], target=current, weight='weight')
                    path.extend(sp[1:])  # Skip first node (already at path[-1])
                except nx.NetworkXNoPath:
                    pass  # No path, skip (shouldn't happen if graph is fully connected)
            else:
                path.append(current)

            visited.add(current)

            neighbors = list(graph.neighbors(current))
            neighbors.sort(key=lambda n: np.linalg.norm(np.array(current) - np.array(n)))

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

    return path


def delta_path(path, filename="delta_path.csv"):

    d_path = []
    for i in range(len(path)):
        if i == 0:
            continue
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        d_path.append((dx, dy))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(d_path)

    return d_path

