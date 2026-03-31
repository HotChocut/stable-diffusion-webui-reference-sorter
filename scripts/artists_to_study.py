import os
import gradio as gr
from modules import scripts, script_callbacks

# Safely build the base path
root_path = os.path.join(scripts.basedir(), "ats", "thumbnail")

def get_images(target_path):
    images = []
    if not os.path.exists(target_path):
        return images
        
    for file_name in os.listdir(target_path):
        final_path = os.path.join(target_path, file_name)
        # Ensure we only grab files, ignoring any accidental nested folders
        if os.path.isfile(final_path):
            try:
                images.append((final_path, file_name))
            except Exception as e:
                print(f"Error loading {final_path}: {e}")
    return images

def on_ui_tabs():     
    with gr.Blocks() as artists_to_study:
        # Dynamically fetch the prompt paths (first-level folders)
        if os.path.exists(root_path):
            prompt_paths = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        else:
            prompt_paths = []

        if not prompt_paths:
            gr.Markdown(f"No folders found in `{root_path}`. Add your folders to see them here.")
        else:
            for prompt_path in prompt_paths:
                with gr.Tab(prompt_path):
                    prompt_full_path = os.path.join(root_path, prompt_path)
                    
                    # Dynamically fetch the jpg paths (second-level folders) for this specific prompt
                    jpg_paths = [d for d in os.listdir(prompt_full_path) if os.path.isdir(os.path.join(prompt_full_path, d))]
                    
                    if not jpg_paths:
                        gr.Markdown(f"No subfolders found in `{prompt_full_path}`.")
                    else:
                        for jpg_path in jpg_paths:
                            with gr.Tab(jpg_path):
                                input_path = os.path.join(prompt_full_path, jpg_path)
                                gallery_label = f"{prompt_path}-{jpg_path}"
                                
                                txt = gr.Textbox(value=input_path, interactive=False, show_label=False, visible=True)
                                btn = gr.Button(value="Get Images", elem_id=f"ats-button-{prompt_path}-{jpg_path}")
                                gallery = gr.Gallery(label=gallery_label, show_label=True, elem_id=f"ats-gallery-{prompt_path}-{jpg_path}").style(grid=[5], height="auto")
                                
                                btn.click(get_images, txt, gallery)
                                
        gr.HTML(
            """
                <p style="font-size: 12px" align="right">artists to study extension by camenduru | <a href="https://github.com/camenduru" target="_blank">github</a> | <a href="https://twitter.com/camenduru" target="_blank">twitter</a> | <a href="https://www.youtube.com/channel/UCdk3FaULpDK8kRCPG5jbgHQ" target="_blank">youtube</a> | <a href="https://artiststostudy.pages.dev" target="_blank">hi-res images</a><br />All images generated with CompVis/stable-diffusion-v1-4 + <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/artists.csv" target="_blank">artists.csv</a> | License: Attribution 4.0 International (CC BY 4.0)</p>
            """
        )
    return (artists_to_study, "Artists To Study", "artists_to_study"),

script_callbacks.on_ui_tabs(on_ui_tabs)
