#!/usr/bin/env python3
"""
Create static before/after images to demonstrate the transitions functionality.
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt

def create_line_before_after():
    """Create before/after images for line transition."""
    print("Creating line transition before/after images...")
    
    # Create data
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x) * 2
    
    # Before image
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y1, 'blue', linewidth=2, label='Initial State')
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-2.5, 2.5)
    ax.set_title('Line Transition - Before', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig('line_transition_before.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # After image
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y2, 'blue', linewidth=2, label='Final State')
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-2.5, 2.5)
    ax.set_title('Line Transition - After', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig('line_transition_after.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ Created line_transition_before.png and line_transition_after.png")


def create_scatter_before_after():
    """Create before/after images for scatter transition."""
    print("Creating scatter transition before/after images...")
    
    # Create data - circle to star pattern
    n_points = 20
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    
    # Circle
    x1 = np.cos(theta)
    y1 = np.sin(theta)
    
    # Star pattern
    star_r = np.where(np.arange(n_points) % 2 == 0, 1.5, 0.7)
    x2 = star_r * np.cos(theta)
    y2 = star_r * np.sin(theta)
    
    # Before image
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x1, y1, color='red', s=100, alpha=0.7, label='Initial State')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title('Scatter Transition - Before (Circle)', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    plt.tight_layout()
    plt.savefig('scatter_transition_before.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # After image
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(x2, y2, color='red', s=100, alpha=0.7, label='Final State')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title('Scatter Transition - After (Star)', fontsize=14, fontweight='bold')
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    plt.tight_layout()
    plt.savefig('scatter_transition_after.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ Created scatter_transition_before.png and scatter_transition_after.png")


def create_bar_before_after():
    """Create before/after images for bar transition."""
    print("Creating bar transition before/after images...")
    
    # Create data
    categories = ['A', 'B', 'C', 'D', 'E']
    heights1 = np.array([2, 5, 3, 8, 1])
    heights2 = np.array([7, 2, 6, 1, 4])
    
    # Before image
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, heights1, color='green', alpha=0.8, label='Initial State')
    ax.set_ylim(0, 9)
    ax.set_title('Bar Transition - Before', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend()
    
    # Add value labels on bars
    for bar, height in zip(bars, heights1):
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                str(height), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('bar_transition_before.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # After image
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, heights2, color='green', alpha=0.8, label='Final State')
    ax.set_ylim(0, 9)
    ax.set_title('Bar Transition - After', fontsize=14, fontweight='bold')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend()
    
    # Add value labels on bars
    for bar, height in zip(bars, heights2):
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                str(height), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('bar_transition_after.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ Created bar_transition_before.png and bar_transition_after.png")


def create_easing_comparison():
    """Create a comparison of different easing functions."""
    print("Creating easing functions comparison...")
    
    # Create time array
    t = np.linspace(0, 1, 100)
    
    # Define easing functions (simplified versions for visualization)
    def linear(t): return t
    def ease_in_quad(t): return t * t
    def ease_out_quad(t): return 1 - (1 - t) * (1 - t)
    def ease_in_out_quad(t): 
        return np.where(t < 0.5, 2 * t * t, 1 - np.power(-2 * t + 2, 2) / 2)
    def ease_in_cubic(t): return t * t * t
    def ease_out_cubic(t): return 1 - np.power(1 - t, 3)
    
    easing_funcs = [
        ('Linear', linear),
        ('Ease In Quad', ease_in_quad),
        ('Ease Out Quad', ease_out_quad),
        ('Ease In-Out Quad', ease_in_out_quad),
        ('Ease In Cubic', ease_in_cubic),
        ('Ease Out Cubic', ease_out_cubic)
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Easing Functions Comparison', fontsize=16, fontweight='bold')
    axes = axes.flatten()
    
    for i, (name, func) in enumerate(easing_funcs):
        ax = axes[i]
        y = func(t)
        ax.plot(t, y, 'blue', linewidth=2)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (0 to 1)')
        ax.set_ylabel('Progress (0 to 1)')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('easing_functions_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ Created easing_functions_comparison.png")


def create_overview_diagram():
    """Create an overview diagram showing the transitions concept."""
    print("Creating transitions overview diagram...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Matplotlib Smooth Transitions Overview', fontsize=16, fontweight='bold')
    
    # Line transition example
    x = np.linspace(0, 2*np.pi, 50)
    y1 = np.sin(x)
    y2 = np.cos(x) * 1.5
    
    ax1.plot(x, y1, 'blue', linewidth=2, alpha=0.7, label='From')
    ax1.plot(x, y2, 'red', linewidth=2, alpha=0.7, label='To')
    ax1.set_title('Line Data Transition', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Scatter transition example
    np.random.seed(42)
    n = 20
    x1 = np.random.randn(n)
    y1 = np.random.randn(n)
    x2 = np.random.randn(n) * 2
    y2 = np.random.randn(n) * 2
    
    ax2.scatter(x1, y1, color='blue', alpha=0.7, s=50, label='From')
    ax2.scatter(x2, y2, color='red', alpha=0.7, s=50, label='To')
    ax2.set_title('Scatter Data Transition', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Bar transition example
    categories = ['A', 'B', 'C', 'D']
    heights1 = [3, 7, 2, 5]
    heights2 = [6, 1, 8, 3]
    
    x_pos = np.arange(len(categories))
    width = 0.35
    
    ax3.bar(x_pos - width/2, heights1, width, color='blue', alpha=0.7, label='From')
    ax3.bar(x_pos + width/2, heights2, width, color='red', alpha=0.7, label='To')
    ax3.set_title('Bar Heights Transition', fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(categories)
    ax3.legend()
    ax3.grid(True, axis='y', alpha=0.3)
    
    # Features overview
    ax4.text(0.5, 0.9, 'Key Features:', ha='center', va='top', fontsize=14, fontweight='bold', transform=ax4.transAxes)
    features = [
        '• Smooth data transitions',
        '• Multiple easing functions',
        '• Color & size transitions',
        '• Figure state transitions',
        '• Customizable duration & FPS',
        '• Line, scatter, bar support',
        '• Convenience functions',
        '• Easy integration'
    ]
    
    for i, feature in enumerate(features):
        ax4.text(0.1, 0.8 - i*0.08, feature, ha='left', va='top', fontsize=11, transform=ax4.transAxes)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Features', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('transitions_overview.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ Created transitions_overview.png")


def main():
    """Create all static example images."""
    print("=== Creating Static Examples for Transitions ===")
    print("Generating before/after images and overview diagrams...\n")
    
    try:
        create_line_before_after()
        create_scatter_before_after()
        create_bar_before_after()
        create_easing_comparison()
        create_overview_diagram()
        
        print("\n=== Static Examples Complete ===")
        print("Generated images:")
        print("- line_transition_before.png / line_transition_after.png")
        print("- scatter_transition_before.png / scatter_transition_after.png")
        print("- bar_transition_before.png / bar_transition_after.png")
        print("- easing_functions_comparison.png")
        print("- transitions_overview.png")
        print("\nThese images demonstrate the before/after states of transitions.")
        
    except Exception as e:
        print(f"\nError during image creation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)