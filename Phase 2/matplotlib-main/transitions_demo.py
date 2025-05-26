#!/usr/bin/env python3
"""
Comprehensive demo of matplotlib smooth transitions functionality.

This script demonstrates various types of smooth transitions between plot states,
including line plots, scatter plots, bar charts, and complete figure transitions.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Add the lib directory to the path so we can import our transitions module
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Import the transitions module directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib'))
import transitions as mt


def demo_line_transition():
    """Demonstrate smooth transition between line plot data."""
    print("Creating line plot transition demo...")
    
    # Create initial data
    x = np.linspace(0, 4*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x) * np.exp(-x/8)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 4*np.pi)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title('Line Plot Transition Demo', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    
    # Create transition animation
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
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('line_transition_demo.gif', writer=writer)
    print("✓ Saved line transition as 'line_transition_demo.gif'")
    
    plt.close(fig)


def demo_scatter_transition():
    """Demonstrate smooth transition between scatter plot data."""
    print("Creating scatter plot transition demo...")
    
    # Create initial and final data
    np.random.seed(42)
    n_points = 50
    
    # Initial state: random circle
    theta1 = np.linspace(0, 2*np.pi, n_points)
    r1 = 1 + 0.3 * np.random.randn(n_points)
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)
    
    # Final state: spiral
    theta2 = np.linspace(0, 4*np.pi, n_points)
    r2 = theta2 / (2*np.pi)
    x2 = r2 * np.cos(theta2)
    y2 = r2 * np.sin(theta2)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title('Scatter Plot Transition Demo', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Create sizes and colors that change
    sizes1 = np.full(n_points, 50)
    sizes2 = np.linspace(20, 100, n_points)
    colors1 = ['blue'] * n_points
    colors2 = plt.cm.viridis(np.linspace(0, 1, n_points))
    
    # Create transition animation
    anim = mt.smooth_transition(
        from_data={'x': x1, 'y': y1, 'sizes': sizes1, 'colors': colors1},
        to_data={'x': x2, 'y': y2, 'sizes': sizes2, 'colors': colors2},
        duration=3.0,
        fps=30,
        easing='ease_in_out_sine',
        ax=ax,
        plot_type='scatter',
        alpha=0.7
    )
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('scatter_transition_demo.gif', writer=writer)
    print("✓ Saved scatter transition as 'scatter_transition_demo.gif'")
    
    plt.close(fig)


def demo_bar_transition():
    """Demonstrate smooth transition between bar chart data."""
    print("Creating bar chart transition demo...")
    
    # Create data
    categories = ['A', 'B', 'C', 'D', 'E', 'F']
    heights1 = np.array([3, 7, 2, 5, 8, 4])
    heights2 = np.array([8, 2, 6, 3, 1, 7])
    
    # Create colors that transition
    colors1 = ['red', 'green', 'blue', 'orange', 'purple', 'brown']
    colors2 = ['cyan', 'magenta', 'yellow', 'pink', 'gray', 'olive']
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_ylim(0, 10)
    ax.set_title('Bar Chart Transition Demo', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.grid(True, axis='y', alpha=0.3)
    
    # Set x-tick labels
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    
    # Create transition animation
    anim = mt.smooth_transition(
        from_data={'x': range(len(categories)), 'heights': heights1, 'colors': colors1},
        to_data={'x': range(len(categories)), 'heights': heights2, 'colors': colors2},
        duration=2.5,
        fps=30,
        easing='ease_in_out_quad',
        ax=ax,
        plot_type='bar',
        alpha=0.8
    )
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('bar_transition_demo.gif', writer=writer)
    print("✓ Saved bar transition as 'bar_transition_demo.gif'")
    
    plt.close(fig)


def demo_easing_functions():
    """Demonstrate different easing functions."""
    print("Creating easing functions comparison demo...")
    
    # Create data for demonstration
    x = np.linspace(0, 2*np.pi, 50)
    y1 = np.sin(x)
    y2 = np.cos(x) * 2
    
    easing_functions = [
        'linear',
        'ease_in_quad',
        'ease_out_quad', 
        'ease_in_out_quad',
        'ease_in_cubic',
        'ease_out_cubic',
        'ease_in_out_cubic',
        'ease_in_sine',
        'ease_out_sine',
        'ease_in_out_sine'
    ]
    
    # Create a grid of subplots
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.suptitle('Easing Functions Comparison', fontsize=16, fontweight='bold')
    axes = axes.flatten()
    
    animations = []
    
    for i, easing in enumerate(easing_functions):
        ax = axes[i]
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-2.5, 2.5)
        ax.set_title(f'{easing}', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Create transition for this easing function
        anim = mt.smooth_transition(
            from_data={'x': x, 'y': y1},
            to_data={'x': x, 'y': y2},
            duration=2.0,
            fps=30,
            easing=easing,
            ax=ax,
            plot_type='line',
            color='red',
            linewidth=2
        )
        animations.append(anim)
    
    plt.tight_layout()
    
    # Save the first animation as an example
    writer = animation.PillowWriter(fps=30)
    animations[0].save('easing_comparison_demo.gif', writer=writer)
    print("✓ Saved easing comparison as 'easing_comparison_demo.gif'")
    
    plt.close(fig)


def demo_figure_state_transition():
    """Demonstrate transition between complete figure states."""
    print("Creating figure state transition demo...")
    
    # Create first figure state
    fig1 = plt.figure(figsize=(10, 6))
    ax1 = fig1.add_subplot(111)
    
    # Simple line plot
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_title('Initial State: Sine Wave')
    ax1.set_xlabel('X values')
    ax1.set_ylabel('Y values')
    ax1.grid(True)
    ax1.set_facecolor('lightblue')
    
    # Create second figure state
    fig2 = plt.figure(figsize=(10, 6))
    ax2 = fig2.add_subplot(111)
    
    # Scatter plot with different data
    np.random.seed(123)
    x_scatter = np.random.randn(100)
    y_scatter = np.random.randn(100)
    ax2.scatter(x_scatter, y_scatter, c='red', alpha=0.6)
    ax2.set_title('Final State: Random Scatter')
    ax2.set_xlabel('Random X')
    ax2.set_ylabel('Random Y')
    ax2.grid(True)
    ax2.set_facecolor('lightcoral')
    
    # Create transition animation
    anim = mt.transition_plot_state(
        fig_from=fig1,
        fig_to=fig2,
        duration=3.0,
        fps=30,
        easing='ease_in_out_cubic'
    )
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('figure_state_transition_demo.gif', writer=writer)
    print("✓ Saved figure state transition as 'figure_state_transition_demo.gif'")
    
    plt.close(fig1)
    plt.close(fig2)
    plt.close(anim._fig)


def demo_complex_transition():
    """Demonstrate a complex transition with multiple elements."""
    print("Creating complex multi-element transition demo...")
    
    # Create figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Complex Multi-Element Transition Demo', fontsize=16, fontweight='bold')
    
    # Subplot 1: Line plot transition
    x = np.linspace(0, 2*np.pi, 100)
    y1_line = np.sin(x)
    y2_line = np.sin(2*x) * np.exp(-x/3)
    
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_title('Line Transition')
    ax1.grid(True, alpha=0.3)
    
    anim1 = mt.smooth_transition(
        from_data={'x': x, 'y': y1_line},
        to_data={'x': x, 'y': y2_line},
        duration=3.0,
        fps=30,
        easing='ease_in_out_quad',
        ax=ax1,
        plot_type='line',
        color='blue',
        linewidth=2
    )
    
    # Subplot 2: Scatter transition
    np.random.seed(42)
    n = 30
    x1_scatter = np.random.randn(n)
    y1_scatter = np.random.randn(n)
    x2_scatter = np.random.randn(n) * 2
    y2_scatter = np.random.randn(n) * 2
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_title('Scatter Transition')
    ax2.grid(True, alpha=0.3)
    
    anim2 = mt.smooth_transition(
        from_data={'x': x1_scatter, 'y': y1_scatter},
        to_data={'x': x2_scatter, 'y': y2_scatter},
        duration=3.0,
        fps=30,
        easing='ease_in_out_cubic',
        ax=ax2,
        plot_type='scatter',
        color='red',
        s=50,
        alpha=0.7
    )
    
    # Subplot 3: Bar transition
    categories = ['A', 'B', 'C', 'D', 'E']
    heights1 = np.array([2, 5, 3, 8, 1])
    heights2 = np.array([7, 1, 6, 2, 4])
    
    ax3.set_ylim(0, 10)
    ax3.set_title('Bar Transition')
    ax3.set_xticks(range(len(categories)))
    ax3.set_xticklabels(categories)
    ax3.grid(True, axis='y', alpha=0.3)
    
    anim3 = mt.smooth_transition(
        from_data={'heights': heights1},
        to_data={'heights': heights2},
        duration=3.0,
        fps=30,
        easing='ease_in_out_sine',
        ax=ax3,
        plot_type='bar',
        color='green',
        alpha=0.8
    )
    
    # Subplot 4: Another line with different easing
    y1_line2 = np.cos(x)
    y2_line2 = np.tan(x/2) * 0.5
    
    ax4.set_xlim(0, 2*np.pi)
    ax4.set_ylim(-2, 2)
    ax4.set_title('Line with Different Easing')
    ax4.grid(True, alpha=0.3)
    
    anim4 = mt.smooth_transition(
        from_data={'x': x, 'y': y1_line2},
        to_data={'x': x, 'y': y2_line2},
        duration=3.0,
        fps=30,
        easing='ease_out_cubic',
        ax=ax4,
        plot_type='line',
        color='purple',
        linewidth=2
    )
    
    plt.tight_layout()
    
    # Save one of the animations as an example
    writer = animation.PillowWriter(fps=30)
    anim1.save('complex_transition_demo.gif', writer=writer)
    print("✓ Saved complex transition as 'complex_transition_demo.gif'")
    
    plt.close(fig)


def demo_convenience_functions():
    """Demonstrate the convenience functions."""
    print("Creating convenience functions demo...")
    
    # Line data transition
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Convenience Functions Demo', fontsize=16, fontweight='bold')
    
    # Line transition
    x = np.linspace(0, 2*np.pi, 50)
    y1 = np.sin(x)
    y2 = np.cos(x) * 2
    
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_title('Line Data Transition')
    ax1.grid(True, alpha=0.3)
    
    anim1 = mt.transition_line_data(
        ax=ax1,
        from_y=y1,
        to_y=y2,
        duration=2.0,
        fps=30,
        color='blue',
        linewidth=2
    )
    
    # Scatter transition
    np.random.seed(42)
    x1 = np.random.randn(30)
    y1 = np.random.randn(30)
    x2 = np.random.randn(30) * 2
    y2 = np.random.randn(30) * 2
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_title('Scatter Data Transition')
    ax2.grid(True, alpha=0.3)
    
    anim2 = mt.transition_scatter_data(
        ax=ax2,
        from_xy=(x1, y1),
        to_xy=(x2, y2),
        duration=2.0,
        fps=30,
        color='red',
        s=50,
        alpha=0.7
    )
    
    # Bar transition
    heights1 = np.array([3, 7, 2, 5, 8])
    heights2 = np.array([8, 2, 6, 3, 1])
    
    ax3.set_ylim(0, 10)
    ax3.set_title('Bar Heights Transition')
    ax3.grid(True, axis='y', alpha=0.3)
    
    anim3 = mt.transition_bar_heights(
        ax=ax3,
        from_heights=heights1,
        to_heights=heights2,
        duration=2.0,
        fps=30,
        color='green',
        alpha=0.8
    )
    
    plt.tight_layout()
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim1.save('convenience_functions_demo.gif', writer=writer)
    print("✓ Saved convenience functions demo as 'convenience_functions_demo.gif'")
    
    plt.close(fig)


def main():
    """Run all transition demonstrations."""
    print("=== Matplotlib Smooth Transitions Demo ===")
    print("This script demonstrates various types of smooth transitions")
    print("between different plot states.\n")
    
    try:
        demo_line_transition()
        demo_scatter_transition()
        demo_bar_transition()
        demo_easing_functions()
        demo_figure_state_transition()
        demo_complex_transition()
        demo_convenience_functions()
        
        print("\n=== All Demonstrations Complete ===")
        print("Generated animations:")
        print("- line_transition_demo.gif")
        print("- scatter_transition_demo.gif")
        print("- bar_transition_demo.gif")
        print("- easing_comparison_demo.gif")
        print("- figure_state_transition_demo.gif")
        print("- complex_transition_demo.gif")
        print("- convenience_functions_demo.gif")
        print("\nThese animations demonstrate the smooth transitions functionality")
        print("working with various plot types and easing functions.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)