"""
DEMO: Perceptual Hash vs Pixel Average
Uses images with actual edges and patterns.
"""

import os
from PIL import Image, ImageDraw, ImageFilter
from naive import image_hash_pixels
from optimized import phash, hamming_distance

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create original with actual content (circles, lines)
original = Image.new('RGB', (500, 500), color=(255, 255, 255))
draw = ImageDraw.Draw(original)
draw.ellipse([100, 100, 400, 400], fill=(100, 150, 200))
draw.rectangle([50, 50, 150, 150], fill=(200, 50, 100))
draw.line([0, 0, 500, 500], fill=(0, 0, 0), width=5)
original.save("original.png")

# Modified versions
resized = original.resize((400, 400))
resized.save("resized.png")

blurred = original.filter(ImageFilter.GaussianBlur(radius=2))
blurred.save("blurred.png")

compressed = original.copy()
compressed.save("compressed.jpg", quality=50)

# Different image
different = Image.new('RGB', (500, 500), color=(255, 255, 255))
draw2 = ImageDraw.Draw(different)
draw2.polygon([(250, 50), (450, 450), (50, 450)], fill=(50, 200, 100))
different.save("different.png")

images = {
    "original": "original.png",
    "resized": "resized.png",
    "blurred": "blurred.png",
    "compressed": "compressed.jpg",
    "different": "different.png",
}

print("=" * 60)
print("NAIVE: Pixel Average")
print("=" * 60)
naive_sigs = {name: image_hash_pixels(path) for name, path in images.items()}
for name, sig in naive_sigs.items():
    diff = abs(sig - naive_sigs["original"])
    status = "MATCH" if diff < 3 else "DIFFERENT"
    print(f"{name:12} | sig={sig:8.2f} | diff={diff:6.2f} | {status}")

print("\n" + "=" * 60)
print("OPTIMIZED: Perceptual Hash")
print("=" * 60)
opt_hashes = {name: phash(path) for name, path in images.items()}
for name, h in opt_hashes.items():
    dist = hamming_distance(h, opt_hashes["original"])
    status = "MATCH" if dist <= 5 else "DIFFERENT"
    print(f"{name:12} | hash={h:016x} | hamming={dist:2d} | {status}")

# Cleanup
for path in images.values():
    os.remove(path)