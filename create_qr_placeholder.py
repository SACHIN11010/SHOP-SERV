import os
from pathlib import Path

# Create a simple 1x1 transparent PNG
img_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x0bIDAT\x08\x1dc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa7\x9a\xc9\x8e\x00\x00\x00\x00IEND\xaeB`\x82'

# Create the directory if it doesn't exist
img_dir = Path("static/img")
img_dir.mkdir(parents=True, exist_ok=True)

# Save the image
with open(img_dir / "qr-placeholder.png", "wb") as f:
    f.write(img_data)

print("QR code placeholder created successfully!")
