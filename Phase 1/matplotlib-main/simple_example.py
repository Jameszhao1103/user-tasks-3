#!/usr/bin/env python3
"""
Simple example demonstrating the dark mode toggle functionality.

This script creates a basic plot and shows how to toggle between light and dark modes.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the lib directory to the path so we can import our dark_mode module
lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

import dark_mode as dm


def main():
    """Create a simple plot and demonstrate dark mode toggle."""
    
    print("=== Simple Dark Mode Toggle Example ===")
    print("This example shows how to use the dark mode toggle functionality.\n")
    
    # Create sample data
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Add multiple elements to showcase the functionality
    line1 = ax.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    line2 = ax.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    
    # Customize the plot
    ax.set_title('Dark Mode Toggle Example', fontsize=16, fontweight='bold')
    ax.set_xlabel('X values (radians)', fontsize=12)
    ax.set_ylabel('Y values', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add an annotation
    ax.annotate('Maximum', xy=(np.pi/2, 1), xytext=(np.pi/2, 1.3),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=10, ha='center')
    
    print("1. Created plot in LIGHT mode")
    
    # Save the light mode version
    plt.savefig('example_light.png', dpi=150, bbox_inches='tight')
    print("   Saved as 'example_light.png'")
    
    # Toggle to dark mode
    print("\n2. Toggling to DARK mode...")
    dm.toggle_dark_mode(fig=fig)
    
    # Save the dark mode version
    plt.savefig('example_dark.png', dpi=150, bbox_inches='tight')
    print("   Saved as 'example_dark.png'")
    
    # Toggle back to light mode
    print("\n3. Toggling back to LIGHT mode...")
    dm.toggle_dark_mode(fig=fig)
    
    # Save the restored light mode version
    plt.savefig('example_restored.png', dpi=150, bbox_inches='tight')
    print("   Saved as 'example_restored.png'")
    
    print("\n=== Example Complete ===")
    print("Generated files:")
    print("- example_light.png (original light mode)")
    print("- example_dark.png (toggled to dark mode)")
    print("- example_restored.png (toggled back to light mode)")
    print("\nUsage summary:")
    print("  import matplotlib.dark_mode as dm")
    print("  dm.toggle_dark_mode(fig=fig)  # Toggle entire figure")
    print("  dm.toggle_dark_mode(ax=ax)   # Toggle single axis")
    print("  dm.toggle_dark_mode()        # Toggle current figure")
    
    plt.close(fig)


if __name__ == "__main__":
    main()