import os
import sys
import asyncio
import argparse
import tempfile
import gradio as gr
from PIL import Image

# Ensure the parent directory is in path so we can import manga_translator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manga_translator.mode.local import MangaTranslatorLocal
from manga_translator.utils import init_logging

init_logging()

# Supported translators
TRANSLATORS_LIST = ["gpt3.5", "offline", "none", "google", "deepl", "youdao", "baidu", "papago"]

# Supported detectors
DETECTORS_LIST = ["ctd", "default"]

# Target languages map
LANGUAGES_MAP = {
    "English": "ENG",
    "Chinese Simplified": "CHS",
    "Chinese Traditional": "CHT",
    "Japanese": "JPN",
    "Korean": "KOR",
    "Vietnamese": "VIN",
    "French": "FRA",
    "German": "DEU",
    "Russian": "RUS",
    "Spanish": "ESP"
}

# Sizes
SIZES_LIST = ["L", "X", "M", "S"]

async def run_translation(image_path, translator_name, detector_name, target_lang_name, size_name):
    # Set up temp file for result
    temp_dir = tempfile.gettempdir()
    dest_path = os.path.join(temp_dir, f"translated_{os.path.basename(image_path)}")
    if os.path.exists(dest_path):
        try:
            os.remove(dest_path)
        except:
            pass

    # Map target language to code
    target_lang_code = LANGUAGES_MAP.get(target_lang_name, "ENG")

    # Set up parameters dictionary
    params = {
        'mode': 'local',
        'verbose': False,
        'attempts': 0,
        'ignore_errors': False,
        'model_dir': None,
        'use_gpu': True,
        'use_gpu_limited': False,
        'font_path': '',
        'pre_dict': None,
        'post_dict': None,
        'kernel_size': 3,
        'context_size': 0,
        'batch_size': 1,
        'batch_concurrent': False,
        'disable_memory_optimization': False,
        'translator': translator_name,
        'detector': detector_name,
        'direction': 'auto',
        'target_lang': target_lang_code,
        'size': size_name,
        'save_quality': 100,
        'skip_no_text': False,
        'prep_manual': False,
        'save_text': False
    }

    translator = MangaTranslatorLocal(params)
    await translator.translate_path(image_path, dest_path, params)
    
    if os.path.exists(dest_path):
        return dest_path
    else:
        # Fallback to checking if result/final.png exists
        fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result/final.png')
        if os.path.exists(fallback_path):
            return fallback_path
        raise Exception("Translation succeeded but output file was not found.")

def translate_wrapper(image, translator_name, detector_name, target_lang_name, size_name):
    if image is None:
        return None
        
    # Handle filepath strings, dicts, or PIL Images
    if isinstance(image, str):
        input_path = image
    elif isinstance(image, dict) and "path" in image:
        input_path = image["path"]
    else:
        # Save input PIL image to temp file
        temp_dir = tempfile.gettempdir()
        input_path = os.path.join(temp_dir, "input_gradio.png")
        image.save(input_path, format="PNG")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        output_path = loop.run_until_complete(run_translation(input_path, translator_name, detector_name, target_lang_name, size_name))
        loop.close()
        return Image.open(output_path)
    except Exception as e:
        import traceback
        err_msg = f"Error during translation: {str(e)}\n\n{traceback.format_exc()}"
        print(err_msg)
        raise gr.Error(err_msg)

# Build Gradio UI
with gr.Blocks(title="Manga Image Translator (Molab Edition)") as demo:
    gr.Markdown("# 🏮 Manga Image Translator (Molab Blackwell Edition)")
    gr.Markdown("Translate Japanese/foreign manga pages directly in your browser with GPU-accelerated local execution.")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="pil", label="Upload Manga Page")
            
            with gr.Row():
                translator = gr.Dropdown(choices=TRANSLATORS_LIST, value="offline", label="Translator Engine")
                detector = gr.Dropdown(choices=DETECTORS_LIST, value="ctd", label="Text Detector")
                
            with gr.Row():
                target_lang = gr.Dropdown(choices=list(LANGUAGES_MAP.keys()), value="English", label="Target Language")
                size = gr.Dropdown(choices=SIZES_LIST, value="L", label="Processing Size (Text Detection Resolution)")
                
            btn = gr.Button("Translate Page", variant="primary")
            
        with gr.Column():
            output_img = gr.Image(type="pil", label="Translated Page")
            
    btn.click(
        fn=translate_wrapper,
        inputs=[input_img, translator, detector, target_lang, size],
        outputs=output_img
    )

if __name__ == "__main__":
    demo.launch(share=True, show_error=True)
