import numpy as np
import matplotlib.pyplot as plt
from smooth_transitions import smooth_transition, transition_plot_state, EasingFunctions
import time

def demo_line_transition():
    """Demo smooth transition for line plots."""
    print("Demo: Line Plot Transition")
    
    # Generate data
    x = np.linspace(0, 10, 50)
    from_data = {
        'x': x,
        'y': np.sin(x),
        'color': 'blue',
        'linewidth': 2
    }
    
    to_data = {
        'x': x,
        'y': np.cos(x) * 2,
        'color': 'red',
        'linewidth': 5
    }
    
    # Create transition
    anim = smooth_transition(from_data, to_data, 
                           duration=3.0, fps=30, 
                           easing='ease_in_out_cubic',
                           plot_type='line')
    
    plt.title('Line Plot Smooth Transition')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return anim

def demo_scatter_transition():
    """Demo smooth transition for scatter plots."""
    print("Demo: Scatter Plot Transition")
    
    # Generate initial scattered data
    n_points = 30
    np.random.seed(42)
    
    from_data = {
        'x': np.random.normal(0, 1, n_points),
        'y': np.random.normal(0, 1, n_points),
        'colors': 'blue',
        'sizes': np.full(n_points, 50)
    }
    
    # Target: clustered data with different colors and sizes
    to_data = {
        'x': np.random.normal(3, 0.5, n_points),
        'y': np.random.normal(2, 0.5, n_points),
        'colors': 'orange',
        'sizes': np.full(n_points, 200)
    }
    
    # Create transition
    anim = smooth_transition(from_data, to_data, 
                           duration=2.5, fps=30, 
                           easing='ease_out_quad',
                           plot_type='scatter')
    
    plt.title('Scatter Plot Smooth Transition')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return anim

def demo_bar_transition():
    """Demo smooth transition for bar charts."""
    print("Demo: Bar Chart Transition")
    
    categories = ['A', 'B', 'C', 'D', 'E']
    x_pos = np.arange(len(categories))
    
    from_data = {
        'x': x_pos,
        'y': [10, 25, 30, 25, 20],
        'colors': 'skyblue',
        'width': 0.6
    }
    
    to_data = {
        'x': x_pos,
        'y': [35, 15, 40, 10, 45],
        'colors': 'lightcoral',
        'width': 0.6
    }
    
    # Create transition
    anim = smooth_transition(from_data, to_data, 
                           duration=2.0, fps=30, 
                           easing='ease_in_out_quad',
                           plot_type='bar')
    
    plt.title('Bar Chart Smooth Transition')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.xticks(x_pos, categories)
    plt.grid(True, alpha=0.3, axis='y')
    plt.show()
    
    return anim

def demo_easing_functions():
    """Demo different easing functions."""
    print("Demo: Different Easing Functions")
    
    # Create subplots for different easing functions
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    easing_types = ['linear', 'ease_in_quad', 'ease_out_quad', 
                   'ease_in_out_quad', 'ease_in_cubic', 'ease_out_cubic']
    
    x = np.linspace(0, 2*np.pi, 50)
    from_y = np.sin(x)
    to_y = np.cos(x) * 1.5
    
    animations = []
    
    for i, easing in enumerate(easing_types):
        plt.sca(axes[i])
        
        from_data = {'x': x, 'y': from_y, 'color': 'blue'}
        to_data = {'x': x, 'y': to_y, 'color': 'red'}
        
        # Note: This creates individual animations for each subplot
        # In practice, you might want to coordinate them
        anim = smooth_transition(from_data, to_data, 
                               duration=2.0, fps=30, 
                               easing=easing,
                               plot_type='line')
        
        axes[i].set_title(f'Easing: {easing}')
        axes[i].grid(True, alpha=0.3)
        animations.append(anim)
    
    plt.tight_layout()
    plt.show()
    
    return animations

def demo_figure_state_transition():
    """Demo transition between complete figure states."""
    print("Demo: Figure State Transition")
    
    # Create first figure
    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    x1 = np.linspace(0, 10, 100)
    y1 = np.exp(-x1/3) * np.sin(x1)
    ax1.plot(x1, y1, 'b-', linewidth=2)
    ax1.set_title('Exponential Decay Sine Wave')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)
    
    # Create second figure
    fig2 = plt.figure(figsize=(8, 6))
    ax2 = fig2.add_subplot(111)
    x2 = np.linspace(0, 10, 100)
    y2 = x2**2 * 0.1
    ax2.plot(x2, y2, 'r-', linewidth=3)
    ax2.set_title('Quadratic Growth')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.grid(True)
    
    # Create transition animation
    anim = transition_plot_state(fig1, fig2, duration=3.0, fps=30, 
                               easing='ease_in_out_cubic')
    
    plt.show()
    
    # Close the original figures
    plt.close(fig1)
    plt.close(fig2)
    
    return anim

def demo_complex_data_transition():
    """Demo complex data transition with multiple properties changing."""
    print("Demo: Complex Multi-Property Transition")
    
    # Create more complex transition with multiple changing properties
    t = np.linspace(0, 4*np.pi, 100)
    
    from_data = {
        'x': t,
        'y': np.sin(t) * np.exp(-t/10),
        'color': 'purple',
        'linewidth': 1
    }
    
    to_data = {
        'x': t,
        'y': np.cos(t/2) * np.sqrt(t),
        'color': 'orange',
        'linewidth': 4
    }
    
    anim = smooth_transition(from_data, to_data, 
                           duration=4.0, fps=30, 
                           easing='ease_in_out_cubic',
                           plot_type='line')
    
    plt.title('Complex Multi-Property Transition')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return anim

def run_all_demos():
    """Run all demonstration functions."""
    print("Starting Matplotlib Smooth Transitions Demo")
    print("=" * 50)
    
    demos = [
        demo_line_transition,
        demo_scatter_transition,
        demo_bar_transition,
        demo_complex_data_transition,
        demo_figure_state_transition
    ]
    
    animations = []
    
    for demo_func in demos:
        try:
            print(f"\nRunning {demo_func.__name__}...")
            anim = demo_func()
            animations.append(anim)
            print("Demo completed successfully!")
            
            # Add a small delay between demos
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in {demo_func.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print("All demos completed!")
    
    return animations

if __name__ == "__main__":
    # Run individual demos or all demos
    animations = run_all_demos()
    
    # Keep the script running to show animations
    print("\nAnimations are running. Close the plot windows to exit.")
    plt.show()