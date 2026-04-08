# DOOM GTK Port

A parody implementation of Doom written in Python using GTK3, where all UI elements are rendered with random Doom palette colors.

## Features

- **Classic Doom Colors**: All widgets use the authentic 16-color Doom palette
- **Random GTK Elements**: Each widget gets randomly assigned Doom colors
- **Animated Portal**: Center viewport features an animated teleporter effect
- **Doom Face Status**: Iconic face that changes expressions based on game events
- **Health & Ammo Bars**: Classic status bars that change color based on levels
- **Interactive Controls**: FIRE, USE, and RANDOM buttons with visual feedback
- **Decorative Crates**: Classic Doom crate textures as UI decorations

## Requirements

- Python 3
- GTK 3
- PyGObject (gi)

### Installation on Debian/Ubuntu

```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

## Running

```bash
python3 doom_gtk_port.py
```

**Note**: Requires a display server (X11 or Wayland). Will not work in headless environments without Xvfb or similar.

## Controls

- **FIRE**: Shoot weapon (reduces ammo, makes face grin)
- **USE**: Use health item (increases health)
- **RANDOM**: Randomize all widget colors and face expression

## Architecture

### Widget Classes

- `DoomWidget`: Base class for all Doom-styled widgets
- `DoomButton`: Interactive button with press effects
- `DoomBar`: Status bar for health/ammo with color-coded levels
- `DoomFace`: Animated face status indicator with multiple expressions
- `DoomCrate`: Decorative crate element with X pattern
- `DoomPortal`: Animated portal with pulsing rings

### Doom Color Palette

The classic Doom palette includes:
- Black, Brown, Dark Grey, Grey, Light Grey
- Red, Green, Blue, Yellow, Orange
- Purple, Pink, Flesh tones
- Dark Green, Bright Green, Cyan

Each widget randomly selects colors from this palette for its background, foreground, accent, and highlight colors.

## How It Works

1. Each widget inherits from `DoomWidget` which provides Doom color generation
2. The `generate_doom_colors()` method randomly assigns colors from the Doom palette
3. Custom drawing is done via Cairo graphics in the `do_draw()` method
4. Animations use GLib timers for smooth updates
5. Game logic simulates damage, shooting, and item usage

## Screenshot Description

When running, you'll see:
- Top: Title "DOOM" in red, health bar, ammo bar, and status face
- Middle: Left and right panels with random widgets, center animated portal
- Bottom: FIRE, USE, RANDOM buttons and decorative crates

All elements constantly change colors in true Doom fashion!

