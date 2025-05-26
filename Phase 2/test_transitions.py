import unittest
import numpy as np
import matplotlib.pyplot as plt
from smooth_transitions import (
    smooth_transition, 
    transition_plot_state, 
    EasingFunctions,
    interpolate_values,
    interpolate_colors
)

class TestSmoothTransitions(unittest.TestCase):
    
    def test_easing_functions(self):
        """Test that easing functions return expected values."""
        # Test linear function
        self.assertAlmostEqual(EasingFunctions.linear(0.5), 0.5)
        self.assertAlmostEqual(EasingFunctions.linear(0), 0)
        self.assertAlmostEqual(EasingFunctions.linear(1), 1)
        
        # Test ease_in_quad
        self.assertAlmostEqual(EasingFunctions.ease_in_quad(0.5), 0.25)
        
        # Test ease_out_quad
        self.assertAlmostEqual(EasingFunctions.ease_out_quad(0.5), 0.75)
    
    def test_interpolate_values(self):
        """Test value interpolation."""
        # Test scalar interpolation
        result = interpolate_values(0, 10, 0.5)
        self.assertAlmostEqual(result, 5.0)
        
        # Test array interpolation
        from_arr = np.array([0, 0, 0])
        to_arr = np.array([10, 20, 30])
        result = interpolate_values(from_arr, to_arr, 0.5)
        expected = np.array([5, 10, 15])
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_interpolate_colors(self):
        """Test color interpolation."""
        from_color = 'red'
        to_color = 'blue'
        result = interpolate_colors(from_color, to_color, 0.5)
        
        # Should return a tuple of 4 values (RGBA)
        self.assertEqual(len(result), 4)
        self.assertTrue(all(0 <= val <= 1 for val in result))
    
    def test_smooth_transition_creation(self):
        """Test that smooth_transition creates animation without errors."""
        from_data = {
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'color': 'blue'
        }
        
        to_data = {
            'x': [1, 2, 3],
            'y': [3, 2, 1],
            'color': 'red'
        }
        
        # Should not raise an exception
        anim = smooth_transition(from_data, to_data, duration=1.0, fps=10, plot_type='line')
        self.assertIsNotNone(anim)
        
        # Clean up
        plt.close('all')
    
    def test_different_plot_types(self):
        """Test different plot types work."""
        data_from = {'x': [1, 2, 3], 'y': [1, 2, 3]}
        data_to = {'x': [1, 2, 3], 'y': [3, 2, 1]}
        
        plot_types = ['line', 'scatter', 'bar']
        
        for plot_type in plot_types:
            with self.subTest(plot_type=plot_type):
                anim = smooth_transition(data_from, data_to, 
                                       duration=0.5, fps=5, 
                                       plot_type=plot_type)
                self.assertIsNotNone(anim)
        
        plt.close('all')
    
    def test_transition_plot_state(self):
        """Test figure state transition."""
        # Create two simple figures
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot([1, 2, 3], [1, 2, 3])
        
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot([1, 2, 3], [3, 2, 1])
        
        # Should not raise an exception
        anim = transition_plot_state(fig1, fig2, duration=0.5, fps=5)
        self.assertIsNotNone(anim)
        
        # Clean up
        plt.close('all')

if __name__ == '__main__':
    unittest.main()