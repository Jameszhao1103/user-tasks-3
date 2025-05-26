"""
Dark mode toggle functionality for matplotlib plots.

This module provides functionality to toggle matplotlib plots between light and dark modes
with a single function call, while preserving the original appearance when toggling back.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import to_rgba
import weakref


# Global storage for original colors to enable toggling back
_original_colors = weakref.WeakKeyDictionary()

# Dark mode color scheme
DARK_COLORS = {
    'background': '#121212',
    'text': '#ffffff',
    'grid': '#404040',
    'spine': '#666666',
    'tick': '#ffffff',
    'label': '#ffffff'
}

# Light mode color scheme (matplotlib defaults)
LIGHT_COLORS = {
    'background': '#ffffff',
    'text': '#000000',
    'grid': '#b0b0b0',
    'spine': '#000000',
    'tick': '#000000',
    'label': '#000000'
}


def _is_dark_mode(fig):
    """Check if a figure is currently in dark mode by examining background color."""
    bg_color = fig.get_facecolor()
    # Convert to RGBA if needed
    if isinstance(bg_color, str):
        bg_color = to_rgba(bg_color)
    elif len(bg_color) == 3:
        bg_color = (*bg_color, 1.0)
    
    # Consider it dark mode if the background is closer to black than white
    brightness = sum(bg_color[:3]) / 3
    return brightness < 0.5


def _store_original_colors(fig):
    """Store original colors of figure elements for restoration."""
    if fig in _original_colors:
        return  # Already stored
    
    original = {
        'fig_facecolor': fig.get_facecolor(),
        'axes': []
    }
    
    for ax in fig.get_axes():
        ax_colors = {
            'facecolor': ax.get_facecolor(),
            'xaxis_color': ax.xaxis.label.get_color(),
            'yaxis_color': ax.yaxis.label.get_color(),
            'title_color': ax.title.get_color(),
            'tick_colors': {
                'x': [tick.get_color() for tick in ax.get_xticklabels()],
                'y': [tick.get_color() for tick in ax.get_yticklabels()]
            },
            'spine_colors': {spine_name: spine.get_edgecolor() 
                           for spine_name, spine in ax.spines.items()},
            'grid_color': None,  # Will be set if grid is visible
            'grid_alpha': None
        }
        
        # Store grid colors if grid is visible
        if ax.xaxis.get_gridlines() and len(ax.xaxis.get_gridlines()) > 0:
            grid_line = ax.xaxis.get_gridlines()[0]
            ax_colors['grid_color'] = grid_line.get_color()
            ax_colors['grid_alpha'] = grid_line.get_alpha()
        
        original['axes'].append(ax_colors)
    
    _original_colors[fig] = original


def _apply_dark_mode(fig):
    """Apply dark mode colors to figure."""
    # Set figure background
    fig.patch.set_facecolor(DARK_COLORS['background'])
    
    for ax in fig.get_axes():
        # Set axes background
        ax.set_facecolor(DARK_COLORS['background'])
        
        # Set text colors
        ax.xaxis.label.set_color(DARK_COLORS['label'])
        ax.yaxis.label.set_color(DARK_COLORS['label'])
        ax.title.set_color(DARK_COLORS['text'])
        
        # Set tick label colors
        for tick in ax.get_xticklabels():
            tick.set_color(DARK_COLORS['tick'])
        for tick in ax.get_yticklabels():
            tick.set_color(DARK_COLORS['tick'])
        
        # Set spine colors
        for spine in ax.spines.values():
            spine.set_edgecolor(DARK_COLORS['spine'])
        
        # Set tick colors
        ax.tick_params(axis='both', colors=DARK_COLORS['tick'])
        
        # Set grid colors if grid is visible
        if ax.xaxis.get_gridlines() and len(ax.xaxis.get_gridlines()) > 0:
            ax.grid(True, color=DARK_COLORS['grid'], alpha=0.3)


def _apply_light_mode(fig):
    """Restore original light mode colors to figure."""
    if fig not in _original_colors:
        # If no original colors stored, apply default light colors
        fig.patch.set_facecolor(LIGHT_COLORS['background'])
        
        for ax in fig.get_axes():
            ax.set_facecolor(LIGHT_COLORS['background'])
            ax.xaxis.label.set_color(LIGHT_COLORS['label'])
            ax.yaxis.label.set_color(LIGHT_COLORS['label'])
            ax.title.set_color(LIGHT_COLORS['text'])
            
            for tick in ax.get_xticklabels():
                tick.set_color(LIGHT_COLORS['tick'])
            for tick in ax.get_yticklabels():
                tick.set_color(LIGHT_COLORS['tick'])
            
            for spine in ax.spines.values():
                spine.set_edgecolor(LIGHT_COLORS['spine'])
            
            ax.tick_params(axis='both', colors=LIGHT_COLORS['tick'])
            
            if ax.xaxis.get_gridlines() and len(ax.xaxis.get_gridlines()) > 0:
                ax.grid(True, color=LIGHT_COLORS['grid'], alpha=0.5)
        return
    
    # Restore original colors
    original = _original_colors[fig]
    
    # Restore figure background
    fig.patch.set_facecolor(original['fig_facecolor'])
    
    # Restore axes colors
    for ax, ax_colors in zip(fig.get_axes(), original['axes']):
        ax.set_facecolor(ax_colors['facecolor'])
        ax.xaxis.label.set_color(ax_colors['xaxis_color'])
        ax.yaxis.label.set_color(ax_colors['yaxis_color'])
        ax.title.set_color(ax_colors['title_color'])
        
        # Restore tick label colors
        for tick, color in zip(ax.get_xticklabels(), ax_colors['tick_colors']['x']):
            tick.set_color(color)
        for tick, color in zip(ax.get_yticklabels(), ax_colors['tick_colors']['y']):
            tick.set_color(color)
        
        # Restore spine colors
        for spine_name, spine in ax.spines.items():
            if spine_name in ax_colors['spine_colors']:
                spine.set_edgecolor(ax_colors['spine_colors'][spine_name])
        
        # Restore grid colors if they were stored
        if ax_colors['grid_color'] is not None:
            ax.grid(True, color=ax_colors['grid_color'], alpha=ax_colors['grid_alpha'])


def toggle_dark_mode(ax=None, fig=None, adjust_data_colors=False):
    """
    Toggle between dark and light mode for matplotlib plots.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Specific axes to apply dark mode to. If provided, only this axes will be modified.
    fig : matplotlib.figure.Figure, optional
        Specific figure to apply dark mode to. If provided, all axes in this figure will be modified.
    adjust_data_colors : bool, default False
        If True, automatically adjust data element colors for better visibility in dark mode.
        This will modify line colors, marker colors, etc.
    
    Returns
    -------
    None
    
    Notes
    -----
    The function automatically detects the current mode (light/dark) and toggles to the opposite.
    Original colors are stored on first call to enable proper restoration when toggling back.
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.dark_mode as dm
    >>> 
    >>> # Create a simple plot
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [1, 4, 2])
    >>> 
    >>> # Toggle to dark mode
    >>> dm.toggle_dark_mode(fig=fig)
    >>> 
    >>> # Toggle back to light mode
    >>> dm.toggle_dark_mode(fig=fig)
    """
    # Determine which figure to work with
    if ax is not None:
        target_fig = ax.get_figure()
        target_axes = [ax]
    elif fig is not None:
        target_fig = fig
        target_axes = fig.get_axes()
    else:
        target_fig = plt.gcf()
        target_axes = target_fig.get_axes()
    
    if not target_axes:
        # No axes to work with
        return
    
    # Store original colors before first modification
    _store_original_colors(target_fig)
    
    # Determine current mode and toggle
    is_currently_dark = _is_dark_mode(target_fig)
    
    if is_currently_dark:
        # Switch to light mode
        if ax is not None:
            # For single axis, we need to handle it specially
            # since _apply_light_mode works on whole figures
            _apply_light_mode(target_fig)
        else:
            _apply_light_mode(target_fig)
    else:
        # Switch to dark mode
        if ax is not None:
            # Apply dark mode to specific axis
            ax.set_facecolor(DARK_COLORS['background'])
            ax.xaxis.label.set_color(DARK_COLORS['label'])
            ax.yaxis.label.set_color(DARK_COLORS['label'])
            ax.title.set_color(DARK_COLORS['text'])
            
            for tick in ax.get_xticklabels():
                tick.set_color(DARK_COLORS['tick'])
            for tick in ax.get_yticklabels():
                tick.set_color(DARK_COLORS['tick'])
            
            for spine in ax.spines.values():
                spine.set_edgecolor(DARK_COLORS['spine'])
            
            ax.tick_params(axis='both', colors=DARK_COLORS['tick'])
            
            if ax.xaxis.get_gridlines() and len(ax.xaxis.get_gridlines()) > 0:
                ax.grid(True, color=DARK_COLORS['grid'], alpha=0.3)
        else:
            _apply_dark_mode(target_fig)
    
    # Optionally adjust data colors for better visibility
    if adjust_data_colors and not is_currently_dark:
        _adjust_data_colors_for_dark_mode(target_axes)
    
    # Refresh the display
    target_fig.canvas.draw_idle()


def _adjust_data_colors_for_dark_mode(axes_list):
    """
    Adjust data element colors for better visibility in dark mode.
    
    This function brightens dark colors and adjusts very light colors
    to ensure good contrast against the dark background.
    """
    for ax in axes_list:
        # Adjust line colors
        for line in ax.get_lines():
            color = line.get_color()
            if isinstance(color, str) and color in ['k', 'black']:
                line.set_color('white')
            elif isinstance(color, str) and color in ['b', 'blue']:
                line.set_color('lightblue')
            elif isinstance(color, str) and color in ['g', 'green']:
                line.set_color('lightgreen')
            elif isinstance(color, str) and color in ['r', 'red']:
                line.set_color('lightcoral')
        
        # Adjust scatter plot colors
        for collection in ax.collections:
            # This handles scatter plots and other collections
            try:
                colors = collection.get_facecolors()
                if len(colors) > 0:
                    # Brighten dark colors
                    new_colors = []
                    for color in colors:
                        if len(color) >= 3:
                            r, g, b = color[:3]
                            brightness = (r + g + b) / 3
                            if brightness < 0.3:  # Very dark colors
                                # Brighten them
                                factor = 0.7 / max(brightness, 0.1)
                                new_color = [min(1.0, c * factor) for c in color[:3]]
                                if len(color) > 3:
                                    new_color.append(color[3])  # Preserve alpha
                                new_colors.append(new_color)
                            else:
                                new_colors.append(color)
                    collection.set_facecolors(new_colors)
            except (AttributeError, ValueError):
                # Some collections might not support color modification
                pass


def set_dark_mode_colors(background='#121212', text='#ffffff', grid='#404040', 
                        spine='#666666', tick='#ffffff', label='#ffffff'):
    """
    Customize the dark mode color scheme.
    
    Parameters
    ----------
    background : str, default '#121212'
        Background color for figures and axes
    text : str, default '#ffffff'
        Color for titles and text elements
    grid : str, default '#404040'
        Color for grid lines
    spine : str, default '#666666'
        Color for axis spines
    tick : str, default '#ffffff'
        Color for tick marks and tick labels
    label : str, default '#ffffff'
        Color for axis labels
    """
    global DARK_COLORS
    DARK_COLORS.update({
        'background': background,
        'text': text,
        'grid': grid,
        'spine': spine,
        'tick': tick,
        'label': label
    })


def reset_to_defaults():
    """Reset all stored original colors and clear the cache."""
    global _original_colors
    _original_colors.clear()