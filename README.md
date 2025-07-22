# Paint Pygame

## Overview
Paint Pygame is a collaborative drawing application built using Python and Pygame. It allows multiple users to connect over a local network and draw together on a shared canvas. The application features various drawing tools, color selection, and brush size adjustment.

## Features
- **Collaborative Drawing**: Multiple users can draw on the same canvas simultaneously.
- **Drawing Tools**: Includes brush, line, circle, and square tools.
- **Color Selection**: Choose from a palette of predefined colors.
- **Brush Size Adjustment**: Select different brush sizes for finer or broader strokes.
- **Network Communication**: Uses sockets for real-time communication between clients and the server.

## Installation
### Prerequisites
- Python 3.8 or higher
- Pygame library

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ConnorKnoetze/paint-pygame.git
   ```
2. Navigate to the project directory:
   ```bash
   cd paint-pygame
   ```
3. Run the `client_launcher.py` script to install dependencies and start the server and clients:
   ```bash
   python client_launcher.py
   ```

## Usage
- The server will start automatically.
- Multiple client windows will open for collaborative drawing.
- Use the toolbar to select tools, colors, and brush sizes.
- Draw on the canvas and see updates in real-time across all connected clients.

## LAN Connectivity
To allow devices on the same LAN to connect to the server, update the `server` variable in the `main.py` file with your device's IP address. This ensures that other devices on the network can join the collaborative drawing session.

Example:
```python
server = "127.0.0.1"  # Replace with your device's IP address
```

## File Structure
- `main.py`: Contains the main application logic for the drawing client.
- `server.py`: Handles client connections and broadcasts drawing updates.
- `client_launcher.py`: Automates the setup and launch of the server and clients.
- `assets/`: Contains graphical assets for tools, colors, and brush sizes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author
Connor Knoetze

## Acknowledgments
- Built using [Pygame](https://www.pygame.org/).
- Inspired by collaborative drawing tools.
