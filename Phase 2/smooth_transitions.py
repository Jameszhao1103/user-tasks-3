import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgba
import time
from typing import Dict, Any, Callable, Optional, Union, Tuple

class EasingFunctions:
    """Collection of easing functions for smooth transitions."""
    
    @staticmethod
    def linear(t: float) -> float:
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        return 1 - 2 * (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        return 1 - (1 - t) ** 3
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - 4 * (1 - t) ** 3

def interpolate_values(from_val: Union[float, np.ndarray], 
                      to_val: Union[float, np.ndarray], 
                      progress: float) -> Union[float, np.ndarray]:
    """Interpolate between two values or arrays."""
    return from_val + (to_val - from_val) * progress

def interpolate_colors(from_color: Union[str, tuple], 
                      to_color: Union[str, tuple], 
                      progress: float) -> tuple:
    """Interpolate between two colors."""
    from_rgba = to_rgba(from_color)
    to_rgba_val = to_rgba(to_color)
    
    return tuple(
        from_rgba[i] + (to_rgba_val[i] - from_rgba[i]) * progress
        for i in range(4)
    )

def smooth_transition(from_data: Dict[str, Any], 
                     to_data: Dict[str, Any], 
                     duration: float = 1.0, 
                     fps: int = 30,
                     easing: str = 'ease_in_out_quad',
                     plot_type: str = 'line',
                     **kwargs) -> animation.FuncAnimation:
    """
    Create a smooth animation transitioning between different states of a plot.
    
    Parameters:
    -----------
    from_data : dict
        Initial data state with keys like 'x', 'y', 'colors', 'sizes', etc.
    to_data : dict
        Final data state with same structure as from_data
    duration : float
        Duration of transition in seconds
    fps : int
        Frames per second for animation
    easing : str
        Easing function name from EasingFunctions class
    plot_type : str
        Type of plot ('line', 'scatter', 'bar')
    **kwargs
        Additional matplotlib plotting arguments
    
    Returns:
    --------
    matplotlib.animation.FuncAnimation
        Animation object
    """
    
    # Get easing function
    easing_func = getattr(EasingFunctions, easing, EasingFunctions.linear)
    
    # Calculate total frames
    total_frames = int(duration * fps)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
    
    # Initialize plot based on type
    if plot_type == 'line':
        line, = ax.plot(from_data.get('x', []), from_data.get('y', []), 
                       color=from_data.get('color', 'blue'),
                       linewidth=from_data.get('linewidth', 2),
                       **{k: v for k, v in kwargs.items() if k not in ['figsize']})
        plot_obj = line
    elif plot_type == 'scatter':
        scatter = ax.scatter(from_data.get('x', []), from_data.get('y', []),
                           c=from_data.get('colors', 'blue'),
                           s=from_data.get('sizes', 50),
                           **{k: v for k, v in kwargs.items() if k not in ['figsize']})
        plot_obj = scatter
    elif plot_type == 'bar':
        bars = ax.bar(from_data.get('x', []), from_data.get('y', []),
                     color=from_data.get('colors', 'blue'),
                     width=from_data.get('width', 0.8),
                     **{k: v for k, v in kwargs.items() if k not in ['figsize']})
        plot_obj = bars
    else:
        raise ValueError(f"Unsupported plot type: {plot_type}")
    
    # Set up axis limits
    all_x = np.concatenate([np.array(from_data.get('x', [])), 
                           np.array(to_data.get('x', []))])
    all_y = np.concatenate([np.array(from_data.get('y', [])), 
                           np.array(to_data.get('y', []))])
    
    if len(all_x) > 0 and len(all_y) > 0:
        ax.set_xlim(all_x.min() - 0.1 * (all_x.max() - all_x.min()),
                   all_x.max() + 0.1 * (all_x.max() - all_x.min()))
        ax.set_ylim(all_y.min() - 0.1 * (all_y.max() - all_y.min()),
                   all_y.max() + 0.1 * (all_y.max() - all_y.min()))
    
    def animate(frame):
        # Calculate progress (0 to 1)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1
        progress = min(1.0, max(0.0, progress))
        
        # Apply easing function
        eased_progress = easing_func(progress)
        
        # Update plot based on type
        if plot_type == 'line':
            # Interpolate y values
            if 'y' in from_data and 'y' in to_data:
                new_y = interpolate_values(np.array(from_data['y']), 
                                         np.array(to_data['y']), 
                                         eased_progress)
                plot_obj.set_ydata(new_y)
            
            # Interpolate x values if they change
            if 'x' in from_data and 'x' in to_data:
                new_x = interpolate_values(np.array(from_data['x']), 
                                         np.array(to_data['x']), 
                                         eased_progress)
                plot_obj.set_xdata(new_x)
            
            # Interpolate color
            if 'color' in from_data and 'color' in to_data:
                new_color = interpolate_colors(from_data['color'], 
                                             to_data['color'], 
                                             eased_progress)
                plot_obj.set_color(new_color)
            
            # Interpolate line width
            if 'linewidth' in from_data and 'linewidth' in to_data:
                new_width = interpolate_values(from_data['linewidth'], 
                                             to_data['linewidth'], 
                                             eased_progress)
                plot_obj.set_linewidth(new_width)
        
        elif plot_type == 'scatter':
            # Update scatter plot data
            if 'x' in from_data and 'x' in to_data:
                new_x = interpolate_values(np.array(from_data['x']), 
                                         np.array(to_data['x']), 
                                         eased_progress)
            else:
                new_x = from_data.get('x', [])
            
            if 'y' in from_data and 'y' in to_data:
                new_y = interpolate_values(np.array(from_data['y']), 
                                         np.array(to_data['y']), 
                                         eased_progress)
            else:
                new_y = from_data.get('y', [])
            
            plot_obj.set_offsets(np.column_stack([new_x, new_y]))
            
            # Interpolate sizes
            if 'sizes' in from_data and 'sizes' in to_data:
                new_sizes = interpolate_values(np.array(from_data['sizes']), 
                                             np.array(to_data['sizes']), 
                                             eased_progress)
                plot_obj.set_sizes(new_sizes)
            
            # Interpolate colors
            if 'colors' in from_data and 'colors' in to_data:
                if isinstance(from_data['colors'], str) and isinstance(to_data['colors'], str):
                    new_color = interpolate_colors(from_data['colors'], 
                                                 to_data['colors'], 
                                                 eased_progress)
                    plot_obj.set_color(new_color)
        
        elif plot_type == 'bar':
            # Update bar heights
            if 'y' in from_data and 'y' in to_data:
                new_heights = interpolate_values(np.array(from_data['y']), 
                                               np.array(to_data['y']), 
                                               eased_progress)
                for bar, height in zip(plot_obj, new_heights):
                    bar.set_height(height)
            
            # Interpolate colors
            if 'colors' in from_data and 'colors' in to_data:
                if isinstance(from_data['colors'], str) and isinstance(to_data['colors'], str):
                    new_color = interpolate_colors(from_data['colors'], 
                                                 to_data['colors'], 
                                                 eased_progress)
                    for bar in plot_obj:
                        bar.set_color(new_color)
        
        return [plot_obj] if plot_type != 'bar' else plot_obj
    
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=total_frames, 
                                 interval=1000/fps, blit=False, repeat=False)
    
    return anim

def transition_plot_state(fig_from: plt.Figure, 
                         fig_to: plt.Figure, 
                         duration: float = 1.0, 
                         fps: int = 30,
                         easing: str = 'ease_in_out_quad') -> animation.FuncAnimation:
    """
    Create a transition between two complete figure states.
    
    Parameters:
    -----------
    fig_from : matplotlib.figure.Figure
        Initial figure state
    fig_to : matplotlib.figure.Figure
        Final figure state
    duration : float
        Duration of transition in seconds
    fps : int
        Frames per second for animation
    easing : str
        Easing function name
    
    Returns:
    --------
    matplotlib.animation.FuncAnimation
        Animation object
    """
    
    # Get easing function
    easing_func = getattr(EasingFunctions, easing, EasingFunctions.linear)
    
    # Calculate total frames
    total_frames = int(duration * fps)
    
    # Create new figure for animation
    fig_anim = plt.figure(figsize=fig_from.get_size_inches())
    ax_anim = fig_anim.add_subplot(111)
    
    # Extract data from both figures
    ax_from = fig_from.axes[0] if fig_from.axes else None
    ax_to = fig_to.axes[0] if fig_to.axes else None
    
    if not ax_from or not ax_to:
        raise ValueError("Both figures must have at least one axis")
    
    def animate(frame):
        # Clear the animation axis
        ax_anim.clear()
        
        # Calculate progress
        progress = frame / (total_frames - 1) if total_frames > 1 else 1
        progress = min(1.0, max(0.0, progress))
        eased_progress = easing_func(progress)
        
        # Interpolate between the two states
        # This is a simplified version - in practice, you'd want more sophisticated
        # figure state interpolation
        alpha_from = 1 - eased_progress
        alpha_to = eased_progress
        
        # Copy elements from first figure with reduced alpha
        for line in ax_from.get_lines():
            x, y = line.get_data()
            ax_anim.plot(x, y, color=line.get_color(), 
                        alpha=alpha_from, linewidth=line.get_linewidth())
        
        # Copy elements from second figure with increasing alpha
        for line in ax_to.get_lines():
            x, y = line.get_data()
            ax_anim.plot(x, y, color=line.get_color(), 
                        alpha=alpha_to, linewidth=line.get_linewidth())
        
        # Set axis properties (interpolated)
        xlim_from = ax_from.get_xlim()
        xlim_to = ax_to.get_xlim()
        ylim_from = ax_from.get_ylim()
        ylim_to = ax_to.get_ylim()
        
        new_xlim = interpolate_values(np.array(xlim_from), np.array(xlim_to), eased_progress)
        new_ylim = interpolate_values(np.array(ylim_from), np.array(ylim_to), eased_progress)
        
        ax_anim.set_xlim(new_xlim)
        ax_anim.set_ylim(new_ylim)
        
        # Set labels
        if progress < 0.5:
            ax_anim.set_xlabel(ax_from.get_xlabel())
            ax_anim.set_ylabel(ax_from.get_ylabel())
            ax_anim.set_title(ax_from.get_title())
        else:
            ax_anim.set_xlabel(ax_to.get_xlabel())
            ax_anim.set_ylabel(ax_to.get_ylabel())
            ax_anim.set_title(ax_to.get_title())
    
    # Create animation
    anim = animation.FuncAnimation(fig_anim, animate, frames=total_frames, 
                                 interval=1000/fps, blit=False, repeat=False)
    
    return anim