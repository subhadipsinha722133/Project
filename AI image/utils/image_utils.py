import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2
import io

def generate_fractal_art(width, height, complexity=5):
    """Generate fractal-like abstract art"""
    img = Image.new('RGB', (width, height), color='black')
    pixels = img.load()
    
    for x in range(width):
        for y in range(height):
            # Create colorful fractal pattern
            r = int(128 + 127 * np.sin(x * complexity / width))
            g = int(128 + 127 * np.sin(y * complexity / height))
            b = int(128 + 127 * np.sin((x + y) * complexity / (width + height)))
            pixels[x, y] = (r, g, b)
    
    return img

def generate_geometric_pattern(width, height, shapes=10):
    """Generate geometric pattern art"""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    for _ in range(shapes):
        # Random shapes with random colors
        shape_type = np.random.choice(['circle', 'rectangle', 'polygon'])
        color = tuple(np.random.randint(0, 255, 3))
        
        if shape_type == 'circle':
            x, y = np.random.randint(0, width), np.random.randint(0, height)
            radius = np.random.randint(10, min(width, height) // 4)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
        
        elif shape_type == 'rectangle':
            x1, y1 = np.random.randint(0, width), np.random.randint(0, height)
            x2, y2 = np.random.randint(x1, width), np.random.randint(y1, height)
            draw.rectangle([x1, y1, x2, y2], fill=color)
        
        else:  # polygon
            points = []
            for _ in range(5):
                points.append((np.random.randint(0, width), np.random.randint(0, height)))
            draw.polygon(points, fill=color)
    
    return img

def apply_filters(image, filter_type):
    """Apply various artistic filters"""
    if filter_type == 'blur':
        return image.filter(ImageFilter.GaussianBlur(5))
    elif filter_type == 'contour':
        return image.filter(ImageFilter.CONTOUR)
    elif filter_type == 'emboss':
        return image.filter(ImageFilter.EMBOSS)
    elif filter_type == 'edges':
        return image.filter(ImageFilter.FIND_EDGES)
    else:
        return image

def image_to_bytes(image):
    """Convert PIL image to bytes for download"""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()