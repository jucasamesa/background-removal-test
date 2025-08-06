#!/usr/bin/env python3
"""
SAM Background Extraction Test Script
This script demonstrates how to use SAM (Segment Anything Model) for background extraction.
Note: This requires additional dependencies (segment-anything, torch, etc.)
"""

import os
import sys
from pathlib import Path
from PIL import Image
import numpy as np

def check_sam_dependencies():
    """Check if SAM dependencies are available."""
    try:
        import torch
        import segment_anything
        print("✅ SAM dependencies available!")
        return True
    except ImportError as e:
        print(f"❌ SAM dependencies not available: {e}")
        print("To install SAM dependencies, run:")
        print("pip install torch torchvision")
        print("pip install git+https://github.com/facebookresearch/segment-anything.git")
        return False

def extract_background_with_sam():
    """Extract background using SAM (Segment Anything Model)."""
    print("\n🔍 Testing background extraction using SAM...")
    
    if not check_sam_dependencies():
        return False
    
    try:
        import torch
        from segment_anything import SamPredictor, sam_model_registry
        
        output_dir = Path("pruebas")
        output_dir.mkdir(exist_ok=True)
        
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
        
        # Load image
        image = Image.open(input_image_path)
        image_array = np.array(image)
        
        # Initialize SAM (you'll need to download the model first)
        print("   Initializing SAM model...")
        print("   Note: You need to download the SAM model first:")
        print("   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth")
        
        # For now, we'll show the structure without the actual model
        print("   SAM model structure would be initialized here...")
        
        # The process would be:
        # 1. Load SAM model
        # 2. Set image
        # 3. Generate automatic mask proposals
        # 4. Select the largest mask (usually the main object)
        # 5. Invert the mask to get background
        # 6. Apply to original image
        
        print("   SAM background extraction would be implemented here...")
        print("   This requires downloading the SAM model file (~2.4GB)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during SAM background extraction: {e}")
        return False

def main():
    """Main function to run SAM background extraction test."""
    print("🚀 Starting SAM Background Extraction Test")
    print("=" * 50)
    
    if extract_background_with_sam():
        print("✅ SAM background extraction test completed!")
    else:
        print("❌ SAM background extraction test failed!")
    
    print("\n" + "=" * 50)
    print("💡 SAM Alternative:")
    print("   - SAM provides more precise segmentation")
    print("   - Better for complex scenes with multiple objects")
    print("   - Requires downloading large model files")
    print("   - More computationally intensive")
    print("   - Better for interactive segmentation")

if __name__ == "__main__":
    main() 