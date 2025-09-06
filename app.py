# ==============================================================================
# Healing Animal Helper (HAH) - Hugging Face Spaces Edition
# For Nano Banana Challenge by Google DeepMind
# ==============================================================================

import os
import gradio as gr
from PIL import Image, ImageDraw
import google.generativeai as genai
import requests
import random
import io
import time
from typing import Optional

print("🐾 HAH - Healing Animal Helper")
print("🍌 Powered by Nano Banana (Gemini 2.5 Flash Image)")
print("🤗 Running on Hugging Face Spaces")

# ------------------------------------------------------------------------------
# Setup Gemini API
# ------------------------------------------------------------------------------
def setup_gemini_api():
    """Setup Gemini API with Hugging Face Secrets"""
    try:
        # In Hugging Face Spaces, use secrets
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  GEMINI_API_KEY not found in environment")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
        print("✅ Nano Banana API configured successfully")
        return model
        
    except Exception as e:
        print(f"❌ API setup failed: {e}")
        return None

# Initialize model
model = setup_gemini_api()

# ------------------------------------------------------------------------------
# Core Nano Banana Function
# ------------------------------------------------------------------------------
def call_nano_banana_api(image: Image.Image, animal_type: str) -> Optional[Image.Image]:
    """Call Nano Banana for image editing magic"""
    if not model:
        return None
    
    try:
        prompt = (
            f"Please gently edit this photograph by adding a cute, peaceful {animal_type} "
            f"that naturally belongs in this scene. The {animal_type} should be: "
            f"• Sleeping or resting peacefully "
            f"• Positioned in a natural spot (chair, floor, corner, or cozy area) "
            f"• Perfectly integrated with the existing lighting, shadows, and perspective "
            f"• Appropriately sized for the scene "
            f"• Looking completely at home in this environment "
            f"The goal is to transform this space from feeling empty to feeling warm and inhabited, "
            f"while maintaining photorealistic quality and keeping all other elements unchanged."
        )
        
        print(f"🍌 Calling Nano Banana for {animal_type}...")
        start_time = time.time()
        
        response = model.generate_content([prompt, image])
        
        if not response.parts:
            return None
        
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                image_data = part.inline_data.data
                edited_image = Image.open(io.BytesIO(image_data))
                
                elapsed = time.time() - start_time
                print(f"✅ Nano Banana magic completed in {elapsed:.2f}s!")
                return edited_image
        
        return None
        
    except Exception as e:
        print(f"❌ Nano Banana error: {e}")
        return None

# ------------------------------------------------------------------------------
# Backup Local Composition
# ------------------------------------------------------------------------------
def create_cute_animal_sprite(animal_type: str, size: tuple = (100, 100)) -> Image.Image:
    """Create cute animal sprite as backup"""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    w, h = size
    colors = {
        "cat": (255, 165, 0, 200),
        "kitten": (255, 192, 203, 200),
        "dog": (139, 69, 19, 200),
        "puppy": (255, 218, 185, 200),
        "rabbit": (255, 255, 255, 200),
        "hamster": (222, 184, 135, 200)
    }
    
    color = colors.get(animal_type, (180, 180, 180, 200))
    
    if animal_type in ["cat", "kitten"]:
        # Cat body and head
        draw.ellipse([w//4, h//2, 3*w//4, 4*h//5], fill=color)
        draw.ellipse([w//3, h//4, 2*w//3, 3*h//5], fill=color)
        # Triangle ears
        draw.polygon([(w//3, h//3), (w//3 + 10, h//6), (w//2 - 6, h//3)], fill=color)
        draw.polygon([(w//2 + 6, h//3), (2*w//3 - 10, h//6), (2*w//3, h//3)], fill=color)
        # Sleeping eyes
        draw.arc([w//2 - 12, h//3 + 6, w//2 - 2, h//3 + 16], 0, 180, fill=(0, 0, 0), width=2)
        draw.arc([w//2 + 2, h//3 + 6, w//2 + 12, h//3 + 16], 0, 180, fill=(0, 0, 0), width=2)
    
    elif animal_type in ["dog", "puppy"]:
        # Dog body and head
        draw.ellipse([w//4, h//2, 3*w//4, 4*h//5], fill=color)
        draw.ellipse([w//3, h//4, 2*w//3, 3*h//5], fill=color)
        # Floppy ears
        draw.ellipse([w//4, h//3, w//3 + 6, h//2], fill=color)
        draw.ellipse([2*w//3 - 6, h//3, 3*w//4, h//2], fill=color)
        # Sleeping eyes
        draw.arc([w//2 - 12, h//3 + 6, w//2 - 2, h//3 + 16], 0, 180, fill=(0, 0, 0), width=2)
        draw.arc([w//2 + 2, h//3 + 6, w//2 + 12, h//3 + 16], 0, 180, fill=(0, 0, 0), width=2)
    
    else:
        # Generic cute animal
        draw.ellipse([w//3, h//3, 2*w//3, 4*h//5], fill=color)
        draw.ellipse([w//3, h//4, w//3 + 12, h//4 + 12], fill=color)
        draw.ellipse([2*w//3 - 12, h//4, 2*w//3, h//4 + 12], fill=color)
        draw.arc([w//2 - 10, h//2, w//2, h//2 + 10], 0, 180, fill=(0, 0, 0), width=2)
        draw.arc([w//2, h//2, w//2 + 10, h//2 + 10], 0, 180, fill=(0, 0, 0), width=2)
    
    # Add sleeping zzz
    try:
        draw.text((w - 20, h//8), "z", fill=(100, 100, 100, 150))
        draw.text((w - 14, h//10), "z", fill=(100, 100, 100, 120))
    except:
        pass
    
    return img

def local_healing_composition(background: Image.Image, animal_type: str) -> Image.Image:
    """Local composition as backup"""
    try:
        bg_width, bg_height = background.size
        animal_size = max(60, min(bg_width, bg_height) // 10)
        animal = create_cute_animal_sprite(animal_type, (animal_size, animal_size))
        
        # Smart positioning
        positions = [
            (bg_width - animal_size - 20, bg_height - animal_size - 20),
            (20, bg_height - animal_size - 20),
            (bg_width - animal_size - 20, 20),
            (bg_width // 3, bg_height - animal_size - 20),
        ]
        
        x, y = random.choice(positions)
        x = max(5, min(x, bg_width - animal_size - 5))
        y = max(5, min(y, bg_height - animal_size - 5))
        
        result = background.copy()
        if result.mode != 'RGBA':
            result = result.convert('RGBA')
        
        result.paste(animal, (x, y), animal)
        
        if result.mode == 'RGBA':
            rgb_result = Image.new('RGB', result.size, (255, 255, 255))
            rgb_result.paste(result, mask=result.split()[-1])
            result = rgb_result
        
        return result
        
    except Exception as e:
        print(f"❌ Local composition failed: {e}")
        return background

# ------------------------------------------------------------------------------
# Main Healing Function
# ------------------------------------------------------------------------------
def generate_healing_image(input_image, animal_choice):
    """Main healing image generation function"""
    if input_image is None:
        gr.Warning("Please upload an image first! 📸")
        return None
    
    try:
        print(f"🎨 Starting healing process with {animal_choice}...")
        
        # Try Nano Banana first
        if model:
            result = call_nano_banana_api(input_image, animal_choice)
            if result is not None:
                print("🎉 Nano Banana healing successful!")
                return result
            else:
                print("⚠️  Nano Banana unavailable, using local healing...")
        
        # Fallback to local composition
        result = local_healing_composition(input_image, animal_choice)
        print("✅ Local healing completed!")
        return result
        
    except Exception as e:
        print(f"❌ Healing process error: {e}")
        gr.Warning(f"Healing magic encountered an issue: {str(e)}")
        return input_image

# ------------------------------------------------------------------------------
# Gradio Interface
# ------------------------------------------------------------------------------
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="🐾 Healing Animal Helper - Nano Banana Edition",
    css="""
        .healing-header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;
        }
        .animal-card { 
            background: #f8f9fa; border-radius: 12px; padding: 15px; margin: 10px 0;
        }
        .magic-button { 
            background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
            border: none; border-radius: 25px; color: white; font-weight: bold;
        }
    """
) as demo:
    
    gr.HTML("""
        <div class="healing-header">
            <h1>🐾 Healing Animal Helper (HAH)</h1>
            <h2>🍌 Powered by Nano Banana Technology</h2>
            <p><em>Transform loneliness into companionship • 將孤單轉化為陪伴</em></p>
            <p><strong>🏆 Entry for Nano Banana 48-Hour Challenge by Google DeepMind</strong></p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📸 **Step 1: Upload Your Photo**")
            input_image = gr.Image(
                label="Upload a photo that feels a bit empty",
                type="pil",
                height=350,
                elem_classes=["animal-card"]
            )
            
            gr.Markdown("### 🐾 **Step 2: Choose Your Healing Companion**")
            animal_choice = gr.Dropdown(
                label="Select your animal friend",
                choices=[
                    ("🐱 Cat - Elegant & Peaceful", "cat"),
                    ("🐶 Dog - Loyal & Warm", "dog"), 
                    ("🐰 Rabbit - Pure & Cute", "rabbit"),
                    ("🐹 Hamster - Tiny & Healing", "hamster"),
                    ("🐕 Puppy - Playful & Sweet", "puppy"),
                    ("🐈 Kitten - Soft & Cuddly", "kitten")
                ],
                value="cat",
                info="Each animal brings unique healing energy ✨",
                elem_classes=["animal-card"]
            )
            
            gr.Markdown("### ✨ **Step 3: Create Magic**")
            generate_btn = gr.Button(
                "🍌 Generate Healing with Nano Banana",
                variant="primary",
                size="lg",
                elem_classes=["magic-button"]
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 🎉 **Your Healing Masterpiece**")
            output_image = gr.Image(
                label="Your transformed, warm image",
                height=350,
                elem_classes=["animal-card"]
            )
            
            gr.HTML(f"""
                <div style="background: #e3f2fd; border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <h4>🍌 Nano Banana Features</h4>
                    <ul>
                        <li>🎨 <strong>True AI Painting</strong> - Not overlays, real drawing</li>
                        <li>🌟 <strong>Perfect Integration</strong> - Natural lighting & shadows</li>
                        <li>💝 <strong>Emotional Healing</strong> - From lonely to loved</li>
                        <li>⚡ <strong>Instant Magic</strong> - {'API Ready' if model else 'Local Mode'}</li>
                    </ul>
                </div>
            """)
    
    # Connect the function
    generate_btn.click(
        fn=generate_healing_image,
        inputs=[input_image, animal_choice],
        outputs=output_image,
        show_progress=True
    )
    
    with gr.Row():
        gr.Markdown("""
        ---
        ## 💡 **How to Get the Best Healing Results**
        
        **🎯 Perfect Image Types:**
        - 🪑 Empty chairs in cafés, restaurants, or homes
        - 🏠 Living rooms, bedrooms, study corners  
        - 🌳 Park benches, outdoor seating areas
        - 📚 Library nooks, reading corners
        - ☕ Tables with items but missing "life"
        
        **🚀 The HAH Difference:**
        - 🤖 **Advanced AI**: Uses Google DeepMind's Nano Banana technology
        - 🎨 **Real Artistry**: Creates, doesn't just paste
        - 💝 **Emotional Impact**: Transforms feeling from empty to inhabited
        - 🌍 **Social Good**: Applications in healthcare, therapy, and wellness
        
        **🏆 Challenge Entry**: This demonstrates Nano Banana's power to create emotionally meaningful experiences through advanced image editing.
        """)
    
    gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); border-radius: 15px;">
            <h3>🏆 Nano Banana 48-Hour Challenge Entry</h3>
            <p><strong>By:</strong> [Your Name] | <strong>Technology:</strong> Gemini 2.5 Flash Image Preview</p>
            <p><em>"HAH showcases how AI can heal human emotions by transforming empty spaces into warm, companioned scenes. Every lonely photo deserves a friend."</em></p>
            <p>
                <strong>🎥 Demo Video:</strong> <a href="your-video-link" target="_blank">Watch on YouTube</a> | 
                <strong>📁 Source Code:</strong> <a href="your-github-link" target="_blank">View on GitHub</a>
            </p>
        </div>
    """)

# ------------------------------------------------------------------------------
# Launch
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 Launching HAH on Hugging Face Spaces...")
    print(f"🍌 Nano Banana Status: {'✅ Connected' if model else '❌ Local Mode Only'}")
    print("🤗 Visit the Spaces URL to start healing!")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )