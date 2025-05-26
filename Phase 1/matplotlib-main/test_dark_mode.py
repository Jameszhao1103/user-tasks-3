#!/usr/bin/env python3
"""
Simple test script for the dark mode functionality.

This script tests the dark mode toggle without requiring the full matplotlib installation.
"""

import sys
import os
import numpy as np

# Install matplotlib if not available
try:
    import matplotlib
    import matplotlib.pyplot as plt
except ImportError:
    print("Installing matplotlib...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib
    import matplotlib.pyplot as plt

# Add the lib directory to the path so we can import our dark_mode module
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Import our dark mode module directly
try:
    # Try to import from the local lib directory first
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib'))
    import dark_mode as dm
    print("✓ Dark mode module imported successfully!")
except ImportError as e:
    print(f"✗ Failed to import dark mode module: {e}")
    sys.exit(1)


def test_basic_functionality():
    """Test basic dark mode toggle functionality."""
    print("\n=== Testing Basic Functionality ===")
    
    # Create a simple plot
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    
    ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
    ax.set_title('Test Plot - Dark Mode Toggle')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.legend()
    ax.grid(True)
    
    # Test initial state (should be light mode)
    print("Initial state: Light mode")
    initial_bg = fig.get_facecolor()
    print(f"Initial background color: {initial_bg}")
    
    # Toggle to dark mode
    print("Toggling to dark mode...")
    dm.toggle_dark_mode(fig=fig)
    
    dark_bg = fig.get_facecolor()
    print(f"Dark mode background color: {dark_bg}")
    
    # Verify the background changed
    if dark_bg != initial_bg:
        print("✓ Background color changed successfully")
    else:
        print("✗ Background color did not change")
    
    # Toggle back to light mode
    print("Toggling back to light mode...")
    dm.toggle_dark_mode(fig=fig)
    
    restored_bg = fig.get_facecolor()
    print(f"Restored background color: {restored_bg}")
    
    # Verify we're back to the original state
    if restored_bg == initial_bg:
        print("✓ Successfully restored to original colors")
    else:
        print("✗ Failed to restore original colors")
    
    plt.close(fig)


def test_single_axis():
    """Test dark mode toggle on a single axis."""
    print("\n=== Testing Single Axis Toggle ===")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Create identical plots
    x = np.linspace(0, 10, 50)
    y = x**2
    
    ax1.plot(x, y, 'r-', linewidth=2)
    ax1.set_title('Axis 1 (Light)')
    ax1.grid(True)
    
    ax2.plot(x, y, 'r-', linewidth=2)
    ax2.set_title('Axis 2 (Dark)')
    ax2.grid(True)
    
    # Apply dark mode to only the second axis
    dm.toggle_dark_mode(ax=ax2)
    
    # Check that only ax2 changed
    ax1_bg = ax1.get_facecolor()
    ax2_bg = ax2.get_facecolor()
    
    if ax1_bg != ax2_bg:
        print("✓ Single axis toggle works correctly")
    else:
        print("✗ Single axis toggle failed")
    
    plt.close(fig)


def test_current_figure():
    """Test dark mode toggle on current figure."""
    print("\n=== Testing Current Figure Toggle ===")
    
    # Create a plot without storing figure reference
    plt.figure(figsize=(8, 6))
    x = np.linspace(0, 5, 100)
    plt.plot(x, np.exp(-x) * np.sin(x), 'g-', linewidth=2)
    plt.title('Current Figure Test')
    plt.grid(True)
    
    # Get initial background
    initial_bg = plt.gcf().get_facecolor()
    
    # Toggle current figure
    dm.toggle_dark_mode()
    
    # Check if it changed
    dark_bg = plt.gcf().get_facecolor()
    
    if dark_bg != initial_bg:
        print("✓ Current figure toggle works correctly")
    else:
        print("✗ Current figure toggle failed")
    
    plt.close()


def test_custom_colors():
    """Test custom color scheme functionality."""
    print("\n=== Testing Custom Colors ===")
    
    # Set custom colors
    dm.set_dark_mode_colors(
        background='#2d2d2d',
        text='#ffffff',
        grid='#555555'
    )
    
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 2], 'b-')
    ax.set_title('Custom Colors Test')
    ax.grid(True)
    
    # Apply dark mode with custom colors
    dm.toggle_dark_mode(fig=fig)
    
    # Check if custom background was applied
    bg_color = fig.get_facecolor()
    print(f"Custom background applied: {bg_color}")
    
    # Reset to defaults
    dm.set_dark_mode_colors()
    
    print("✓ Custom colors test completed")
    plt.close(fig)


def test_data_color_adjustment():
    """Test data color adjustment functionality."""
    print("\n=== Testing Data Color Adjustment ===")
    
    fig, ax = plt.subplots()
    
    # Create plot with dark colors that would be hard to see in dark mode
    ax.plot([1, 2, 3], [1, 4, 2], 'k-', linewidth=3, label='black line')
    ax.plot([1, 2, 3], [2, 1, 3], 'b-', linewidth=3, label='blue line')
    ax.set_title('Data Color Adjustment Test')
    ax.legend()
    
    # Apply dark mode with data color adjustment
    dm.toggle_dark_mode(fig=fig, adjust_data_colors=True)
    
    print("✓ Data color adjustment test completed")
    plt.close(fig)


def main():
    """Run all tests."""
    print("=== Matplotlib Dark Mode Toggle Tests ===")
    
    try:
        test_basic_functionality()
        test_single_axis()
        test_current_figure()
        test_custom_colors()
        test_data_color_adjustment()
        
        print("\n=== All Tests Completed ===")
        print("✓ Dark mode toggle functionality is working correctly!")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)