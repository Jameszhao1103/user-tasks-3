# Matplotlib Smooth Transitions

This module provides smooth animated transitions between different states of matplotlib plots. It enables creating fluid animations that transition between data states, plot properties, and even complete figure configurations.

## Features

- **Smooth data transitions** for line plots, scatter plots, and bar charts
- **Multiple easing functions** for natural-looking animations
- **Property transitions** including colors, sizes, and positions
- **Complete figure state transitions** between different plot configurations
- **Convenience functions** for common transition types
- **Customizable duration and frame rate**

## Core Functions

### `smooth_transition(from_data, to_data, duration=1.0, fps=30, **kwargs)`

Creates a smooth animated transition between two data states.

**Parameters:**
- `from_data`: Initial data state (dict, array-like, or list)
- `to_data`: Final data state (same format as from_data)
- `duration`: Duration of transition in seconds (default: 1.0)
- `fps`: Frames per second for animation (default: 30)
- `easing`: Easing function name or custom function (default: 'ease_in_out_quad')
- `ax`: Matplotlib axes to animate (default: current axes)
- `plot_type`: Type of plot - 'line', 'scatter', or 'bar' (default: 'line')
- `**kwargs`: Additional arguments passed to the plot function

**Returns:**
- `matplotlib.animation.FuncAnimation`: Animation object

### `transition_plot_state(fig_from, fig_to, duration=1.0, fps=30, easing='ease_in_out_quad')`

Creates a smooth transition between two complete figure states.

**Parameters:**
- `fig_from`: Initial figure state
- `fig_to`: Final figure state
- `duration`: Duration of transition in seconds (default: 1.0)
- `fps`: Frames per second for animation (default: 30)
- `easing`: Easing function name or custom function (default: 'ease_in_out_quad')

**Returns:**
- `matplotlib.animation.FuncAnimation`: Animation object

## Convenience Functions

### `transition_line_data(ax, from_y, to_y, duration=1.0, fps=30, **kwargs)`

Convenience function for transitioning line plot y-data.

### `transition_scatter_data(ax, from_xy, to_xy, duration=1.0, fps=30, **kwargs)`

Convenience function for transitioning scatter plot data.

### `transition_bar_heights(ax, from_heights, to_heights, duration=1.0, fps=30, **kwargs)`

Convenience function for transitioning bar chart heights.

## Easing Functions

The module includes various easing functions for natural-looking animations:

- `linear`: No acceleration
- `ease_in_quad`: Quadratic ease-in (accelerating from zero)
- `ease_out_quad`: Quadratic ease-out (decelerating to zero)
- `ease_in_out_quad`: Quadratic ease-in-out
- `ease_in_cubic`: Cubic ease-in
- `ease_out_cubic`: Cubic ease-out
- `ease_in_out_cubic`: Cubic ease-in-out
- `ease_in_sine`: Sinusoidal ease-in
- `ease_out_sine`: Sinusoidal ease-out
- `ease_in_out_sine`: Sinusoidal ease-in-out

## Data Formats

### Line Plots
```python
# Simple y-values
data = [1, 2, 3, 4, 5]

# Or dictionary format
data = {'x': [0, 1, 2, 3, 4], 'y': [1, 2, 3, 4, 5]}
```

### Scatter Plots
```python
# Tuple format
data = ([1, 2, 3], [4, 5, 6])  # (x_values, y_values)

# Or dictionary format
data = {
    'x': [1, 2, 3],
    'y': [4, 5, 6],
    'sizes': [50, 100, 75],      # Optional
    'colors': ['red', 'blue', 'green']  # Optional
}
```

### Bar Charts
```python
# Simple heights
data = [3, 7, 2, 5]

# Or dictionary format
data = {
    'heights': [3, 7, 2, 5],
    'colors': ['red', 'green', 'blue', 'orange']  # Optional
}
```

## Usage Examples

### Basic Line Transition

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

# Create data
x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x) * 2

# Create figure
fig, ax = plt.subplots()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-2.5, 2.5)

# Create transition
anim = mt.smooth_transition(
    from_data={'x': x, 'y': y1},
    to_data={'x': x, 'y': y2},
    duration=2.0,
    fps=30,
    easing='ease_in_out_cubic',
    ax=ax,
    plot_type='line',
    color='blue',
    linewidth=2
)

# Save or show animation
anim.save('line_transition.gif', writer='pillow')
# or plt.show()
```

### Scatter Plot Transition

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

# Create data - circle to star
n_points = 20
theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)

# Circle
x1 = np.cos(theta)
y1 = np.sin(theta)

# Star
star_r = np.where(np.arange(n_points) % 2 == 0, 1.5, 0.7)
x2 = star_r * np.cos(theta)
y2 = star_r * np.sin(theta)

# Create figure
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# Create transition
anim = mt.smooth_transition(
    from_data={'x': x1, 'y': y1},
    to_data={'x': x2, 'y': y2},
    duration=2.5,
    fps=30,
    easing='ease_in_out_sine',
    ax=ax,
    plot_type='scatter',
    color='red',
    s=100
)

anim.save('scatter_transition.gif', writer='pillow')
```

### Bar Chart Transition

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

# Create data
categories = ['A', 'B', 'C', 'D', 'E']
heights1 = np.array([2, 5, 3, 8, 1])
heights2 = np.array([7, 2, 6, 1, 4])

# Create figure
fig, ax = plt.subplots()
ax.set_ylim(0, 9)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)

# Create transition
anim = mt.smooth_transition(
    from_data={'heights': heights1},
    to_data={'heights': heights2},
    duration=2.0,
    fps=30,
    easing='ease_in_out_quad',
    ax=ax,
    plot_type='bar',
    color='green'
)

anim.save('bar_transition.gif', writer='pillow')
```

### Using Convenience Functions

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

fig, ax = plt.subplots()

# Line data transition
x = np.linspace(0, 2*np.pi, 50)
y1 = np.sin(x)
y2 = np.cos(x) * 1.5

anim = mt.transition_line_data(
    ax=ax,
    from_y=y1,
    to_y=y2,
    duration=2.0,
    color='blue'
)

anim.save('line_convenience.gif', writer='pillow')
```

### Figure State Transition

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

# Create first figure
fig1, ax1 = plt.subplots()
x = np.linspace(0, 10, 50)
ax1.plot(x, np.sin(x), 'b-')
ax1.set_title('Sine Wave')

# Create second figure
fig2, ax2 = plt.subplots()
ax2.scatter(np.random.randn(100), np.random.randn(100), c='red')
ax2.set_title('Random Scatter')

# Create transition
anim = mt.transition_plot_state(
    fig_from=fig1,
    fig_to=fig2,
    duration=3.0,
    fps=30
)

anim.save('figure_transition.gif', writer='pillow')
```

### Custom Easing Function

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transitions as mt

def custom_bounce(t):
    """Custom bounce easing function."""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - 2 * (1 - t) * (1 - t)

# Use custom easing
anim = mt.smooth_transition(
    from_data={'y': [1, 2, 3, 4, 5]},
    to_data={'y': [5, 4, 3, 2, 1]},
    duration=2.0,
    easing=custom_bounce,  # Custom function
    ax=ax,
    plot_type='line'
)
```

## Advanced Features

### Color Transitions

The module automatically handles color transitions when colors are specified in the data:

```python
# Colors will smoothly transition
from_data = {
    'x': [1, 2, 3],
    'y': [1, 2, 3],
    'colors': ['red', 'green', 'blue']
}

to_data = {
    'x': [1, 2, 3],
    'y': [3, 2, 1],
    'colors': ['blue', 'red', 'green']
}

anim = mt.smooth_transition(from_data, to_data, plot_type='scatter')
```

### Size Transitions

For scatter plots, point sizes can also be animated:

```python
from_data = {
    'x': [1, 2, 3],
    'y': [1, 2, 3],
    'sizes': [50, 100, 150]
}

to_data = {
    'x': [1, 2, 3],
    'y': [3, 2, 1],
    'sizes': [150, 50, 100]
}

anim = mt.smooth_transition(from_data, to_data, plot_type='scatter')
```

## Performance Tips

1. **Lower FPS for faster rendering**: Use `fps=15` or `fps=20` for quicker animations
2. **Shorter durations**: Use `duration=1.0` or less for snappy transitions
3. **Fewer data points**: Reduce the number of points for complex animations
4. **Simple easing**: Use `'linear'` easing for fastest performance

## Saving Animations

The module works with all matplotlib animation writers:

```python
# GIF format (requires Pillow)
anim.save('animation.gif', writer='pillow', fps=30)

# MP4 format (requires ffmpeg)
anim.save('animation.mp4', writer='ffmpeg', fps=30)

# HTML with JavaScript controls
anim.save('animation.html', writer='html')
```

## Integration with Matplotlib

The transitions module is designed to work seamlessly with existing matplotlib code. Simply import the module and use the transition functions with your existing plots and data.

## Requirements

- matplotlib >= 3.0
- numpy
- Pillow (for GIF output)
- ffmpeg (for MP4 output, optional)

## Examples Gallery

The repository includes several example scripts:

- `simple_transitions_example.py`: Basic usage examples
- `transitions_demo.py`: Comprehensive demonstration of all features
- `test_transitions.py`: Test suite for functionality verification

Run these scripts to see the transitions in action and learn how to use the various features.