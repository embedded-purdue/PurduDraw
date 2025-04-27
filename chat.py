import cv2
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Step 1: Load and Edge Detect
img = cv2.imread('images/subaru.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (500, 500))
edges = cv2.Canny(img, 50, 150)

# Step 2: Find points
points = np.column_stack(np.where(edges > 0))

# Step 3: Build graph based on 8-neighbor connectivity
G = nx.Graph()
for idx, (y, x) in enumerate(points):
    G.add_node(idx, pos=(x, y))

# Connect nearby points (within some radius)
radius = 5  # adjust this
for i in range(len(points)):
    for j in range(i+1, len(points)):
        if np.linalg.norm(points[i] - points[j]) <= radius:
            G.add_edge(i, j)

# Step 4: DFS to make a path
start_node = 0
path = []
visited = set()

def dfs_iterative(start):
    stack = [start]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            path.append(u)
            neighbors = list(G.neighbors(u))
            stack.extend(neighbors)

dfs_iterative(start_node)

# Step 5: Convert path indices back to coordinates
path_points = points[path]

# Step 6: Plot the path
plt.plot(path_points[:,1], path_points[:,0], linewidth=0.5)
plt.gca().invert_yaxis()
plt.axis('equal')
plt.show()