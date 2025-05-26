#!/usr/bin/env python3
"""
Visual demonstration of the dark mode toggle functionality.

This script creates plots and saves them as images to show the before/after
effect of the dark mode toggle.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt

# Add the lib directory to the path so we can import our dark_mode module
lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

import dark_mode as dm


def create_comprehensive_plot():
    """Create a comprehensive plot with various elements to showcase dark mode."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Dark Mode Toggle Demo - Comprehensive Plot', fontsize=16, fontweight='bold')
    
    # Plot 1: Line plot with multiple series
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.exp(-x/5)
    
    ax1.plot(x, y1, 'b-', label='sin(x)', linewidth=2)
    ax1.plot(x, y2, 'r--', label='cos(x)', linewidth=2)
    ax1.plot(x, y3, 'g:', label='damped sin(x)', linewidth=2)
    ax1.set_title('Multi-line Plot', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X values')
    ax1.set_ylabel('Y values')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Scatter plot with colormap
    np.random.seed(42)
    x_scatter = np.random.randn(200)
    y_scatter = np.random.randn(200)
    colors = np.random.rand(200)
    sizes = 1000 * np.random.rand(200)
    
    scatter = ax2.scatter(x_scatter, y_scatter, c=colors, s=sizes, alpha=0.6, cmap='viridis')
    ax2.set_title('Scatter Plot with Colormap', fontsize=12, fontweight='bold')
    ax2.set_xlabel('X values')
    ax2.set_ylabel('Y values')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax2)
    
    # Plot 3: Bar plot with error bars
    categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    values = [23, 45, 56, 78, 32]
    errors = [2, 3, 4, 1, 2]
    colors_bar = ['red', 'green', 'blue', 'orange', 'purple']
    
    bars = ax3.bar(categories, values, yerr=errors, color=colors_bar, alpha=0.7, capsize=5)
    ax3.set_title('Bar Plot with Error Bars', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Categories')
    ax3.set_ylabel('Values')
    ax3.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}', ha='center', va='bottom')
    
    # Plot 4: Histogram with multiple datasets
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(2, 1.5, 1000)
    
    ax4.hist(data1, bins=30, alpha=0.7, color='skyblue', label='Dataset 1', edgecolor='black')
    ax4.hist(data2, bins=30, alpha=0.7, color='lightcoral', label='Dataset 2', edgecolor='black')
    ax4.set_title('Overlapping Histograms', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    ax4.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def demo_basic_toggle():
    """Demonstrate basic dark mode toggle."""
    print("Creating basic toggle demonstration...")
    
    # Create a simple but comprehensive plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create data
    x = np.linspace(0, 4*np.pi, 200)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x/2)
    
    # Plot multiple lines
    ax.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    ax.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    ax.plot(x, y3, 'g:', linewidth=3, label='sin(x)cos(x/2)')
    
    # Customize the plot
    ax.set_title('Dark Mode Toggle Demo - Basic Plot', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values (radians)', fontsize=12)
    ax.set_ylabel('Y values', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add some annotations
    ax.annotate('Peak', xy=(np.pi/2, 1), xytext=(np.pi/2, 1.3),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=10, ha='center')
    
    # Save light mode version
    plt.savefig('demo_light_mode.png', dpi=150, bbox_inches='tight')
    print("✓ Saved light mode plot as 'demo_light_mode.png'")
    
    # Toggle to dark mode
    dm.toggle_dark_mode(fig=fig)
    
    # Save dark mode version
    plt.savefig('demo_dark_mode.png', dpi=150, bbox_inches='tight')
    print("✓ Saved dark mode plot as 'demo_dark_mode.png'")
    
    plt.close(fig)


def demo_comprehensive_plot():
    """Demonstrate dark mode on a comprehensive plot with multiple elements."""
    print("Creating comprehensive plot demonstration...")
    
    fig = create_comprehensive_plot()
    
    # Save light mode version
    plt.savefig('comprehensive_light_mode.png', dpi=150, bbox_inches='tight')
    print("✓ Saved comprehensive light mode plot as 'comprehensive_light_mode.png'")
    
    # Toggle to dark mode
    dm.toggle_dark_mode(fig=fig)
    
    # Save dark mode version
    plt.savefig('comprehensive_dark_mode.png', dpi=150, bbox_inches='tight')
    print("✓ Saved comprehensive dark mode plot as 'comprehensive_dark_mode.png'")
    
    plt.close(fig)


def demo_single_axis():
    """Demonstrate dark mode toggle on individual axes."""
    print("Creating single axis demonstration...")
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Single Axis Dark Mode Toggle Demo', fontsize=16, fontweight='bold')
    
    # Create identical plots on all three axes
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x) * np.exp(-x/4)
    
    for i, ax in enumerate([ax1, ax2, ax3]):
        ax.plot(x, y, 'b-', linewidth=2)
        ax.fill_between(x, 0, y, alpha=0.3, color='lightblue')
        ax.set_title(f'Axis {i+1}')
        ax.set_xlabel('X values')
        ax.set_ylabel('Y values')
        ax.grid(True, alpha=0.3)
    
    # Apply dark mode to only the middle axis
    dm.toggle_dark_mode(ax=ax2)
    
    # Update titles to reflect the mode
    ax1.set_title('Axis 1 (Light Mode)')
    ax2.set_title('Axis 2 (Dark Mode)')
    ax3.set_title('Axis 3 (Light Mode)')
    
    plt.tight_layout()
    plt.savefig('single_axis_demo.png', dpi=150, bbox_inches='tight')
    print("✓ Saved single axis demo as 'single_axis_demo.png'")
    
    plt.close(fig)


def demo_custom_colors():
    """Demonstrate custom dark mode color schemes."""
    print("Creating custom colors demonstration...")
    
    # Create three plots with different custom color schemes
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Custom Dark Mode Color Schemes', fontsize=16, fontweight='bold')
    
    # Create sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Plot 1: Default dark mode
    ax1.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    ax1.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    ax1.set_title('Default Dark Mode')
    ax1.legend()
    ax1.grid(True)
    dm.toggle_dark_mode(ax=ax1)
    
    # Plot 2: Blue theme
    ax2.plot(x, y1, 'cyan', linewidth=2, label='sin(x)')
    ax2.plot(x, y2, 'yellow', linewidth=2, label='cos(x)')
    ax2.set_title('Blue Theme')
    ax2.legend()
    ax2.grid(True)
    
    # Set custom blue theme
    dm.set_dark_mode_colors(
        background='#1a1a2e',
        text='#eee',
        grid='#16213e',
        spine='#0f3460',
        tick='#eee',
        label='#eee'
    )
    dm.toggle_dark_mode(ax=ax2)
    
    # Plot 3: Green theme
    ax3.plot(x, y1, 'lightgreen', linewidth=2, label='sin(x)')
    ax3.plot(x, y2, 'orange', linewidth=2, label='cos(x)')
    ax3.set_title('Green Theme')
    ax3.legend()
    ax3.grid(True)
    
    # Set custom green theme
    dm.set_dark_mode_colors(
        background='#0d1b2a',
        text='#a8dadc',
        grid='#457b9d',
        spine='#1d3557',
        tick='#a8dadc',
        label='#a8dadc'
    )
    dm.toggle_dark_mode(ax=ax3)
    
    # Reset to defaults for future use
    dm.set_dark_mode_colors()
    
    plt.tight_layout()
    plt.savefig('custom_colors_demo.png', dpi=150, bbox_inches='tight')
    print("✓ Saved custom colors demo as 'custom_colors_demo.png'")
    
    plt.close(fig)


def demo_data_color_adjustment():
    """Demonstrate data color adjustment feature."""
    print("Creating data color adjustment demonstration...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Data Color Adjustment Demo', fontsize=16, fontweight='bold')
    
    # Create plots with colors that would be hard to see in dark mode
    x = np.linspace(0, 10, 100)
    
    # Plot 1: Dark mode without data color adjustment
    ax1.plot(x, np.sin(x), 'black', linewidth=3, label='black line')
    ax1.plot(x, np.cos(x), 'darkblue', linewidth=3, label='dark blue line')
    ax1.plot(x, np.sin(x/2), 'darkgreen', linewidth=3, label='dark green line')
    ax1.scatter([2, 4, 6, 8], [0.5, -0.5, 0.8, -0.8], c=['black', 'darkred', 'darkblue', 'darkgreen'], s=100)
    ax1.set_title('Without Data Color Adjustment')
    ax1.legend()
    ax1.grid(True)
    dm.toggle_dark_mode(ax=ax1, adjust_data_colors=False)
    
    # Plot 2: Dark mode with data color adjustment
    ax2.plot(x, np.sin(x), 'black', linewidth=3, label='black line')
    ax2.plot(x, np.cos(x), 'darkblue', linewidth=3, label='dark blue line')
    ax2.plot(x, np.sin(x/2), 'darkgreen', linewidth=3, label='dark green line')
    ax2.scatter([2, 4, 6, 8], [0.5, -0.5, 0.8, -0.8], c=['black', 'darkred', 'darkblue', 'darkgreen'], s=100)
    ax2.set_title('With Data Color Adjustment')
    ax2.legend()
    ax2.grid(True)
    dm.toggle_dark_mode(ax=ax2, adjust_data_colors=True)
    
    plt.tight_layout()
    plt.savefig('data_color_adjustment_demo.png', dpi=150, bbox_inches='tight')
    print("✓ Saved data color adjustment demo as 'data_color_adjustment_demo.png'")
    
    plt.close(fig)


def main():
    """Run all visual demonstrations."""
    print("=== Matplotlib Dark Mode Toggle Visual Demo ===")
    print("This script will create several demonstration images showing")
    print("the dark mode toggle functionality in action.\n")
    
    try:
        demo_basic_toggle()
        demo_comprehensive_plot()
        demo_single_axis()
        demo_custom_colors()
        demo_data_color_adjustment()
        
        print("\n=== All Demonstrations Complete ===")
        print("Generated images:")
        print("- demo_light_mode.png / demo_dark_mode.png")
        print("- comprehensive_light_mode.png / comprehensive_dark_mode.png")
        print("- single_axis_demo.png")
        print("- custom_colors_demo.png")
        print("- data_color_adjustment_demo.png")
        print("\nThese images demonstrate the dark mode toggle functionality")
        print("working on various types of matplotlib plots.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)