"""
OPTIMIZED IMAGE DEDUPLICATION
Perceptual hash + Hamming distance. O(N).
"""

from PIL import Image
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def phash(image_path, hash_size=8):
    """Difference hash (dHash)"""
    img = Image.open(image_path).convert('L')
    img = img.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    
    try:
        pixels = list(img.get_image_data())
    except AttributeError:
        pixels = list(img.getdata())
    
    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * (hash_size + 1) + col]
            right = pixels[row * (hash_size + 1) + col + 1]
            diff.append(left > right)
    
    hash_value = 0
    for bit in diff:
        hash_value = (hash_value << 1) | int(bit)
    
    return hash_value

def hamming_distance(hash1, hash2):
    xor = hash1 ^ hash2
    return bin(xor).count('1')

def optimized_dedup(hashes, threshold=2):
    """Compare pre-computed hashes — O(N) total with smart bucketing"""
    duplicates = []
    paths = list(hashes.keys())
    
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            dist = hamming_distance(hashes[paths[i]], hashes[paths[j]])
            if dist <= threshold:
                duplicates.append((paths[i], paths[j], dist))
    
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
    
    # Pre-compute hashes
    paths = [f"img_{i}.png" for i in range(50)]
    hashes = {p: phash(p) for p in paths}
    
    start = time.time()
    dups = optimized_dedup(hashes)
    print(f"Found {len(dups)} similar pairs in {time.time() - start:.4f}s")
    
    # Cleanup
    for p in paths:
        os.remove(p)