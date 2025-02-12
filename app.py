from flask import Flask, render_template, jsonify, request
import random
import copy
import os

app = Flask(__name__)

# Fixed grid dimensions
GRID_WIDTH = 30
GRID_HEIGHT = 30

# Initialize empty grid and history
def create_empty_grid(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

grid = create_empty_grid(GRID_WIDTH, GRID_HEIGHT)
history = []
MAX_HISTORY = 100  # Maximum number of states to keep in history

def count_live_neighbors(r, c):
    """Count the number of live neighbors around cell (r, c)."""
    live_count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            # Use modulo to wrap around grid edges
            rr = (r + dr) % GRID_HEIGHT
            cc = (c + dc) % GRID_WIDTH
            live_count += grid[rr][cc]
    return live_count

def update_grid():
    """Compute one iteration of Conway's Game of Life."""
    new_grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            live_neighbors = count_live_neighbors(r, c)
            cell_state = grid[r][c]
            
            # Apply Conway's rules
            if cell_state == 1:
                # Cell is alive
                if live_neighbors == 2 or live_neighbors == 3:
                    new_grid[r][c] = 1  # stays alive
                else:
                    new_grid[r][c] = 0  # dies
            else:
                # Cell is dead
                if live_neighbors == 3:
                    new_grid[r][c] = 1  # becomes alive
                else:
                    new_grid[r][c] = 0  # stays dead
    return new_grid

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def get_state():
    """Return the current grid state as JSON."""
    return jsonify(grid)

@app.route('/step', methods=['POST'])
def step():
    """
    Advance the simulation by one step and return the new state.
    Called by the frontend when the simulation is running or stepping forward.
    """
    global grid, history
    # Save current state to history before updating
    if len(history) >= MAX_HISTORY:
        history.pop(0)  # Remove oldest state if we've reached max history
    history.append(copy.deepcopy(grid))
    grid = update_grid()
    return jsonify(grid)

@app.route('/step_back', methods=['POST'])
def step_back():
    """
    Go back one step in the simulation history.
    Returns the previous state or current state if no history exists.
    """
    global grid, history
    if history:
        grid = history.pop()
    return jsonify(grid)

@app.route('/toggle_cell', methods=['POST'])
def toggle_cell():
    """
    Toggle the state of a single cell (row, col).
    Expects JSON body: {"row": <int>, "col": <int>}
    Returns updated grid for re-rendering.
    """
    global grid, history
    data = request.get_json()
    r = data['row']
    c = data['col']
    
    # Save current state to history before modifying
    if len(history) >= MAX_HISTORY:
        history.pop(0)
    history.append(copy.deepcopy(grid))
    
    # Toggle cell: 1 -> 0, 0 -> 1
    grid[r][c] = 1 - grid[r][c]
    
    return jsonify(grid)

@app.route('/random', methods=['POST'])
def random_board():
    """
    Generate a new random board configuration.
    Returns the new grid state as JSON.
    """
    global grid, history
    # Save current state to history before generating new random board
    if len(history) >= MAX_HISTORY:
        history.pop(0)
    history.append(copy.deepcopy(grid))
    
    grid = [[1 if random.random() < 0.25 else 0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    return jsonify(grid)

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask server
    app.run(host='0.0.0.0', port=port)
