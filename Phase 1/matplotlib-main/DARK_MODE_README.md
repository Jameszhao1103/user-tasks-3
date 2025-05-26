# Matplotlib Dark Mode Toggle

This implementation adds a comprehensive dark mode toggle functionality to matplotlib, allowing users to easily switch any existing plot between light and dark modes with a single function call.

## Features

- **Reversible Toggle**: Call the function once to switch to dark mode, call it again to switch back to light mode
- **Flexible Application**: Can be applied to individual axes, entire figures, or the current figure
- **Automatic Color Detection**: Automatically detects current mode and toggles appropriately
- **Original Color Preservation**: Stores original colors to enable perfect restoration when toggling back
- **Data Color Adjustment**: Optional feature to adjust data element colors for better visibility in dark mode
- **Custom Color Schemes**: Ability to customize the dark mode color palette
- **Comprehensive Element Support**: Handles backgrounds, text, grids, spines, tick marks, and labels

## Installation

The dark mode functionality is implemented as a new module `dark_mode.py` in the matplotlib library:

```
lib/matplotlib/dark_mode.py
```

## Usage

### Basic Usage

```python
import matplotlib.pyplot as plt
import matplotlib.dark_mode as dm
import numpy as np

# Create a plot
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_title('My Plot')
ax.grid(True)

# Toggle to dark mode
dm.toggle_dark_mode(fig=fig)

# Toggle back to light mode
dm.toggle_dark_mode(fig=fig)
```

### Function Signature

```python
toggle_dark_mode(ax=None, fig=None, adjust_data_colors=False)
```

**Parameters:**
- `ax` (matplotlib.axes.Axes, optional): Specific axes to apply dark mode to
- `fig` (matplotlib.figure.Figure, optional): Specific figure to apply dark mode to
- `adjust_data_colors` (bool, default False): Whether to automatically adjust data element colors for better visibility

**Behavior:**
- If `ax` is provided: Only that specific axis is modified
- If `fig` is provided: All axes in the figure are modified
- If neither is provided: The current figure (`plt.gcf()`) is modified

### Examples

#### 1. Toggle Entire Figure

```python
import matplotlib.pyplot as plt
import matplotlib.dark_mode as dm
import numpy as np

# Create a multi-subplot figure
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Add various plot types
x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x), 'b-', label='sin(x)')
ax1.legend()
ax1.grid(True)

ax2.scatter(np.random.randn(100), np.random.randn(100))
ax2.grid(True)

ax3.bar(['A', 'B', 'C'], [1, 2, 3])
ax3.grid(True)

ax4.hist(np.random.randn(1000), bins=30)
ax4.grid(True)

# Toggle entire figure to dark mode
dm.toggle_dark_mode(fig=fig)
plt.show()
```

#### 2. Toggle Individual Axis

```python
import matplotlib.pyplot as plt
import matplotlib.dark_mode as dm
import numpy as np

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Create identical plots
x = np.linspace(0, 2*np.pi, 100)
for ax in [ax1, ax2]:
    ax.plot(x, np.sin(x), 'b-', linewidth=2)
    ax.set_title('Sine Wave')
    ax.grid(True)

# Apply dark mode to only the second axis
dm.toggle_dark_mode(ax=ax2)
plt.show()
```

#### 3. Toggle Current Figure

```python
import matplotlib.pyplot as plt
import matplotlib.dark_mode as dm
import numpy as np

# Create a plot without storing figure reference
plt.figure(figsize=(10, 6))
x = np.linspace(0, 4*np.pi, 200)
plt.plot(x, np.sin(x), 'g-', label='sin(x)', linewidth=2)
plt.title('Current Figure Example')
plt.legend()
plt.grid(True)

# Toggle current figure to dark mode
dm.toggle_dark_mode()
plt.show()
```

#### 4. Data Color Adjustment

```python
import matplotlib.pyplot as plt
import matplotlib.dark_mode as dm
import numpy as np

# Create plot with dark colors that would be hard to see in dark mode
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), 'black', linewidth=3, label='black line')
ax.plot(x, np.cos(x), 'darkblue', linewidth=3, label='dark blue line')
ax.legend()
ax.grid(True)

# Toggle to dark mode with automatic data color adjustment
dm.toggle_dark_mode(fig=fig, adjust_data_colors=True)
plt.show()
```

### Custom Color Schemes

You can customize the dark mode color palette:

```python
import matplotlib.dark_mode as dm

# Set custom dark mode colors
dm.set_dark_mode_colors(
    background='#1a1a2e',  # Dark blue background
    text='#eee',           # Light text
    grid='#16213e',        # Blue grid
    spine='#0f3460',       # Darker blue spines
    tick='#eee',           # Light tick marks
    label='#eee'           # Light labels
)

# Now use dark mode with custom colors
dm.toggle_dark_mode(fig=fig)

# Reset to default colors
dm.set_dark_mode_colors()
```

### Utility Functions

#### Reset Stored Colors

```python
import matplotlib.dark_mode as dm

# Clear all stored original colors (useful for memory management)
dm.reset_to_defaults()
```

## Color Scheme

### Default Dark Mode Colors

- **Background**: `#121212` (Dark gray)
- **Text**: `#ffffff` (White)
- **Grid**: `#404040` (Medium gray)
- **Spines**: `#666666` (Light gray)
- **Ticks**: `#ffffff` (White)
- **Labels**: `#ffffff` (White)

### Default Light Mode Colors

- **Background**: `#ffffff` (White)
- **Text**: `#000000` (Black)
- **Grid**: `#b0b0b0` (Light gray)
- **Spines**: `#000000` (Black)
- **Ticks**: `#000000` (Black)
- **Labels**: `#000000` (Black)

## Implementation Details

### How It Works

1. **Color Detection**: The function examines the current background color to determine if the plot is in light or dark mode
2. **Color Storage**: On first use, original colors are stored in a weak reference dictionary to enable restoration
3. **Element Modification**: The function systematically updates:
   - Figure and axes backgrounds
   - Text elements (titles, labels)
   - Tick marks and tick labels
   - Axis spines
   - Grid lines
4. **Data Color Adjustment** (optional): Automatically brightens dark data colors for better visibility

### Memory Management

- Uses `weakref.WeakKeyDictionary` to store original colors
- Automatically cleans up when figures are garbage collected
- Provides `reset_to_defaults()` function for manual cleanup

### Supported Plot Elements

- ✅ Figure backgrounds
- ✅ Axes backgrounds
- ✅ Titles and labels
- ✅ Tick marks and tick labels
- ✅ Axis spines
- ✅ Grid lines
- ✅ Legend elements
- ✅ Line plots
- ✅ Scatter plots
- ✅ Bar plots
- ✅ Histograms
- ✅ Annotations

## Demo Scripts

### Test Script

Run the test script to verify functionality:

```bash
python test_dark_mode.py
```

### Visual Demo

Generate demonstration images:

```bash
python visual_demo.py
```

This creates several PNG files showing before/after comparisons:
- `demo_light_mode.png` / `demo_dark_mode.png`
- `comprehensive_light_mode.png` / `comprehensive_dark_mode.png`
- `single_axis_demo.png`
- `custom_colors_demo.png`
- `data_color_adjustment_demo.png`

### Interactive Demo

For interactive demonstration (requires display):

```bash
python dark_mode_demo.py
```

## Requirements

- matplotlib >= 3.0
- numpy
- Python >= 3.6

## Limitations

- Some custom plot elements may not be automatically adjusted
- Complex colormaps in data elements are preserved (not adjusted)
- Third-party matplotlib extensions may require additional handling

## Future Enhancements

Potential improvements for future versions:

1. **Smart Data Color Adjustment**: More sophisticated algorithms for adjusting data colors
2. **Theme Presets**: Pre-defined color schemes (e.g., "GitHub Dark", "VS Code Dark")
3. **Animation Support**: Smooth transitions between light and dark modes
4. **Configuration File**: Save/load custom color schemes
5. **Integration**: Direct integration with matplotlib style sheets

## Contributing

To contribute to this functionality:

1. Test with various plot types and configurations
2. Report issues with specific plot elements not being handled correctly
3. Suggest improvements for color schemes or functionality
4. Add support for additional matplotlib features

## License

This implementation follows the same license as matplotlib.