
# Anvil Dodge - SE Lab 4

## Overview

Anvil Dodge is a 2D survival game developed using Python and Pygame.

The player moves horizontally to avoid falling anvils. The objective is to survive for as long as possible without colliding with an anvil.

This project demonstrates object-oriented programming, game loops, collision detection, boundary management, time tracking, difficulty scaling, and visual effects.

## Features

- Player movement using the A/D keys or arrow keys.
- Boundary restrictions that prevent the player from leaving the screen.
- Random anvil spawning and randomized falling speeds.
- Rectangular collision detection.
- Game-over screen when the player is hit.
- Survival-time tracking.
- Increasing difficulty as survival time increases.
- Speed-based anvil warning colors:
  - Grey for normal anvils.
  - Orange for fast anvils.
  - Red for very fast anvils.
- Dust particle effects when anvils hit the ground.
- Restart functionality using the R key.

## Technologies Used

- Python 3.10 or later
- Pygame

## Project Structure

```text
63_anvil_dodge/
├── game/
│   ├── player.py
│   ├── anvil.py
│   └── game_engine.py
├── main.py
└── README.md
```

## Installation

1. Install Python 3.10 or later.
2. Open a terminal in the project directory.
3. Install Pygame:

```bash
python -m pip install pygame
```

## Running the Game

Execute:

```bash
python main.py
```

## Controls

| Key | Action |
|---|---|
| Left Arrow or A | Move left |
| Right Arrow or D | Move right |
| R | Restart after game over |
| Window close button | Exit the game |

## Bug Fixes and Improvements

### 1. Player Boundary Bug

The original player could move beyond the visible screen boundaries.

The player's position is now clamped between zero and the maximum valid horizontal coordinate.

### 2. Dynamic Difficulty Scaling

The anvil spawn interval decreases as the player's survival time increases.

The interval starts at 700 milliseconds and cannot fall below 200 milliseconds.

### 3. Speed-Based Warning Colors

Anvils have different colors depending on their falling speed.

This helps the player identify faster hazards visually.

### 4. Ground Impact Effects

Dust particles appear when an anvil reaches the ground.

Particles move, respond to a simple gravity effect, and disappear after a short lifetime.

## Testing Checklist

- [ ] The player cannot move beyond the left edge.
- [ ] The player cannot move beyond the right edge.
- [ ] Anvils spawn at randomized horizontal positions.
- [ ] Anvils fall at randomized speeds.
- [ ] Faster anvils display warning colors.
- [ ] Anvils spawn more frequently as survival time increases.
- [ ] Ground impacts generate dust particles.
- [ ] A player collision triggers game over.
- [ ] The survival timer stops after game over.
- [ ] Pressing R resets the player, timer, anvils, and particles.

## Submission Requirements

- Record approximately 10 seconds of gameplay before the fixes, showing the original boundary bug.
- Record approximately 10 seconds of gameplay after the fixes, showing the corrected boundaries and implemented features.
- Include the link to the ChatGPT conversation used during debugging.

## Conclusion

Anvil Dodge demonstrates how debugging, testing, and incremental improvements can make a game more reliable and engaging. The updated implementation fixes the player boundary issue and adds progressive difficulty, visual hazard warnings, and ground-impact effects.
