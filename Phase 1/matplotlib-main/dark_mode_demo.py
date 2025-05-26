#!/usr/bin/env python3
"""
Dark Mode Toggle Demo for Matplotlib

This script demonstrates the dark mode toggle functionality for matplotlib plots.
It shows various plot types and how they look in both light and dark modes.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the lib directory to the path so we can import our dark_mode module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import matplotlib.dark_mode as dm


def create_sample_plots():
    """Create a variety of sample plots to demonstrate dark mode functionality."""
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Dark Mode Toggle Demo - Various Plot Types', fontsize=16)
    
    # Plot 1: Line plot
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    ax1.plot(x, y1, 'b-', label='sin(x)', linewidth=2)
    ax1.plot(x, y2, 'r--', label='cos(x)', linewidth=2)
    ax1.set_title('Line Plot')
    ax1.set_xlabel('X values')
    ax1.set_ylabel('Y values')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(100)
    y_scatter = np.random.randn(100)
    colors = np.random.rand(100)
    ax2.scatter(x_scatter, y_scatter, c=colors, alpha=0.7, s=50)
    ax2.set_title('Scatter Plot')
    ax2.set_xlabel('X values')
    ax2.set_ylabel('Y values')
    ax2.grid(True)
    
    # Plot 3: Bar plot
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]
    bars = ax3.bar(categories, values, color=['red', 'green', 'blue', 'orange', 'purple'])
    ax3.set_title('Bar Plot')
    ax3.set_xlabel('Categories')
    ax3.set_ylabel('Values')
    ax3.grid(True, axis='y')
    
    # Plot 4: Histogram
    data = np.random.normal(0, 1, 1000)
    ax4.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax4.set_title('Histogram')
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, axis='y')
    
    plt.tight_layout()
    return fig


def demo_single_axis_toggle():
    """Demonstrate toggling dark mode on a single axis."""
    print("\n=== Single Axis Toggle Demo ===")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Single Axis Dark Mode Toggle', fontsize=14)
    
    # Create identical plots on both axes
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_title('Light Mode (Original)')
    ax1.set_xlabel('X values')
    ax1.set_ylabel('sin(x)')
    ax1.grid(True)
    
    ax2.plot(x, y, 'b-', linewidth=2)
    ax2.set_title('Dark Mode')
    ax2.set_xlabel('X values')
    ax2.set_ylabel('sin(x)')
    ax2.grid(True)
    
    # Apply dark mode to only the second axis
    dm.toggle_dark_mode(ax=ax2)
    
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue...")


def demo_full_figure_toggle():
    """Demonstrate toggling dark mode on entire figures."""
    print("\n=== Full Figure Toggle Demo ===")
    
    # Create the sample plots
    fig = create_sample_plots()
    
    print("Showing plot in LIGHT mode...")
    plt.show(block=False)
    plt.pause(0.1)  # Allow the plot to render
    
    input("Press Enter to toggle to DARK mode...")
    
    # Toggle to dark mode
    dm.toggle_dark_mode(fig=fig)
    plt.draw()
    
    print("Now showing plot in DARK mode...")
    input("Press Enter to toggle back to LIGHT mode...")
    
    # Toggle back to light mode
    dm.toggle_dark_mode(fig=fig)
    plt.draw()
    
    print("Back to LIGHT mode!")
    input("Press Enter to toggle to DARK mode with adjusted data colors...")
    
    # Toggle to dark mode with data color adjustment
    dm.toggle_dark_mode(fig=fig, adjust_data_colors=True)
    plt.draw()
    
    print("DARK mode with adjusted data colors!")
    input("Press Enter to close...")
    
    plt.close(fig)


def demo_custom_colors():
    """Demonstrate custom dark mode color schemes."""
    print("\n=== Custom Color Scheme Demo ===")
    
    # Create a simple plot
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), 'b-', label='Original colors', linewidth=2)
    ax.set_title('Custom Dark Mode Colors')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.legend()
    ax.grid(True)
    
    plt.show(block=False)
    plt.pause(0.1)
    
    input("Press Enter to apply custom dark mode colors...")
    
    # Set custom dark mode colors
    dm.set_dark_mode_colors(
        background='#1a1a2e',  # Dark blue background
        text='#16213e',        # Darker blue text
        grid='#0f3460',        # Blue grid
        spine='#e94560',       # Red spines
        tick='#f5f5f5',        # Light tick marks
        label='#f5f5f5'        # Light labels
    )
    
    # Apply the custom dark mode
    dm.toggle_dark_mode(fig=fig)
    plt.draw()
    
    print("Custom dark mode applied!")
    input("Press Enter to close...")
    
    plt.close(fig)
    
    # Reset to default colors for future demos
    dm.set_dark_mode_colors()


def demo_current_figure():
    """Demonstrate toggling dark mode on the current figure."""
    print("\n=== Current Figure Toggle Demo ===")
    
    # Create a plot without explicitly storing the figure reference
    plt.figure(figsize=(10, 6))
    x = np.linspace(0, 4*np.pi, 200)
    plt.plot(x, np.sin(x), 'g-', label='sin(x)', linewidth=2)
    plt.plot(x, np.cos(x), 'm--', label='cos(x)', linewidth=2)
    plt.title('Current Figure Dark Mode Toggle')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.legend()
    plt.grid(True)
    
    plt.show(block=False)
    plt.pause(0.1)
    
    input("Press Enter to toggle current figure to dark mode...")
    
    # Toggle dark mode on current figure (no fig or ax parameter)
    dm.toggle_dark_mode()
    plt.draw()
    
    print("Current figure toggled to dark mode!")
    input("Press Enter to toggle back...")
    
    # Toggle back
    dm.toggle_dark_mode()
    plt.draw()
    
    print("Back to light mode!")
    input("Press Enter to close...")
    
    plt.close()


def main():
    """Run all demo functions."""
    print("=== Matplotlib Dark Mode Toggle Demo ===")
    print("This demo will show various matplotlib plots and demonstrate")
    print("the dark mode toggle functionality.")
    print("\nNote: Close any plot windows that appear to continue with the demo.")
    
    try:
        # Run all demos
        demo_single_axis_toggle()
        demo_full_figure_toggle()
        demo_custom_colors()
        demo_current_figure()
        
        print("\n=== Demo Complete ===")
        print("The dark mode toggle functionality supports:")
        print("- Toggling individual axes: dm.toggle_dark_mode(ax=ax)")
        print("- Toggling entire figures: dm.toggle_dark_mode(fig=fig)")
        print("- Toggling current figure: dm.toggle_dark_mode()")
        print("- Adjusting data colors: dm.toggle_dark_mode(adjust_data_colors=True)")
        print("- Custom color schemes: dm.set_dark_mode_colors(...)")
        print("- Reversible toggling (call again to switch back)")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()