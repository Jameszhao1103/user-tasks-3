# Matplotlib Smooth Transitions

This project implements smooth animations and transitions between different states of matplotlib plots.

## Features

- **Smooth data transitions**: Animate changes in plot data values
- **Property transitions**: Animate colors, sizes, line widths, and positions
- **Multiple plot types**: Support for line plots, scatter plots, and bar charts
- **Easing functions**: Various easing options for natural-looking animations
- **Figure state transitions**: Transition between completely different plot states

## Installation

Ensure you have the required dependencies:

```bash
pip install matplotlib numpy
```

## Usage

### Basic Line Plot Transition

```python
from smooth_transitions import smooth_transition
import numpy as np

# Define initial and final data states
x = np.linspace(0, 10, 50)
from_data = {
    'x': x,
    'y': np.sin(x),
    'color': 'blue',
    'linewidth': 2
}

to_data = {
    'x': x,
    'y': np.cos(x),
    'color': 'red',
    'linewidth': 4
}

# Create smooth transition
anim = smooth_transition(from_data, to_data, 
                        duration=2.0, fps=30, 
                        easing='ease_in_out_quad',
                        plot_type='line')
plt.show()
```

### Scatter Plot Transition

```python
# Scatter plot with changing positions and sizes
from_data = {
    'x': [1, 2, 3, 4],
    'y': [1, 2, 3, 4],
    'colors': 'blue',
    'sizes': [50, 50, 50, 50]
}

to_data = {
    'x': [4, 3, 2, 1],
    'y': [1, 2, 3, 4],
    'colors': 'red',
    'sizes': [100, 150, 200, 250]
}

anim = smooth_transition(from_data, to_data, 
                        duration=3.0, fps=30,
                        plot_type='scatter')
plt.show()
```

### Figure State Transition

```python
from smooth_transitions import transition_plot_state

# Create two different figures
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(x_data1, y_data1)
ax1.set_title("Plot 1")

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(x_data2, y_data2)
ax2.set_title("Plot 2")

# Transition between them
anim = transition_plot_state(fig1, fig2, duration=2.0)
plt.show()
```

## Available Easing Functions

- `linear`: Constant speed
- `ease_in_quad`: Slow start, accelerating
- `ease_out_quad`: Fast start, decelerating  
- `ease_in_out_quad`: Slow start and end
- `ease_in_cubic`: More pronounced slow start
- `ease_out_cubic`: More pronounced slow end

## Parameters

### smooth_transition()

- `from_data` (dict): Initial data state
- `to_data` (dict): Final data state  
- `duration` (float): Animation duration in seconds
- `fps` (int): Frames per second
- `easing` (str): Easing function name
- `plot_type` (str): 'line', 'scatter', or 'bar'
- `**kwargs`: Additional matplotlib arguments

### Data Dictionary Format

For **line plots**:
```python
{
    'x': array_like,           # X coordinates
    'y': array_like,           # Y coordinates  
    'color': str or tuple,     # Line color
    'linewidth': float         # Line width
}
```

For **scatter plots**:
```python
{
    'x': array_like,           # X coordinates
    'y': array_like,           # Y coordinates
    'colors': str or array,    # Point colors
    'sizes': array_like        # Point sizes
}
```

For **bar charts**:
```python
{
    'x': array_like,           # Bar positions
    'y': array_like,           # Bar heights
    'colors': str or array,    # Bar colors
    'width': float             # Bar width
}
```

## Running the Demo

Execute the demo script to see various transition examples:

```bash
python demo.py
```

## Running Tests

```bash
python test_transitions.py
```

## Examples Gallery

The demo script includes examples of:

1. **Line Plot Transitions**: Smooth morphing between different mathematical functions
2. **Scatter Plot Transitions**: Points moving and changing size/color
3. **Bar Chart Transitions**: Bars growing/shrinking with color changes
4. **Easing Function Comparison**: Side-by-side comparison of different easing types
5. **Figure State Transitions**: Complete plot transformations
6. **Multi-Property Transitions**: Complex animations with multiple changing properties

## Contributing

This implementation provides a foundation for smooth matplotlib transitions. Potential enhancements:

- Support for more plot types (histograms, contour plots, etc.)
- Advanced figure state interpolation
- Keyframe-based animations
- Export to video formats
- Interactive transition controls