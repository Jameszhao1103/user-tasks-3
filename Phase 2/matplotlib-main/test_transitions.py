#!/usr/bin/env python3
"""
Test script for the matplotlib transitions functionality.

This script tests the core functionality of the transitions module
without requiring visual output.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt

# Add the lib directory to the path so we can import our transitions module
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

try:
    # Import the transitions module directly
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'matplotlib'))
    import transitions as mt
    print("✓ Transitions module imported successfully!")
except ImportError as e:
    print(f"✗ Failed to import transitions module: {e}")
    sys.exit(1)


def test_easing_functions():
    """Test all easing functions."""
    print("\n=== Testing Easing Functions ===")
    
    easing_functions = [
        'linear', 'ease_in_quad', 'ease_out_quad', 'ease_in_out_quad',
        'ease_in_cubic', 'ease_out_cubic', 'ease_in_out_cubic',
        'ease_in_sine', 'ease_out_sine', 'ease_in_out_sine'
    ]
    
    for easing in easing_functions:
        try:
            func = getattr(mt.EasingFunctions, easing)
            # Test with various input values
            test_values = [0.0, 0.25, 0.5, 0.75, 1.0]
            results = [func(t) for t in test_values]
            
            # Basic sanity checks
            assert 0.0 <= results[0] <= 0.1, f"{easing}: f(0) should be close to 0"
            assert 0.9 <= results[-1] <= 1.0, f"{easing}: f(1) should be close to 1"
            
            print(f"✓ {easing}: {results}")
            
        except Exception as e:
            print(f"✗ {easing}: {e}")
            return False
    
    return True


def test_interpolation():
    """Test value interpolation functions."""
    print("\n=== Testing Interpolation Functions ===")
    
    # Test numeric interpolation
    result = mt.interpolate_values(0, 10, 0.5)
    assert result == 5.0, f"Expected 5.0, got {result}"
    print("✓ Numeric interpolation works")
    
    # Test array interpolation
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    result = mt.interpolate_values(arr1, arr2, 0.5)
    expected = np.array([2.5, 3.5, 4.5])
    assert np.allclose(result, expected), f"Expected {expected}, got {result}"
    print("✓ Array interpolation works")
    
    # Test list interpolation
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    result = mt.interpolate_values(list1, list2, 0.5)
    expected = [2.5, 3.5, 4.5]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ List interpolation works")
    
    # Test color interpolation
    try:
        result = mt.interpolate_values('red', 'blue', 0.5)
        print(f"✓ Color interpolation works: {result}")
    except Exception as e:
        print(f"✗ Color interpolation failed: {e}")
        return False
    
    return True


def test_data_normalization():
    """Test data normalization functions."""
    print("\n=== Testing Data Normalization ===")
    
    # Test line plot normalization
    y_data = [1, 2, 3, 4, 5]
    result = mt._normalize_data(y_data, 'line')
    expected_keys = {'y'}
    assert set(result.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(result.keys())}"
    assert np.array_equal(result['y'], np.array(y_data)), "Y data should match input"
    print("✓ Line plot data normalization works")
    
    # Test scatter plot normalization
    scatter_data = ([1, 2, 3], [4, 5, 6])
    result = mt._normalize_data(scatter_data, 'scatter')
    expected_keys = {'x', 'y'}
    assert set(result.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(result.keys())}"
    print("✓ Scatter plot data normalization works")
    
    # Test bar plot normalization
    bar_data = [1, 2, 3, 4]
    result = mt._normalize_data(bar_data, 'bar')
    expected_keys = {'heights'}
    assert set(result.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(result.keys())}"
    print("✓ Bar plot data normalization works")
    
    # Test dictionary input (should pass through)
    dict_data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
    result = mt._normalize_data(dict_data, 'scatter')
    assert result == dict_data, "Dictionary data should pass through unchanged"
    print("✓ Dictionary data normalization works")
    
    return True


def test_smooth_transition_creation():
    """Test creation of smooth transition animations."""
    print("\n=== Testing Smooth Transition Creation ===")
    
    # Create test figure and axis
    fig, ax = plt.subplots()
    
    # Test line transition
    try:
        y1 = np.array([1, 2, 3, 4, 5])
        y2 = np.array([5, 4, 3, 2, 1])
        
        anim = mt.smooth_transition(
            from_data={'y': y1},
            to_data={'y': y2},
            duration=1.0,
            fps=10,  # Low fps for faster testing
            ax=ax,
            plot_type='line'
        )
        
        assert anim is not None, "Animation object should be created"
        print("✓ Line transition animation created successfully")
        
    except Exception as e:
        print(f"✗ Line transition creation failed: {e}")
        plt.close(fig)
        return False
    
    # Test scatter transition
    try:
        x1, y1 = np.array([1, 2, 3]), np.array([1, 2, 3])
        x2, y2 = np.array([3, 2, 1]), np.array([3, 2, 1])
        
        anim = mt.smooth_transition(
            from_data={'x': x1, 'y': y1},
            to_data={'x': x2, 'y': y2},
            duration=1.0,
            fps=10,
            ax=ax,
            plot_type='scatter'
        )
        
        assert anim is not None, "Animation object should be created"
        print("✓ Scatter transition animation created successfully")
        
    except Exception as e:
        print(f"✗ Scatter transition creation failed: {e}")
        plt.close(fig)
        return False
    
    # Test bar transition
    try:
        heights1 = np.array([1, 2, 3])
        heights2 = np.array([3, 2, 1])
        
        anim = mt.smooth_transition(
            from_data={'heights': heights1},
            to_data={'heights': heights2},
            duration=1.0,
            fps=10,
            ax=ax,
            plot_type='bar'
        )
        
        assert anim is not None, "Animation object should be created"
        print("✓ Bar transition animation created successfully")
        
    except Exception as e:
        print(f"✗ Bar transition creation failed: {e}")
        plt.close(fig)
        return False
    
    plt.close(fig)
    return True


def test_convenience_functions():
    """Test convenience functions."""
    print("\n=== Testing Convenience Functions ===")
    
    fig, ax = plt.subplots()
    
    # Test transition_line_data
    try:
        y1 = np.array([1, 2, 3, 4, 5])
        y2 = np.array([5, 4, 3, 2, 1])
        
        anim = mt.transition_line_data(ax, y1, y2, duration=1.0, fps=10)
        assert anim is not None, "Line data transition should create animation"
        print("✓ transition_line_data works")
        
    except Exception as e:
        print(f"✗ transition_line_data failed: {e}")
        plt.close(fig)
        return False
    
    # Test transition_scatter_data
    try:
        xy1 = (np.array([1, 2, 3]), np.array([1, 2, 3]))
        xy2 = (np.array([3, 2, 1]), np.array([3, 2, 1]))
        
        anim = mt.transition_scatter_data(ax, xy1, xy2, duration=1.0, fps=10)
        assert anim is not None, "Scatter data transition should create animation"
        print("✓ transition_scatter_data works")
        
    except Exception as e:
        print(f"✗ transition_scatter_data failed: {e}")
        plt.close(fig)
        return False
    
    # Test transition_bar_heights
    try:
        heights1 = np.array([1, 2, 3])
        heights2 = np.array([3, 2, 1])
        
        anim = mt.transition_bar_heights(ax, heights1, heights2, duration=1.0, fps=10)
        assert anim is not None, "Bar heights transition should create animation"
        print("✓ transition_bar_heights works")
        
    except Exception as e:
        print(f"✗ transition_bar_heights failed: {e}")
        plt.close(fig)
        return False
    
    plt.close(fig)
    return True


def test_figure_state_extraction():
    """Test figure state extraction."""
    print("\n=== Testing Figure State Extraction ===")
    
    # Create a test figure with various elements
    fig, ax = plt.subplots()
    
    # Add line
    x = np.linspace(0, 10, 20)
    y = np.sin(x)
    ax.plot(x, y, 'b-', linewidth=2)
    
    # Add scatter
    ax.scatter([1, 2, 3], [1, 2, 3], c='red', s=50)
    
    # Add bar
    ax.bar([5, 6, 7], [1, 2, 3], color='green')
    
    # Set properties
    ax.set_title('Test Plot')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.grid(True)
    
    try:
        state = mt._extract_figure_state(fig)
        
        # Check that state has expected structure
        assert 'axes' in state, "State should contain 'axes'"
        assert 'figure_props' in state, "State should contain 'figure_props'"
        assert len(state['axes']) > 0, "Should have at least one axis"
        
        ax_state = state['axes'][0]
        assert 'lines' in ax_state, "Axis state should contain 'lines'"
        assert 'collections' in ax_state, "Axis state should contain 'collections'"
        assert 'patches' in ax_state, "Axis state should contain 'patches'"
        assert 'title' in ax_state, "Axis state should contain 'title'"
        
        print("✓ Figure state extraction works")
        print(f"  - Found {len(ax_state['lines'])} lines")
        print(f"  - Found {len(ax_state['collections'])} collections")
        print(f"  - Found {len(ax_state['patches'])} patches")
        
    except Exception as e:
        print(f"✗ Figure state extraction failed: {e}")
        plt.close(fig)
        return False
    
    plt.close(fig)
    return True


def test_figure_transition():
    """Test figure state transition."""
    print("\n=== Testing Figure State Transition ===")
    
    # Create two simple figures
    fig1, ax1 = plt.subplots()
    x = np.linspace(0, 10, 20)
    ax1.plot(x, np.sin(x), 'b-')
    ax1.set_title('Figure 1')
    
    fig2, ax2 = plt.subplots()
    ax2.plot(x, np.cos(x), 'r-')
    ax2.set_title('Figure 2')
    
    try:
        anim = mt.transition_plot_state(
            fig_from=fig1,
            fig_to=fig2,
            duration=1.0,
            fps=10
        )
        
        assert anim is not None, "Figure transition should create animation"
        print("✓ Figure state transition works")
        
    except Exception as e:
        print(f"✗ Figure state transition failed: {e}")
        return False
    finally:
        plt.close(fig1)
        plt.close(fig2)
        if 'anim' in locals():
            plt.close(anim._fig)
    
    return True


def main():
    """Run all tests."""
    print("=== Matplotlib Transitions Module Tests ===")
    
    tests = [
        test_easing_functions,
        test_interpolation,
        test_data_normalization,
        test_smooth_transition_creation,
        test_convenience_functions,
        test_figure_state_extraction,
        test_figure_transition
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
            failed += 1
    
    print(f"\n=== Test Results ===")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Transitions functionality is working correctly.")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)