import matplotlib.pyplot as plt

def draw_path(path, image_name):
    """
    Draw a path on an image.
    
    Args:
        path: a list of (x, y) tuples
        image_name: the name of the output image file
    """

    x, y = zip(*path)
    plt.figure()
    plt.plot(x, y, linestyle='-', color='black')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("processed/" + image_name)
    plt.show()
