#!/usr/bin/env python3
"""
Rembg Library Test Script
This script demonstrates various ways to use the rembg library for background removal.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np

# Import rembg
try:
    from rembg import remove, new_session
    print("✅ rembg imported successfully!")
except ImportError as e:
    print(f"❌ Error importing rembg: {e}")
    sys.exit(1)

def create_output_directory():
    """Create the pruebas output directory if it doesn't exist."""
    output_dir = Path("pruebas")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir.absolute()}")
    return output_dir

def test_basic_removal():
    """Test basic background removal functionality."""
    print("\n🔍 Testing basic background removal...")
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Check if we have example images
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found. Please make sure you're in the correct directory.")
        return False
    
    # Find an example image
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    # Use the first example image
    input_image_path = example_images[0]
    output_image_path = output_dir / f"test_output_{input_image_path.stem}.png"
    
    print(f"📸 Using input image: {input_image_path.name}")
    
    try:
        # Method 1: Using PIL Image
        print("   Method 1: Using PIL Image...")
        input_image = Image.open(input_image_path)
        output_image = remove(input_image)
        output_image.save(output_image_path)
        print(f"   ✅ Saved output as: {output_image_path}")
        
        # Method 2: Using bytes
        print("   Method 2: Using bytes...")
        with open(input_image_path, 'rb') as i:
            input_bytes = i.read()
            output_bytes = remove(input_bytes)
            output_bytes_path = output_dir / f"test_output_bytes_{input_image_path.stem}.png"
            with open(output_bytes_path, 'wb') as o:
                o.write(output_bytes)
        print(f"   ✅ Saved output as: {output_bytes_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during background removal: {e}")
        return False

def test_different_models():
    """Test different models available in rembg."""
    print("\n🔍 Testing different models...")
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Available models
    models = [
        "u2net",           # Default model for general use
        "u2netp",          # Lightweight version
        "u2net_human_seg", # Human segmentation
        "isnet-general-use", # General use model
        "isnet-anime",     # Anime character segmentation
    ]
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found.")
        return False
    
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    input_image_path = example_images[0]
    input_image = Image.open(input_image_path)
    
    for model in models:
        try:
            print(f"   Testing model: {model}")
            session = new_session(model)
            output_image = remove(input_image, session=session)
            output_path = output_dir / f"test_output_{model}_{input_image_path.stem}.png"
            output_image.save(output_path)
            print(f"   ✅ Saved output as: {output_path}")
        except Exception as e:
            print(f"   ❌ Error with model {model}: {e}")

def test_advanced_features():
    """Test advanced features like alpha matting and post-processing."""
    print("\n🔍 Testing advanced features...")
    
    # Create output directory
    output_dir = create_output_directory()
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found.")
        return False
    
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    input_image_path = example_images[0]
    input_image = Image.open(input_image_path)
    
    try:
        # Test with alpha matting
        print("   Testing with alpha matting...")
        output_alpha = remove(
            input_image, 
            alpha_matting=True,
            alpha_matting_foreground_threshold=270,
            alpha_matting_background_threshold=20,
            alpha_matting_erode_size=11
        )
        output_alpha_path = output_dir / f"test_output_alpha_{input_image_path.stem}.png"
        output_alpha.save(output_alpha_path)
        print(f"   ✅ Saved alpha matting output as: {output_alpha_path}")
        
        # Test with post-processing
        print("   Testing with post-processing...")
        output_post = remove(input_image, post_process_mask=True)
        output_post_path = output_dir / f"test_output_post_{input_image_path.stem}.png"
        output_post.save(output_post_path)
        print(f"   ✅ Saved post-processed output as: {output_post_path}")
        
        # Test with background color replacement
        print("   Testing with background color replacement...")
        output_bg = remove(input_image, bgcolor=(255, 255, 255, 255))  # White background
        output_bg_path = output_dir / f"test_output_bg_white_{input_image_path.stem}.png"
        output_bg.save(output_bg_path)
        print(f"   ✅ Saved white background output as: {output_bg_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during advanced testing: {e}")
        return False

def test_batch_processing():
    """Test batch processing of multiple images."""
    print("\n🔍 Testing batch processing...")
    
    # Create output directory
    output_dir = create_output_directory()
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found.")
        return False
    
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    # Limit to first 3 images for testing
    test_images = example_images[:3]
    
    try:
        # Create a session for better performance
        session = new_session()
        
        for i, image_path in enumerate(test_images):
            print(f"   Processing {i+1}/{len(test_images)}: {image_path.name}")
            input_image = Image.open(image_path)
            output_image = remove(input_image, session=session)
            output_path = output_dir / f"batch_output_{i+1}_{image_path.stem}.png"
            output_image.save(output_path)
            print(f"   ✅ Saved as: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during batch processing: {e}")
        return False

def main():
    """Main function to run all tests."""
    print("🚀 Starting Rembg Library Tests")
    print("=" * 50)
    
    # Test basic functionality
    if test_basic_removal():
        print("✅ Basic removal test passed!")
    else:
        print("❌ Basic removal test failed!")
    
    # Test different models
    test_different_models()
    
    # Test advanced features
    if test_advanced_features():
        print("✅ Advanced features test passed!")
    else:
        print("❌ Advanced features test failed!")
    
    # Test batch processing
    if test_batch_processing():
        print("✅ Batch processing test passed!")
    else:
        print("❌ Batch processing test failed!")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print(f"\n📁 Check the 'pruebas' directory for output images:")
    print("   - test_output_*.png: Basic removal outputs")
    print("   - test_output_*_model_*.png: Different model outputs")
    print("   - test_output_alpha_*.png: Alpha matting outputs")
    print("   - test_output_post_*.png: Post-processed outputs")
    print("   - test_output_bg_white_*.png: White background outputs")
    print("   - batch_output_*.png: Batch processing outputs")

if __name__ == "__main__":
    main() 