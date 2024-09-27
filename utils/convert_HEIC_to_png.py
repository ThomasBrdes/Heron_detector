import os
from PIL import Image
import pillow_heif

def convert_heic_to_png(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Filter out HEIC files
    heic_files = [f for f in files if f.lower().endswith('.heic')]
    
    if not heic_files:
        print("No HEIC files found in the folder.")
        return
    
    # Create a subfolder for PNGs if it doesn't exist
    png_folder = os.path.join(folder_path, 'png')
    os.makedirs(png_folder, exist_ok=True)
    
    for heic_file in heic_files:
        heic_file_path = os.path.join(folder_path, heic_file)
        png_file_path = os.path.join(png_folder, f"{os.path.splitext(heic_file)[0]}.png")
        
        # Open the HEIC file
        heif_file = pillow_heif.read_heif(heic_file_path)
        
        # Convert to a PIL Image
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        
        # Save the image as PNG
        image.save(png_file_path, "PNG")
        print(f"Converted {heic_file} to {png_file_path}")

if __name__ == "__main__":
    folder_path = "C:/Users/Thomas/Documents/DATASETS/heron"
    convert_heic_to_png(folder_path)
