import tkinter as tk
from tkinter import messagebox
from collections import deque

# Constants for grid size and styling
ROWS, COLS = 8, 8
CELL_SIZE = 50

# Initialize variables
start = None
destination = None
blocks = set()
current_mode = None

# Create the grid
def create_grid():
    for i in range(ROWS):
        for j in range(COLS):
            cell = tk.Frame(
                grid_frame,
                width=CELL_SIZE,
                height=CELL_SIZE,
                bg="white",
                borderwidth=1,
                relief="solid",
            )
            cell.grid(row=i, column=j)
            cell.bind("<Button-1>", lambda e, r=i, c=j: handle_click(r, c))
            grid_cells[(i, j)] = cell

# Handle cell clicks based on the current mode
def handle_click(row, col):
    global start, destination
    cell = grid_cells[(row, col)]

    if current_mode == "select":
        if (row, col) != start and (row, col) != destination:
            cell.config(bg="gray")
            blocks.add((row, col))
    elif current_mode == "delete":
        cell.config(bg="white")
        blocks.discard((row, col))
        if (row, col) == start:
            start = None
        elif (row, col) == destination:
            destination = None
    elif current_mode == "start":
        if start:
            grid_cells[start].config(bg="white")
        cell.config(bg="green")
        start = (row, col)
    elif current_mode == "final":
        if destination:
            grid_cells[destination].config(bg="white")
        cell.config(bg="red")
        destination = (row, col)

# Reset the entire grid
def reset_grid():
    global start, destination, blocks
    start, destination = None, None
    blocks.clear()
    for cell in grid_cells.values():
        cell.config(bg="white")
    status_label.config(text="Grid reset. Select Start and Destination points.")

# Find the shortest path using BFS with step-by-step visualization
def find_shortest_path():
    if not start or not destination:
        status_label.config(text="Please set both Start and Final points!")
        return

    # BFS algorithm
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (row, col), path = queue.popleft()

        # Destination reached
        if (row, col) == destination:
            status_label.config(text="Path found! Animating...")
            animate_path(path)
            return

        # Mark as visited
        visited.add((row, col))

        # Explore neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < ROWS
                and 0 <= nc < COLS
                and (nr, nc) not in visited
                and (nr, nc) not in blocks
            ):
                queue.append(((nr, nc), path + [(nr, nc)]))

    status_label.config(text="No path found!")

# Animate the shortest path step by step
def animate_path(path, index=0):
    if index < len(path):
        r, c = path[index]
        if (r, c) != start and (r, c) != destination:  # Don't color start or destination
            grid_cells[(r, c)].config(bg="yellow")
        root.after(500, animate_path, path, index + 1)  # 500ms delay between steps
    else:
        status_label.config(text="Path animation complete!")

# Set the current mode
def set_mode(mode):
    global current_mode
    current_mode = mode
    status_label.config(text=f"Mode: {mode.capitalize()}")

# Initialize the main window
root = tk.Tk()
root.title("Micromouse Maze Game")
root.geometry(f"{COLS * CELL_SIZE + 20}x{ROWS * CELL_SIZE + 150}")

# Header label
header_label = tk.Label(root, text="Micromouse Maze Game", font=("Arial", 20), fg="blue")
header_label.pack(pady=10)

# Grid frame
grid_frame = tk.Frame(root)
grid_frame.pack()

# Controls frame
controls_frame = tk.Frame(root)
controls_frame.pack(pady=10)

# Control buttons with updated colors
tk.Button(
    controls_frame, text="Select", command=lambda: set_mode("select"), bg="#A9A9A9", fg="black", width=10
).grid(row=0, column=0, padx=5)
tk.Button(
    controls_frame, text="Delete", command=lambda: set_mode("delete"), bg="#FFB6C1", fg="black", width=10
).grid(row=0, column=1, padx=5)
tk.Button(
    controls_frame, text="Start", command=lambda: set_mode("start"), bg="#90EE90", fg="black", width=10
).grid(row=0, column=2, padx=5)
tk.Button(
    controls_frame, text="Final", command=lambda: set_mode("final"), bg="#FF6347", fg="black", width=10
).grid(row=0, column=3, padx=5)
tk.Button(
    controls_frame, text="Reset", command=reset_grid, bg="#FFD700", fg="black", width=10
).grid(row=0, column=4, padx=5)
tk.Button(
    controls_frame, text="Find Path", command=find_shortest_path, bg="#1E90FF", fg="white", width=10
).grid(row=0, column=5, padx=5)

# Status label
status_label = tk.Label(root, text="Select Start and Destination points.", font=("Arial", 12), fg="black")
status_label.pack(pady=10)

# Dictionary to hold grid cell references
grid_cells = {}

# Create the grid
create_grid()

# Run the application
root.mainloop()
