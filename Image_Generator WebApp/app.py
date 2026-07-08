# app.py
import os
import io
import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Stable Diffusion Streamlit", layout="centered")

st.title("Stable Diffusion — Streamlit demo")
st.markdown(
    """
Enter a prompt and generate an image.  
Tip: for large models (SDXL) you generally need a GPU (CUDA).  
If a model is gated on Hugging Face, provide an HF token below.
"""
)

# --- Sidebar / settings ---
st.sidebar.header("Model & runtime")
model_choice = st.sidebar.selectbox(
    "Choose model",
    ("dreamlike-art/dreamlike-diffusion-1.0", "stabilityai/stable-diffusion-xl-base-1.0")
)
hf_token = st.sidebar.text_input("Hugging Face token (optional)", type="password")
device_override = st.sidebar.selectbox("Device override (auto-detect default)", ("auto", "cuda", "cpu"))

st.sidebar.markdown("**Generation settings**")
height = st.sidebar.selectbox("Height", (512, 640, 768))
width = st.sidebar.selectbox("Width", (512, 640, 768))
num_inference_steps = st.sidebar.slider("Steps", 10, 100, 28)
guidance_scale = st.sidebar.slider("Guidance scale", 1.0, 15.0, 7.5)
seed_input = st.sidebar.number_input("Seed (0 = random)", min_value=0, step=1, value=0)
num_images = st.sidebar.slider("Images to generate", 1, 4, 1)

# --- Device detection & dtype ---
def pick_device(override):
    if override == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return override

device = pick_device(device_override)
torch_dtype = torch.float16 if device == "cuda" else torch.float32

st.sidebar.write(f"Using device: **{device}** — dtype: **{torch_dtype}**")

# --- Cache the pipeline so it persists ---
@st.cache_resource(show_spinner=False)
def load_pipeline(model_id: str, device: str, dtype: torch.dtype, token: str | None):
    load_kwargs = {}
    if token:
        load_kwargs["use_auth_token"] = token
    # for SDXL there may be special kwargs; this is a general loader
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype, **load_kwargs)
    # move to device
    pipe = pipe.to(device)
    # Try to enable memory optimizations if available
    try:
        pipe.enable_attention_slicing()
    except Exception:
        pass
    try:
        # xformers optional; only available if installed
        pipe.enable_xformers_memory_efficient_attention()
    except Exception:
        pass
    return pipe

# --- UI for prompt & generate ---
prompt = st.text_area("Prompt", value="A fantasy castle on a floating island, cinematic lighting", height=120)
generate_btn = st.button("Generate")

# Optional negative prompt
negative_prompt = st.text_input("Negative prompt (optional)", value="")

if generate_btn:
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        # Warn about CPU with SDXL
        if device == "cpu" and "stable-diffusion-xl" in model_choice:
            st.warning("SDXL on CPU is very slow and may not fit in memory. Use a GPU or choose the Dreamlike model.")
        try:
            with st.spinner("Loading pipeline (cached) — may take a while on first run..."):
                pipe = load_pipeline(model_choice, device, torch_dtype, hf_token or None)
        except Exception as e:
            st.exception(f"Failed to load model: {e}")
            st.stop()

        # set seed
        if seed_input == 0:
            seed = random.randint(1, 2**31 - 1)
        else:
            seed = int(seed_input)

        generator = torch.Generator(device=device).manual_seed(seed) if device == "cuda" or device == "cpu" else None

        images = []
        try:
            with st.spinner("Generating image(s)..."):
                # diffusers pipeline call
                out = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt if negative_prompt.strip() else None,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=generator,
                    num_images_per_prompt=num_images,
                )
                images = out.images
        except Exception as e:
            st.exception(f"Generation failed: {e}")
            st.stop()

        # display images and download links
        cols = st.columns(min(len(images), 4))
        for i, img in enumerate(images):
            col = cols[i % len(cols)]
            with col:
                st.image(img, use_column_width=True, caption=f"Seed: {seed}  |  Model: {model_choice.split('/')[-1]}")
                # offer download
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                btn_label = f"Download image {i+1}"
                st.download_button(btn_label, data=buf, file_name=f"sd_image_{seed}_{i+1}.png", mime="image/png")

        # show generation metadata
        st.markdown("---")
        st.write("### Generation details")
        st.write(f"- Model: `{model_choice}`")
        st.write(f"- Seed: `{seed}`")
        st.write(f"- Size: {width}×{height}")
        st.write(f"- Steps: {num_inference_steps}")
        st.write(f"- Guidance scale: {guidance_scale}")

st.markdown("---")
st.write("Made with diffusers + Streamlit. Run: `streamlit run app.py`")
st.write("If you hit memory/CUDA errors, try lowering `height`/`width`/`steps` or use a smaller model.")
