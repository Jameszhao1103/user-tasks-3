"""
Smooth transitions and animations for matplotlib plots.

This module provides functionality to create smooth animated transitions between
different states of matplotlib plots, including data changes, color transitions,
and complete figure state changes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.collections import PathCollection
import copy
import time
from typing import Union, Dict, List, Tuple, Optional, Callable, Any


# Easing functions for smooth transitions
class EasingFunctions:
    """Collection of easing functions for smooth animations."""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing (no acceleration)."""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease-in (accelerating from zero velocity)."""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease-out (decelerating to zero velocity)."""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease-in-out (acceleration until halfway, then deceleration)."""
        if t < 0.5:
            return 2 * t * t
        return 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease-in."""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease-out."""
        return 1 - pow(1 - t, 3)
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease-in-out."""
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2
    
    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sinusoidal ease-in."""
        return 1 - np.cos((t * np.pi) / 2)
    
    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sinusoidal ease-out."""
        return np.sin((t * np.pi) / 2)
    
    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sinusoidal ease-in-out."""
        return -(np.cos(np.pi * t) - 1) / 2


def interpolate_values(start_val: Any, end_val: Any, progress: float) -> Any:
    """
    Interpolate between two values based on progress (0.0 to 1.0).
    
    Parameters
    ----------
    start_val : Any
        Starting value
    end_val : Any
        Ending value
    progress : float
        Progress from 0.0 to 1.0
        
    Returns
    -------
    Any
        Interpolated value
    """
    if isinstance(start_val, (int, float)) and isinstance(end_val, (int, float)):
        return start_val + (end_val - start_val) * progress
    elif isinstance(start_val, np.ndarray) and isinstance(end_val, np.ndarray):
        return start_val + (end_val - start_val) * progress
    elif isinstance(start_val, (list, tuple)) and isinstance(end_val, (list, tuple)):
        if len(start_val) == len(end_val):
            return [interpolate_values(s, e, progress) for s, e in zip(start_val, end_val)]
    elif isinstance(start_val, str) and isinstance(end_val, str):
        # For colors, try to interpolate if they're valid color specifications
        try:
            import matplotlib.colors as mcolors
            start_rgb = mcolors.to_rgb(start_val)
            end_rgb = mcolors.to_rgb(end_val)
            interpolated_rgb = interpolate_values(start_rgb, end_rgb, progress)
            return interpolated_rgb
        except:
            # If color interpolation fails, return start or end based on progress
            return start_val if progress < 0.5 else end_val
    
    # Default: return start or end based on progress threshold
    return start_val if progress < 0.5 else end_val


def smooth_transition(from_data: Union[Dict, np.ndarray, List], 
                     to_data: Union[Dict, np.ndarray, List],
                     duration: float = 1.0,
                     fps: int = 30,
                     easing: Union[str, Callable] = 'ease_in_out_quad',
                     ax: Optional[Axes] = None,
                     plot_type: str = 'line',
                     **kwargs) -> animation.FuncAnimation:
    """
    Create a smooth animated transition between two data states.
    
    Parameters
    ----------
    from_data : dict, array-like, or list
        Initial data state. Can be:
        - For line plots: dict with 'x', 'y' keys or just y-values
        - For scatter plots: dict with 'x', 'y', optionally 'sizes', 'colors'
        - For bar plots: dict with 'heights', optionally 'colors'
        - Array-like for simple y-value transitions
    to_data : dict, array-like, or list
        Final data state (same format as from_data)
    duration : float, default 1.0
        Duration of transition in seconds
    fps : int, default 30
        Frames per second for animation
    easing : str or callable, default 'ease_in_out_quad'
        Easing function name or custom function
    ax : matplotlib.axes.Axes, optional
        Axes to animate. If None, uses current axes
    plot_type : str, default 'line'
        Type of plot: 'line', 'scatter', 'bar'
    **kwargs
        Additional arguments passed to the plot function
        
    Returns
    -------
    matplotlib.animation.FuncAnimation
        Animation object
    """
    if ax is None:
        ax = plt.gca()
    
    # Get easing function
    if isinstance(easing, str):
        easing_func = getattr(EasingFunctions, easing, EasingFunctions.linear)
    else:
        easing_func = easing
    
    # Normalize data format
    from_data_norm = _normalize_data(from_data, plot_type)
    to_data_norm = _normalize_data(to_data, plot_type)
    
    # Calculate number of frames
    num_frames = int(duration * fps)
    
    # Store original plot elements for cleanup
    original_elements = []
    
    def animate(frame):
        # Clear previous frame elements
        for elem in original_elements:
            if hasattr(elem, 'remove'):
                try:
                    elem.remove()
                except:
                    pass
        original_elements.clear()
        
        # Calculate progress with easing
        progress = frame / (num_frames - 1) if num_frames > 1 else 1.0
        progress = max(0.0, min(1.0, progress))
        eased_progress = easing_func(progress)
        
        # Interpolate data
        current_data = {}
        for key in from_data_norm:
            if key in to_data_norm:
                current_data[key] = interpolate_values(
                    from_data_norm[key], to_data_norm[key], eased_progress
                )
            else:
                current_data[key] = from_data_norm[key]
        
        # Create plot based on type
        if plot_type == 'line':
            line, = ax.plot(current_data.get('x', range(len(current_data['y']))), 
                           current_data['y'], **kwargs)
            original_elements.append(line)
        elif plot_type == 'scatter':
            # Handle scatter plot parameters carefully to avoid conflicts
            scatter_kwargs = kwargs.copy()
            if 'sizes' in current_data:
                scatter_kwargs['s'] = current_data['sizes']
            elif 's' not in scatter_kwargs:
                scatter_kwargs['s'] = 50
            
            if 'colors' in current_data:
                scatter_kwargs['c'] = current_data['colors']
            elif 'c' not in scatter_kwargs and 'color' not in scatter_kwargs:
                scatter_kwargs['c'] = 'blue'
            
            scatter = ax.scatter(current_data['x'], current_data['y'], **scatter_kwargs)
            original_elements.append(scatter)
        elif plot_type == 'bar':
            # Handle bar plot parameters carefully
            bar_kwargs = kwargs.copy()
            x_pos = current_data.get('x', range(len(current_data['heights'])))
            
            if 'colors' in current_data:
                bar_kwargs['color'] = current_data['colors']
            elif 'color' not in bar_kwargs:
                bar_kwargs['color'] = 'blue'
            
            bars = ax.bar(x_pos, current_data['heights'], **bar_kwargs)
            original_elements.extend(bars)
        
        return original_elements
    
    # Create animation
    anim = animation.FuncAnimation(
        ax.figure, animate, frames=num_frames, interval=1000/fps, 
        blit=False, repeat=False
    )
    
    return anim


def transition_plot_state(fig_from: Figure, 
                         fig_to: Figure,
                         duration: float = 1.0,
                         fps: int = 30,
                         easing: Union[str, Callable] = 'ease_in_out_quad') -> animation.FuncAnimation:
    """
    Create a smooth transition between two complete figure states.
    
    Parameters
    ----------
    fig_from : matplotlib.figure.Figure
        Initial figure state
    fig_to : matplotlib.figure.Figure
        Final figure state
    duration : float, default 1.0
        Duration of transition in seconds
    fps : int, default 30
        Frames per second for animation
    easing : str or callable, default 'ease_in_out_quad'
        Easing function name or custom function
        
    Returns
    -------
    matplotlib.animation.FuncAnimation
        Animation object
    """
    # Get easing function
    if isinstance(easing, str):
        easing_func = getattr(EasingFunctions, easing, EasingFunctions.linear)
    else:
        easing_func = easing
    
    # Extract data from both figures
    from_states = _extract_figure_state(fig_from)
    to_states = _extract_figure_state(fig_to)
    
    # Create new figure for animation
    anim_fig = plt.figure(figsize=fig_from.get_size_inches())
    
    # Calculate number of frames
    num_frames = int(duration * fps)
    
    def animate(frame):
        anim_fig.clear()
        
        # Calculate progress with easing
        progress = frame / (num_frames - 1) if num_frames > 1 else 1.0
        progress = max(0.0, min(1.0, progress))
        eased_progress = easing_func(progress)
        
        # Interpolate between figure states
        _render_interpolated_figure(anim_fig, from_states, to_states, eased_progress)
        
        return anim_fig.get_children()
    
    # Create animation
    anim = animation.FuncAnimation(
        anim_fig, animate, frames=num_frames, interval=1000/fps,
        blit=False, repeat=False
    )
    
    return anim


def _normalize_data(data: Union[Dict, np.ndarray, List], plot_type: str) -> Dict:
    """Normalize data to a consistent dictionary format."""
    if isinstance(data, dict):
        return data.copy()
    
    # Convert array-like data to dictionary format
    if plot_type == 'line':
        if isinstance(data, (list, tuple, np.ndarray)):
            return {'y': np.array(data)}
    elif plot_type == 'scatter':
        if isinstance(data, (list, tuple)) and len(data) == 2:
            return {'x': np.array(data[0]), 'y': np.array(data[1])}
    elif plot_type == 'bar':
        if isinstance(data, (list, tuple, np.ndarray)):
            return {'heights': np.array(data)}
    
    raise ValueError(f"Cannot normalize data format for plot_type '{plot_type}'")


def _extract_figure_state(fig: Figure) -> Dict:
    """Extract the state of a figure for interpolation."""
    state = {
        'axes': [],
        'figure_props': {
            'facecolor': fig.get_facecolor(),
            'size': fig.get_size_inches()
        }
    }
    
    for ax in fig.get_axes():
        ax_state = {
            'xlim': ax.get_xlim(),
            'ylim': ax.get_ylim(),
            'title': ax.get_title(),
            'xlabel': ax.get_xlabel(),
            'ylabel': ax.get_ylabel(),
            'facecolor': ax.get_facecolor(),
            'lines': [],
            'collections': [],
            'patches': []
        }
        
        # Extract line data
        for line in ax.get_lines():
            line_data = {
                'xdata': line.get_xdata(),
                'ydata': line.get_ydata(),
                'color': line.get_color(),
                'linewidth': line.get_linewidth(),
                'linestyle': line.get_linestyle(),
                'marker': line.get_marker(),
                'markersize': line.get_markersize()
            }
            ax_state['lines'].append(line_data)
        
        # Extract collection data (scatter plots, etc.)
        for collection in ax.collections:
            if isinstance(collection, PathCollection):
                # Scatter plot
                offsets = collection.get_offsets()
                sizes = collection.get_sizes()
                colors = collection.get_facecolors()
                coll_data = {
                    'type': 'scatter',
                    'offsets': offsets,
                    'sizes': sizes,
                    'colors': colors
                }
                ax_state['collections'].append(coll_data)
        
        # Extract patch data (bar plots, etc.)
        for patch in ax.patches:
            if isinstance(patch, Rectangle):
                # Bar chart rectangle
                patch_data = {
                    'type': 'rectangle',
                    'xy': patch.get_xy(),
                    'width': patch.get_width(),
                    'height': patch.get_height(),
                    'facecolor': patch.get_facecolor(),
                    'edgecolor': patch.get_edgecolor()
                }
                ax_state['patches'].append(patch_data)
        
        state['axes'].append(ax_state)
    
    return state


def _render_interpolated_figure(fig: Figure, from_state: Dict, to_state: Dict, progress: float):
    """Render an interpolated figure state."""
    # Interpolate figure properties
    fig_props = interpolate_values(from_state['figure_props'], to_state['figure_props'], progress)
    fig.patch.set_facecolor(fig_props['facecolor'])
    
    # Handle axes
    num_axes = min(len(from_state['axes']), len(to_state['axes']))
    
    for i in range(num_axes):
        from_ax_state = from_state['axes'][i]
        to_ax_state = to_state['axes'][i]
        
        # Create or get axis
        if i < len(fig.get_axes()):
            ax = fig.get_axes()[i]
        else:
            ax = fig.add_subplot(1, 1, 1)  # Simple case - could be enhanced
        
        # Interpolate axis properties
        xlim = interpolate_values(from_ax_state['xlim'], to_ax_state['xlim'], progress)
        ylim = interpolate_values(from_ax_state['ylim'], to_ax_state['ylim'], progress)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        # Set labels (no interpolation for text)
        if progress < 0.5:
            ax.set_title(from_ax_state['title'])
            ax.set_xlabel(from_ax_state['xlabel'])
            ax.set_ylabel(from_ax_state['ylabel'])
        else:
            ax.set_title(to_ax_state['title'])
            ax.set_xlabel(to_ax_state['xlabel'])
            ax.set_ylabel(to_ax_state['ylabel'])
        
        # Interpolate background color
        facecolor = interpolate_values(from_ax_state['facecolor'], to_ax_state['facecolor'], progress)
        ax.set_facecolor(facecolor)
        
        # Interpolate lines
        num_lines = min(len(from_ax_state['lines']), len(to_ax_state['lines']))
        for j in range(num_lines):
            from_line = from_ax_state['lines'][j]
            to_line = to_ax_state['lines'][j]
            
            # Interpolate line data
            xdata = interpolate_values(from_line['xdata'], to_line['xdata'], progress)
            ydata = interpolate_values(from_line['ydata'], to_line['ydata'], progress)
            color = interpolate_values(from_line['color'], to_line['color'], progress)
            linewidth = interpolate_values(from_line['linewidth'], to_line['linewidth'], progress)
            markersize = interpolate_values(from_line['markersize'], to_line['markersize'], progress)
            
            ax.plot(xdata, ydata, color=color, linewidth=linewidth,
                   linestyle=from_line['linestyle'], marker=from_line['marker'],
                   markersize=markersize)
        
        # Interpolate collections (scatter plots)
        num_collections = min(len(from_ax_state['collections']), len(to_ax_state['collections']))
        for j in range(num_collections):
            from_coll = from_ax_state['collections'][j]
            to_coll = to_ax_state['collections'][j]
            
            if from_coll['type'] == 'scatter' and to_coll['type'] == 'scatter':
                offsets = interpolate_values(from_coll['offsets'], to_coll['offsets'], progress)
                sizes = interpolate_values(from_coll['sizes'], to_coll['sizes'], progress)
                colors = interpolate_values(from_coll['colors'], to_coll['colors'], progress)
                
                ax.scatter(offsets[:, 0], offsets[:, 1], s=sizes, c=colors)
        
        # Interpolate patches (bar charts)
        num_patches = min(len(from_ax_state['patches']), len(to_ax_state['patches']))
        for j in range(num_patches):
            from_patch = from_ax_state['patches'][j]
            to_patch = to_ax_state['patches'][j]
            
            if from_patch['type'] == 'rectangle' and to_patch['type'] == 'rectangle':
                xy = interpolate_values(from_patch['xy'], to_patch['xy'], progress)
                width = interpolate_values(from_patch['width'], to_patch['width'], progress)
                height = interpolate_values(from_patch['height'], to_patch['height'], progress)
                facecolor = interpolate_values(from_patch['facecolor'], to_patch['facecolor'], progress)
                
                rect = Rectangle(xy, width, height, facecolor=facecolor)
                ax.add_patch(rect)


# Convenience functions for common transition types
def transition_line_data(ax: Axes, from_y: np.ndarray, to_y: np.ndarray, 
                        duration: float = 1.0, fps: int = 30, **kwargs) -> animation.FuncAnimation:
    """Convenience function for transitioning line plot y-data."""
    return smooth_transition(
        from_data={'y': from_y},
        to_data={'y': to_y},
        duration=duration,
        fps=fps,
        ax=ax,
        plot_type='line',
        **kwargs
    )


def transition_scatter_data(ax: Axes, from_xy: Tuple[np.ndarray, np.ndarray], 
                           to_xy: Tuple[np.ndarray, np.ndarray],
                           duration: float = 1.0, fps: int = 30, **kwargs) -> animation.FuncAnimation:
    """Convenience function for transitioning scatter plot data."""
    return smooth_transition(
        from_data={'x': from_xy[0], 'y': from_xy[1]},
        to_data={'x': to_xy[0], 'y': to_xy[1]},
        duration=duration,
        fps=fps,
        ax=ax,
        plot_type='scatter',
        **kwargs
    )


def transition_bar_heights(ax: Axes, from_heights: np.ndarray, to_heights: np.ndarray,
                          duration: float = 1.0, fps: int = 30, **kwargs) -> animation.FuncAnimation:
    """Convenience function for transitioning bar chart heights."""
    return smooth_transition(
        from_data={'heights': from_heights},
        to_data={'heights': to_heights},
        duration=duration,
        fps=fps,
        ax=ax,
        plot_type='bar',
        **kwargs
    )