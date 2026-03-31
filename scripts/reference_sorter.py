import os
import gradio as gr
from modules import scripts, script_callbacks

root_path = os.path.join(scripts.basedir(), "references")

def load_images(path):
    if not os.path.exists(path):
        return []
    return [(os.path.join(path, f), f) for f in os.listdir(path) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif'))]

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as reference_sorter:
        if not os.path.exists(root_path):
            gr.Markdown(f"### References Folder Missing\nPlease create a folder named `references` in your extension directory.")
            return (reference_sorter, "Reference Sorter", "reference_sorter"),

        with gr.Column(variant="panel"):
            with gr.Row():
                with gr.Column(scale=1): pass
                with gr.Column(scale=2):
                    refresh_btn = gr.Button("🔄 Refresh Images", variant="primary")
                    gr.HTML("<p style='text-align: center;'>*(Note: If you add <b>new folders</b>, you must reload the UI to generate the new tabs)*</p>")
                with gr.Column(scale=1): pass

        all_galleries = [] 

        categories = sorted([d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))])
        
        if not categories:
            gr.Markdown("The `references` folder is empty.")
        else:
            for category in categories:
                with gr.Tab(category):
                    cat_path = os.path.join(root_path, category)
                    sub_folders = sorted([d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))])
                    
                    if not sub_folders:
                        imgs = load_images(cat_path)
                        gal = gr.Gallery(value=imgs, show_label=False).style(grid=[5], height="auto")
                        all_galleries.append((cat_path, gal))
                    else:
                        for sub in sub_folders:
                            with gr.Tab(sub):
                                sub_path = os.path.join(cat_path, sub)
                                imgs = load_images(sub_path)
                                gal = gr.Gallery(
                                    value=imgs, 
                                    label=f"{category} / {sub}", 
                                    show_label=True,
                                    elem_id=f"style-gallery-{category}-{sub}"
                                ).style(grid=[6], height="auto")
                                all_galleries.append((sub_path, gal))

        def refresh_all_content():
            return [load_images(p) for p, _ in all_galleries]

        refresh_btn.click(fn=refresh_all_content, outputs=[g for _, g in all_galleries])

    return (reference_sorter, "Reference Sorter", "reference_sorter"),

script_callbacks.on_ui_tabs(on_ui_tabs)
