"""
NAIVE IMAGE DEDUPLICATION
Compare every pair pixel-by-pixel. O(N^2).
"""

from PIL import Image
import time
import warnings

# Suppress deprecation for now
warnings.filterwarnings("ignore", category=DeprecationWarning)

def image_hash_pixels(image_path):
    """Average pixel value as simple signature"""
    img = Image.open(image_path).convert('L').resize((8, 8))
    try:
        pixels = list(img.get_image_data())
    except AttributeError:
        pixels = list(img.getdata())
    return sum(pixels) / len(pixels)

def naive_dedup(signatures):
    """Compare every pair of pre-computed signatures — O(N^2)"""
    duplicates = []
    paths = list(signatures.keys())
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            diff = abs(signatures[paths[i]] - signatures[paths[j]])
            if diff < 10:
                duplicates.append((paths[i], paths[j], diff))
    return duplicates

if __name__ == "__main__":
    import random
    import os
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Generate images
    for i in range(50):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        img = Image.new('RGB', (500, 500), color=(r, g, b))
        img.save(f"img_{i}.png")
    
    # Pre-compute signatures
    paths = [f"img_{i}.png" for i in range(50)]
    sigs = {p: image_hash_pixels(p) for p in paths}
    
    start = time.time()
    dups = naive_dedup(sigs)
    print(f"Found {len(dups)} similar pairs in {time.time() - start:.4f}s")
    
    # Cleanup
    for p in paths:
        os.remove(p)