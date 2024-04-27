import numpy as np
import matplotlib.pyplot as plt
import cv2
from queue import PriorityQueue

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def astar(start, end, grid):
    start_node = Node(start)
    end_node = Node(end)
    open_list = PriorityQueue()
    open_list.put(start_node)
    closed_list = set()
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while not open_list.empty():
        current_node = open_list.get()
        closed_list.add(current_node.position)
        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for move in moves:
            neighbor_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])
            if (0 <= neighbor_position[0] < grid.shape[0]) and (0 <= neighbor_position[1] < grid.shape[1]) and grid[neighbor_position[0], neighbor_position[1]] == 0 and neighbor_position not in closed_list:
                neighbor_node = Node(neighbor_position, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = abs(neighbor_position[0] - end_node.position[0]) + abs(neighbor_position[1] - end_node.position[1])
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                if not any(n.position == neighbor_node.position for n in open_list.queue):
                    open_list.put(neighbor_node)

    return None

def create_grid(image, grid_size):
    height, width = image.shape[:2]
    grid = np.zeros((height // grid_size, width // grid_size), dtype=int)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        start_x, end_x = x // grid_size, (x + w) // grid_size
        start_y, end_y = y // grid_size, (y + h) // grid_size
        grid[start_y:end_y + 1, start_x:end_x + 1] = 1

    return grid

start_point = None
end_point = None
point_count = 0

def onclick(event):
    global start_point, end_point, point_count, grid_size
    if point_count < 2:
        point_x = int(event.xdata // grid_size)
        point_y = int(event.ydata // grid_size)
        if point_count == 0:
            start_point = (point_y, point_x)
            plt.scatter(event.xdata, event.ydata, c='green', s=100, label='Start Point')
        elif point_count == 1:
            end_point = (point_y, point_x)
            plt.scatter(event.xdata, event.ydata, c='red', s=100, label='End Point')
        point_count += 1
    plt.draw()

image_path = r"C:\Users\athar\Desktop\car2.jpg"
image = cv2.imread(image_path)
grid_size = 10
grid = create_grid(image, grid_size)

fig, ax = plt.subplots()
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

if start_point and end_point:
    path = astar(start_point, end_point, grid)
    if path:
        for pos in path:
            y, x = pos
            px = (x * grid_size) + (grid_size // 2)
            py = (y * grid_size) + (grid_size // 2)
            image[py-grid_size//4:py+grid_size//4, px-grid_size//4:px+grid_size//4] = (0, 255, 0)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Shortest Path with A*")
        plt.show()
    else:
        print("No path found.")
else:
    print("Select start and end points before running the pathfinding algorithm.")
