import numpy as np
import pygame
import sys
import random
import math

#
# -----------------------------------------------------------------------------
# 1) CONFIGURATION
# -----------------------------------------------------------------------------
#
WIDTH, HEIGHT = 400, 400

# Number of agents
AGENTS_NUM = 750

# Update steps per frame => smoother lines but higher CPU usage
SUBSTEPS = 4

# Agent motion parameters
SENSOR_OFFSET = 10
SENSOR_ANGLE  = math.pi / 12
TURN_ANGLE    = math.pi / 9
RANDOM_TURN   = math.pi / 30

# Each pixel color in [0..1] will fade some fraction of the distance toward (1,1,1)
FADE_SPEED = 0.04

# Radius of each agent's trail
AGENT_TRAIL_RADIUS = 3

# A single pastel green color in [0..1]
GREEN = (0.40, 0.65, 0.40)

# 3D float array (height, width, 3 channels), all start at white
trail_map = np.ones((HEIGHT, WIDTH, 3), dtype=np.float32)


#
# -----------------------------------------------------------------------------
# 2) AGENT CLASS
# -----------------------------------------------------------------------------
#
class Agent:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.dir = random.uniform(0, 2 * math.pi)
        # Removed the age system entirely

    def update_direction(self):
        # Sense brightness in three directions
        right  = self.sense(SENSOR_ANGLE)
        center = self.sense(0)
        left   = self.sense(-SENSOR_ANGLE)

        # Slightly discourage going straight => (center - 1)
        three_ways = [left, center - 1, right]
        idx = min_index(three_ways)

        # idx=0 => turn left, idx=1 => straight, idx=2 => turn right
        self.dir += TURN_ANGLE * (idx - 1)

        # Add random wiggle
        self.dir += random.uniform(-RANDOM_TURN, RANDOM_TURN)

    def sense(self, offset):
        """
        Return brightness in [0..255] at sensor offset from agent's direction.
        """
        global trail_map
        angle = self.dir + offset
        x_sens = int(self.x + SENSOR_OFFSET * math.cos(angle))
        y_sens = int(self.y + SENSOR_OFFSET * math.sin(angle))

        # Wrap
        x_sens %= WIDTH
        y_sens %= HEIGHT

        # Convert color (R,G,B) in [0..1] => brightness in [0..255]
        px_color = trail_map[y_sens, x_sens]
        brightness_01 = (px_color[0] + px_color[1] + px_color[2]) / 3.0
        return brightness_01 * 255.0

    def update_position(self):
        """
        Move forward and draw the same green color every time (no aging).
        """
        self.x += math.cos(self.dir)
        self.y += math.sin(self.dir)

        # Wrap edges
        self.x %= WIDTH
        self.y %= HEIGHT

        self.draw_trail(int(self.x), int(self.y), AGENT_TRAIL_RADIUS)

    def draw_trail(self, cx, cy, radius):
        """
        Draw a small circle of one pastel-green color.
        """
        global trail_map
        r, g, b = GREEN  # fixed color
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    x_t = (cx + dx) % WIDTH
                    y_t = (cy + dy) % HEIGHT
                    trail_map[y_t, x_t, 0] = r
                    trail_map[y_t, x_t, 1] = g
                    trail_map[y_t, x_t, 2] = b


#
# -----------------------------------------------------------------------------
# 3) HELPER FUNCTIONS
# -----------------------------------------------------------------------------
#
def min_index(values):
    """Return the index of the smallest value in a list."""
    min_val = values[0]
    min_idx = 0
    for i, val in enumerate(values):
        if val < min_val:
            min_val = val
            min_idx = i
    return min_idx


#
# -----------------------------------------------------------------------------
# 4) MAIN LOOP
# -----------------------------------------------------------------------------
#
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slime Mold: Single Pastel Green Trails")

    clock = pygame.time.Clock()
    agents = [Agent() for _ in range(AGENTS_NUM)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fade each pixel some fraction FADE_SPEED toward white (1,1,1)
        global trail_map
        trail_map += (1.0 - trail_map) * FADE_SPEED

        # Update agents multiple times per frame => smoother lines
        for _ in range(SUBSTEPS):
            for ag in agents:
                ag.update_direction()
            for ag in agents:
                ag.update_position()

        # Convert [0..1] => [0..255], shape => (H, W, 3)
        arr8 = (trail_map * 255).astype(np.uint8)

        # Blit to Pygame
        pygame.surfarray.blit_array(screen, arr8)
        pygame.display.flip()

        # e.g., 30 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
