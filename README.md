# Slime Mold: Single Pastel Green Trails

## Overview
This project simulates a simple slime mold-inspired system where agents move around a 2D environment, leaving behind pastel green trails. The trails gradually fade over time, creating a visually engaging dynamic pattern. The simulation is implemented using Python with NumPy and Pygame.

## Features
- Agents move and react to their surroundings based on sensed brightness.
- Smooth and organic trail patterns are drawn using a pastel green color.
- Agents wrap around screen edges for continuous motion.
- Trail fading effect creates evolving textures over time.
- Adjustable parameters for agent behavior and visual output.

## Requirements
- Python 3.x
- NumPy
- Pygame

Install dependencies using:
```sh
pip install numpy pygame
```

## Usage
Run the simulation by executing:
```sh
python ABM_OSC_OUT.py
```

## Configuration
The following parameters can be adjusted in the code:

| Parameter           | Description                                   | Default Value |
|---------------------|-----------------------------------------------|--------------|
| `WIDTH`, `HEIGHT`  | Screen dimensions (pixels)                    | 400, 400     |
| `AGENTS_NUM`       | Number of agents in the simulation            | 750          |
| `SUBSTEPS`         | Agent update steps per frame (smoothness)     | 4            |
| `SENSOR_OFFSET`    | Distance for agent sensor offset              | 10           |
| `SENSOR_ANGLE`     | Angle of agent's sensors                      | π/12         |
| `TURN_ANGLE`       | Maximum turn angle for agents                 | π/9          |
| `RANDOM_TURN`      | Random turn factor                            | π/30         |
| `FADE_SPEED`       | Rate at which trails fade toward white        | 0.04         |
| `AGENT_TRAIL_RADIUS` | Radius of each agent's trail                | 3            |
| `GREEN`            | Color of trails in (R, G, B) format (0-1)     | (0.40, 0.65, 0.40) |

## Controls
- Press **ESC** or close the window to exit the simulation.

## Implementation Details
- Agents move in a continuous loop, sensing their surroundings and updating their direction based on brightness.
- A global `trail_map` stores the RGB values of trails in a floating-point array for smooth color blending.
- Each frame, the agents update their position, leaving trails, and the map fades toward white.
- The display updates at 60 FPS with Pygame.

## Future Enhancements
- Add color variation for different agent behaviors.
- Implement multiple agent species with distinct trail patterns.
- Optimize performance for larger-scale simulations.
- Integrate dynamic ecological system based interactions. 

## License
This project is released under the MIT License.

