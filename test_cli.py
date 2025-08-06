#!/usr/bin/env python3
"""
Rembg CLI Test Script
This script demonstrates how to use the rembg command-line interface.
"""

import subprocess
import sys
from pathlib import Path

def create_output_directory():
    """Create the pruebas output directory if it doesn't exist."""
    output_dir = Path("pruebas")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir.absolute()}")
    return output_dir

def test_cli_help():
    """Test the CLI help command."""
    print("🔍 Testing CLI help...")
    try:
        result = subprocess.run(['rembg', '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CLI help command works!")
            print("Available commands:")
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('Usage:'):
                    print(f"   {line.strip()}")
        else:
            print("❌ CLI help command failed!")
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ rembg command not found in PATH")
        return False

def test_cli_remove():
    """Test the CLI remove command."""
    print("\n🔍 Testing CLI remove command...")
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Check if we have example images
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("❌ Examples directory not found.")
        return False
    
    # Find an example image
    example_images = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))
    if not example_images:
        print("❌ No example images found.")
        return False
    
    input_image_path = example_images[0]
    output_image_path = output_dir / f"cli_output_{input_image_path.stem}.png"
    
    print(f"📸 Using input image: {input_image_path.name}")
    
    try:
        # Test basic removal
        cmd = ['rembg', 'i', str(input_image_path), str(output_image_path)]
        print(f"   Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Successfully created: {output_image_path}")
            
            # Check if output file exists
            if output_image_path.exists():
                print(f"   ✅ Output file exists and has size: {output_image_path.stat().st_size} bytes")
                return True
            else:
                print("   ❌ Output file not found")
                return False
        else:
            print(f"   ❌ Command failed with return code: {result.returncode}")
            print(f"   Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error running CLI command: {e}")
        return False

def test_cli_models():
    """Test CLI with different models."""
    print("\n🔍 Testing CLI with different models...")
    
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
    
    # Test different models
    models = ["u2net", "u2netp", "isnet-general-use"]
    
    for model in models:
        try:
            output_path = output_dir / f"cli_output_{model}_{input_image_path.stem}.png"
            cmd = ['rembg', 'i', '-m', model, str(input_image_path), str(output_path)]
            print(f"   Testing model {model}...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                print(f"   ✅ Successfully created: {output_path}")
            else:
                print(f"   ❌ Failed to create output for model {model}")
                
        except Exception as e:
            print(f"   ❌ Error testing model {model}: {e}")

def main():
    """Main function to run CLI tests."""
    print("🚀 Starting Rembg CLI Tests")
    print("=" * 50)
    
    # Test CLI help
    if test_cli_help():
        print("✅ CLI help test passed!")
    else:
        print("❌ CLI help test failed!")
    
    # Test CLI remove
    if test_cli_remove():
        print("✅ CLI remove test passed!")
    else:
        print("❌ CLI remove test failed!")
    
    # Test CLI with different models
    test_cli_models()
    
    print("\n" + "=" * 50)
    print("🎉 CLI tests completed!")
    print(f"\n📁 Check the 'pruebas' directory for CLI output images:")
    print("   - cli_output_*.png: CLI command outputs")

if __name__ == "__main__":
    main() 