#!/usr/bin/env python3
"""
Simple example demonstrating the smooth transitions functionality.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import the transitions module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib'))
import transitions as mt


def create_line_transition_example():
    """Create a simple line transition example."""
    print("Creating line transition example...")
    
    # Create data
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x) * 2
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-2.5, 2.5)
    ax.set_title('Smooth Line Transition Example', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    
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
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('simple_line_transition.gif', writer=writer)
    print("✓ Saved simple line transition as 'simple_line_transition.gif'")
    
    plt.close(fig)


def create_scatter_transition_example():
    """Create a simple scatter transition example."""
    print("Creating scatter transition example...")
    
    # Create data - circle to star pattern
    n_points = 20
    
    # Circle
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    x1 = np.cos(theta)
    y1 = np.sin(theta)
    
    # Star pattern
    star_theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    star_r = np.where(np.arange(n_points) % 2 == 0, 1.5, 0.7)
    x2 = star_r * np.cos(star_theta)
    y2 = star_r * np.sin(star_theta)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title('Smooth Scatter Transition Example', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
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
        s=100,
        alpha=0.7
    )
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('simple_scatter_transition.gif', writer=writer)
    print("✓ Saved simple scatter transition as 'simple_scatter_transition.gif'")
    
    plt.close(fig)


def create_bar_transition_example():
    """Create a simple bar transition example."""
    print("Creating bar transition example...")
    
    # Create data
    categories = ['A', 'B', 'C', 'D', 'E']
    heights1 = np.array([2, 5, 3, 8, 1])
    heights2 = np.array([7, 2, 6, 1, 4])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_ylim(0, 9)
    ax.set_title('Smooth Bar Transition Example', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.grid(True, axis='y', alpha=0.3)
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
        color='green',
        alpha=0.8
    )
    
    # Save animation
    writer = animation.PillowWriter(fps=30)
    anim.save('simple_bar_transition.gif', writer=writer)
    print("✓ Saved simple bar transition as 'simple_bar_transition.gif'")
    
    plt.close(fig)


def create_convenience_functions_example():
    """Demonstrate convenience functions."""
    print("Creating convenience functions example...")
    
    # Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Convenience Functions Examples', fontsize=16, fontweight='bold')
    
    # Line transition using convenience function
    x = np.linspace(0, 2*np.pi, 50)
    y1 = np.sin(x)
    y2 = np.cos(x) * 1.5
    
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_ylim(-2, 2)
    ax1.set_title('transition_line_data')
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
    
    # Scatter transition using convenience function
    np.random.seed(42)
    x1_scatter = np.random.randn(20)
    y1_scatter = np.random.randn(20)
    x2_scatter = np.random.randn(20) * 2
    y2_scatter = np.random.randn(20) * 2
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_title('transition_scatter_data')
    ax2.grid(True, alpha=0.3)
    
    anim2 = mt.transition_scatter_data(
        ax=ax2,
        from_xy=(x1_scatter, y1_scatter),
        to_xy=(x2_scatter, y2_scatter),
        duration=2.0,
        fps=30,
        color='red',
        s=50,
        alpha=0.7
    )
    
    # Bar transition using convenience function
    heights1 = np.array([3, 7, 2, 5])
    heights2 = np.array([6, 1, 8, 3])
    
    ax3.set_ylim(0, 9)
    ax3.set_title('transition_bar_heights')
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
    anim1.save('convenience_functions_example.gif', writer=writer)
    print("✓ Saved convenience functions example as 'convenience_functions_example.gif'")
    
    plt.close(fig)


def main():
    """Run all examples."""
    print("=== Simple Matplotlib Transitions Examples ===")
    print("Creating visual examples of the smooth transitions functionality...\n")
    
    try:
        create_line_transition_example()
        create_scatter_transition_example()
        create_bar_transition_example()
        create_convenience_functions_example()
        
        print("\n=== Examples Complete ===")
        print("Generated animations:")
        print("- simple_line_transition.gif")
        print("- simple_scatter_transition.gif")
        print("- simple_bar_transition.gif")
        print("- convenience_functions_example.gif")
        print("\nThese demonstrate the core functionality of the transitions module.")
        
    except Exception as e:
        print(f"\nError during example creation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)