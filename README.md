# Conway's Game of Life

![Demo](sample.webm)

An interactive implementation of Conway's Game of Life with a modern, responsive interface. Built with Flask and vanilla JavaScript.

## Features

- Interactive 30x30 grid with clickable cells
- Play, pause, and step through generations
- Generate random board configurations
- Adjustable simulation speed

## Technical Details

### Backend (Flask)
- Implements core Game of Life logic
- Maintains game state and history
- RESTful endpoints for all game operations
- Wrapping grid edges (toroidal array)

### Frontend
- Pure JavaScript with no external dependencies
- CSS Grid for game board layout
- Modern design system with CSS variables
- Smooth transitions and hover effects
- Responsive layout that adapts to screen size

## Running Locally

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install flask
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser

## Game Rules

Conway's Game of Life follows four simple rules:

1. Any live cell with fewer than two live neighbors dies (underpopulation)
2. Any live cell with two or three live neighbors lives on to the next generation
3. Any live cell with more than three live neighbors dies (overpopulation)
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction)

## Implementation Notes

- The grid wraps around at the edges, creating a toroidal array
- History tracking allows stepping backward through up to 100 previous states
- Cell states are toggled through an intuitive click interface
- Simulation speed can be adjusted from 0.1 to 100 steps per second