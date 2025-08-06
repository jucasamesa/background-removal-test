#!/usr/bin/env python3
"""
Background Extraction Test Script
This script demonstrates how to extract only the background from images using rembg.
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
    """Create the onlybg output directory if it doesn't exist."""
    output_dir = Path("onlybg")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir.absolute()}")
    return output_dir

def extract_background_using_mask_inversion():
    """Extract background by inverting the rembg mask."""
    print("\n🔍 Testing background extraction using mask inversion...")
    
    output_dir = create_output_directory()
    
    # Check if we have example images
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found.")
        return False
    
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    input_image_path = example_images[0]
    print(f"📸 Using input image: {input_image_path.name}")
    
    try:
        # Load original image
        original_image = Image.open(input_image_path)
        
        # Get the mask using rembg (this gives us the foreground mask)
        print("   Getting foreground mask...")
        mask = remove(original_image, only_mask=True)
        
        # Convert mask to numpy array
        mask_array = np.array(mask)
        
        # Invert the mask to get background mask
        print("   Inverting mask to get background...")
        background_mask = 255 - mask_array
        
        # Convert back to PIL Image
        background_mask_pil = Image.fromarray(background_mask.astype(np.uint8))
        
        # Apply the background mask to the original image
        print("   Applying background mask to original image...")
        original_array = np.array(original_image)
        
        # Create a 4-channel image (RGBA) if it's not already
        if original_array.shape[2] == 3:
            # Add alpha channel
            rgba_image = np.zeros((original_array.shape[0], original_array.shape[1], 4), dtype=np.uint8)
            rgba_image[:, :, :3] = original_array
            rgba_image[:, :, 3] = 255  # Full opacity
        else:
            rgba_image = original_array
        
        # Apply the background mask to the alpha channel
        rgba_image[:, :, 3] = background_mask[:, :, 0] if background_mask.ndim == 3 else background_mask
        
        # Convert back to PIL Image
        background_image = Image.fromarray(rgba_image, 'RGBA')
        
        # Save the background
        output_path = output_dir / f"background_extracted_{input_image_path.stem}.png"
        background_image.save(output_path)
        print(f"   ✅ Saved background as: {output_path}")
        
        # Also save the inverted mask for reference
        mask_output_path = output_dir / f"background_mask_{input_image_path.stem}.png"
        background_mask_pil.save(mask_output_path)
        print(f"   ✅ Saved background mask as: {mask_output_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during background extraction: {e}")
        return False

def extract_background_using_alpha_compositing():
    """Extract background using alpha compositing technique."""
    print("\n🔍 Testing background extraction using alpha compositing...")
    
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
    print(f"📸 Using input image: {input_image_path.name}")
    
    try:
        # Load original image
        original_image = Image.open(input_image_path)
        
        # Remove background (get foreground with transparent background)
        print("   Removing background to get foreground...")
        foreground = remove(original_image)
        
        # Create a white background image
        print("   Creating white background...")
        white_bg = Image.new('RGBA', original_image.size, (255, 255, 255, 255))
        
        # Composite foreground over white background
        print("   Compositing foreground over white background...")
        composite = Image.alpha_composite(white_bg, foreground)
        
        # Now subtract the foreground from original to get background
        print("   Subtracting foreground from original...")
        original_array = np.array(original_image.convert('RGBA'))
        composite_array = np.array(composite)
        foreground_array = np.array(foreground)
        
        # Create background by subtracting foreground
        background_array = original_array.copy()
        
        # Where foreground has alpha > 0, make background transparent
        alpha_mask = foreground_array[:, :, 3] > 0
        background_array[alpha_mask, 3] = 0  # Make transparent where foreground exists
        
        background_image = Image.fromarray(background_array, 'RGBA')
        
        # Save the background
        output_path = output_dir / f"background_alpha_composite_{input_image_path.stem}.png"
        background_image.save(output_path)
        print(f"   ✅ Saved background as: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during alpha compositing: {e}")
        return False

def main():
    """Main function to run background extraction tests."""
    print("🚀 Starting Background Extraction Tests")
    print("=" * 50)
    
    # Test mask inversion method
    if extract_background_using_mask_inversion():
        print("✅ Background extraction using mask inversion passed!")
    else:
        print("❌ Background extraction using mask inversion failed!")
    
    # Test alpha compositing method
    if extract_background_using_alpha_compositing():
        print("✅ Background extraction using alpha compositing passed!")
    else:
        print("❌ Background extraction using alpha compositing failed!")
    
    print("\n" + "=" * 50)
    print("🎉 Background extraction tests completed!")
    print(f"\n📁 Check the 'onlybg' directory for output images:")
    print("   - background_extracted_*.png: Background extracted using mask inversion")
    print("   - background_mask_*.png: Background mask")
    print("   - background_alpha_composite_*.png: Background extracted using alpha compositing")

if __name__ == "__main__":
    main() 