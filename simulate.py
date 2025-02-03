import matplotlib.pyplot as plt

def draw_path(path, image_name):
    """
    Simulate a path using turtle graphics and save the image.
    
    Args:
        path (list of tuples): List of (x, y) coordinates to follow.
        image_name (str): Name of the file to save the drawing.
    """

    x, y = zip(*path)

    # Plot the path
    plt.figure()
    plt.plot(x, y, linestyle='-', color='black')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Path Visualization")
    plt.grid(True)
    plt.savefig("processed/" + image_name)
    plt.show()
