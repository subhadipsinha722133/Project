import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import io

# Configure the page
st.set_page_config(
    page_title="AI Art Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .art-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .generated-image {
        border: 3px solid #fff;
        border-radius: 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .stButton button {
        width: 100%;
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

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

def main():
    # Header
    st.markdown('<h1 class="main-header">🎨 AI Art Generator</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'regenerate_counter' not in st.session_state:
        st.session_state.regenerate_counter = 0
    
    # Sidebar
    st.sidebar.title("Configuration")
    
    # Art generation method selection
    generation_method = st.sidebar.selectbox(
        "Select Generation Method",
        ["Fractal Art", "Geometric Patterns", "Abstract Colors", "Symmetrical Patterns"]
    )
    
    # Image dimensions
    col1, col2 = st.sidebar.columns(2)
    with col1:
        width = st.slider("Width", 100, 1024, 512)
    with col2:
        height = st.slider("Height", 100, 1024, 512)
    
    # Parameters based on selected method
    if generation_method == "Fractal Art":
        complexity = st.sidebar.slider("Complexity", 1, 20, 5)
        param1 = complexity
        
    elif generation_method == "Geometric Patterns":
        shapes_count = st.sidebar.slider("Number of Shapes", 5, 50, 15)
        param1 = shapes_count
        
    elif generation_method == "Abstract Colors":
        color_intensity = st.sidebar.slider("Color Intensity", 1, 10, 5)
        param1 = color_intensity
        
    else:  # Symmetrical Patterns
        symmetry_level = st.sidebar.slider("Symmetry Level", 2, 8, 4)
        param1 = symmetry_level
    
    # Filters
    filter_option = st.sidebar.selectbox(
        "Apply Filter",
        ["None", "Blur", "Contour", "Emboss", "Edges"]
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="art-container">', unsafe_allow_html=True)
        st.subheader("Generated Art")
        
        # Generate art button
        if st.button("🎨 Generate Art", use_container_width=True, type="primary"):
            with st.spinner("Creating your masterpiece..."):
                try:
                    # Generate art based on selected method
                    if generation_method == "Fractal Art":
                        image = generate_fractal_art(width, height, param1)
                    elif generation_method == "Geometric Patterns":
                        image = generate_geometric_pattern(width, height, param1)
                    elif generation_method == "Abstract Colors":
                        # Simple color gradient based art
                        image = generate_abstract_colors(width, height, param1)
                    else:  # Symmetrical Patterns
                        image = generate_symmetrical_pattern(width, height, param1)
                    
                    # Apply selected filter
                    if filter_option != "None":
                        image = apply_filters(image, filter_option.lower())
                    
                    # Display the image
                    st.image(image, caption=f"Generated Art - {generation_method}", 
                            use_column_width=True, output_format="PNG")
                    
                    # Store image in session state for download
                    st.session_state.generated_image = image
                    
                except Exception as e:
                    st.error(f"Error generating art: {str(e)}")
        
        # Show existing image if available
        elif st.session_state.generated_image is not None:
            st.image(st.session_state.generated_image, 
                    caption="Your Generated Artwork", 
                    use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Art Information")
        
        if st.session_state.generated_image is not None:
            # Download button
            img_bytes = image_to_bytes(st.session_state.generated_image)
            st.download_button(
                label="📥 Download Art",
                data=img_bytes,
                file_name="ai_art.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Regenerate button
            if st.button("🔄 Regenerate with Same Settings", use_container_width=True):
                st.session_state.regenerate_counter += 1
                st.rerun()
            
            # Image info
            st.info(f"""
            **Image Details:**
            - Size: {width} × {height} pixels
            - Method: {generation_method}
            - Filter: {filter_option}
            """)
        
        # Tips section
        st.subheader("🎯 Tips")
        st.markdown("""
        - **Fractal Art**: Higher complexity = more detailed patterns
        - **Geometric Patterns**: More shapes = denser compositions
        - **Abstract Colors**: Higher intensity = more vibrant colors
        - **Symmetry**: Higher levels = more complex symmetrical patterns
        - Try different filters for various artistic effects
        """)
    
    # Advanced options section
    with st.expander("🛠️ Advanced Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎲 Randomize All Parameters"):
                # This will trigger a rerun with new parameters
                st.session_state.regenerate_counter += 1
                st.rerun()
        
        with col2:
            if st.button("💾 Save Current Settings"):
                st.success("Settings saved! (Feature in development)")
        
        with col3:
            if st.button("🔄 Reset Everything"):
                st.session_state.generated_image = None
                st.session_state.regenerate_counter = 0
                st.rerun()
    
    # Examples gallery
    st.subheader("🎭 Example Gallery")
    st.markdown("Click on any example to see the style")
    
    example_cols = st.columns(4)
    example_methods = ["Fractal Art", "Geometric Patterns", "Abstract Colors", "Symmetrical Patterns"]
    example_params = [8, 20, 7, 6]
    
    for i, col in enumerate(example_cols):
        with col:
            # Generate example image
            if example_methods[i] == "Fractal Art":
                example_img = generate_fractal_art(200, 200, example_params[i])
            elif example_methods[i] == "Geometric Patterns":
                example_img = generate_geometric_pattern(200, 200, example_params[i])
            elif example_methods[i] == "Abstract Colors":
                example_img = generate_abstract_colors(200, 200, example_params[i])
            else:
                example_img = generate_symmetrical_pattern(200, 200, example_params[i])
            
            st.image(example_img, use_column_width=True)
            
            # Use example button
            if st.button(f"Use {example_methods[i]}", key=f"example_{i}"):
                st.session_state.example_selected = i
                st.rerun()

def generate_abstract_colors(width, height, intensity=5):
    """Generate abstract color field art"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for x in range(width):
        for y in range(height):
            # Create vibrant color gradients
            r = int(255 * abs(np.sin(x * intensity / 50)))
            g = int(255 * abs(np.cos(y * intensity / 50)))
            b = int(255 * abs(np.sin((x + y) * intensity / 100)))
            pixels[x, y] = (r, g, b)
    
    return img

def generate_symmetrical_pattern(width, height, symmetry=4):
    """Generate symmetrical pattern art"""
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2
    
    for radius in range(10, max_radius, max_radius // 10):
        for angle in range(0, 360, 360 // symmetry):
            # Create symmetrical patterns
            rad = np.radians(angle)
            x1 = center_x + int(radius * np.cos(rad))
            y1 = center_y + int(radius * np.sin(rad))
            
            color = (
                int(255 * radius / max_radius),
                int(255 * angle / 360),
                int(255 * (1 - radius / max_radius))
            )
            
            draw.ellipse([x1-5, y1-5, x1+5, y1+5], fill=color)
    
    return img

if __name__ == "__main__":
    main()