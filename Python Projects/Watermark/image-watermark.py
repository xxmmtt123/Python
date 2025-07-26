from tkinter import *
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont
import os

original_image = None
tk_img = None
watermarked_image = None

def add_watermark(img, text, size, position, color_hex, alpha=200, shadow_value=1.75, font_path=None):
    if not text:
        return img

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, size)
        else:
            font = ImageFont.truetype("Arial.ttf", size)
    except Exception as e:
        print(f"Failed to load font: {e}. Using default font.")
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if position == "Top-Left":
        x, y = 10, 10
    elif position == "Top-Right":
        x = img.width - text_width - 10
        y = 10
    elif position == "Bottom-Left":
        x = 10
        y = img.height - text_height - 20
    elif position == "Bottom-Right":
        x = img.width - text_width - 10
        y = img.height - text_height - 20
    elif position == "Center":
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
    else:
        x, y = 10, 10

    r, g, b = img_color_from_hex(color_hex)
    fill_color = (r, g, b, alpha)

    shadow_alpha = int(alpha * shadow_value)

    draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, shadow_alpha))
    draw.text((x, y), text, font=font, fill=fill_color)

    combined = Image.alpha_composite(img, txt_layer)
    return combined.convert('RGB')

def img_color_from_hex(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def load_fonts():
    fonts_dir = "fonts"
    fonts = {}
    if os.path.isdir(fonts_dir):
        for f in os.listdir(fonts_dir):
            if f.lower().endswith(".ttf"):
                fonts[f] = os.path.join(fonts_dir, f)
    return fonts


def display_resized_image():
    global tk_img, watermarked_image
    if original_image:
        max_width = image_frame.winfo_width()
        max_height = image_frame.winfo_height()

        if max_width < 10 or max_height < 10:
            window.after(100, display_resized_image)
            return

        img_copy = original_image.copy()
        img_copy.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        font_size = int(font_size_scale.get())

        selected_font = font_selector.get()
        font_path = font_paths.get(selected_font)

        alpha = transparency_scale.get()
        shadow_value = shadow_scale.get()

        watermarked_image = add_watermark(
            img_copy,
            watermark_text.get(),
            font_size,
            position_option.get(),
            watermark_color.get(),
            alpha=alpha,
            shadow_value=shadow_value,
            font_path=font_path
        )

        tk_img = ImageTk.PhotoImage(watermarked_image)
        image_label.config(image=tk_img, text="")
        image_label.image = tk_img

def upload_image():
    global original_image
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if file_path:
        img = Image.open(file_path)
        img = ImageOps.exif_transpose(img)
        original_image = img
        display_resized_image()

def choose_color():
    color_code = colorchooser.askcolor(title="Choose watermark color")
    if color_code[1] is not None:
        watermark_color.set(color_code[1])
        color_display.config(bg=color_code[1])
        display_resized_image()

def export_image():
    global watermarked_image
    if watermarked_image is None:
        messagebox.showwarning("No Image", "Please upload and watermark an image first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
        title="Save Image As"
    )
    if file_path:
        try:
            watermarked_image.save(file_path)
            messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save image:\n{e}")

window = Tk()
window.title("Watermark Image Editor")
window.geometry("900x700")

controls_frame = Frame(window)
controls_frame.pack(side=TOP, fill=X, padx=10, pady=10)

Label(controls_frame, text="Watermark Text:").grid(row=0, column=0, sticky=W)
watermark_text = StringVar(value="Your Watermark")
Entry(controls_frame, textvariable=watermark_text, width=40).grid(row=0, column=1, sticky=W, padx=5)

Label(controls_frame, text="Position:").grid(row=1, column=0, sticky=W)
position_option = StringVar(value="Bottom-Right")
positions = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"]
OptionMenu(controls_frame, position_option, *positions).grid(row=1, column=1, sticky=W, padx=5)

Label(controls_frame, text="Font size:").grid(row=2, column=0, sticky=W)
# font_size_entry = Entry(controls_frame, width=5)
# font_size_entry.grid(row=2, column=1, sticky=W, padx=5)
# font_size_entry.insert(0, "30")
font_size_scale = Scale(controls_frame, from_=8, to=50, orient=HORIZONTAL, length=150)
font_size_scale.set(30)  # default opacity
font_size_scale.grid(row=2, column=1, sticky=W, padx=5)

# Load fonts and create font selector dropdown
font_paths = load_fonts()
font_names = list(font_paths.keys())
if not font_names:
    font_names = ["Default"]
font_selector = StringVar(value=font_names[0])
Label(controls_frame, text="Font:").grid(row=3, column=0, sticky=W)
OptionMenu(controls_frame, font_selector, *font_names).grid(row=3, column=1, sticky=W, padx=5)

Label(controls_frame, text="Transparency:").grid(row=4, column=0, sticky=W)
transparency_scale = Scale(controls_frame, from_=50, to=255, orient=HORIZONTAL, length=150)
transparency_scale.set(200)  # default opacity
transparency_scale.grid(row=4, column=1, sticky=W, padx=5)

Label(controls_frame, text="Shadow:").grid(row=5, column=0, sticky=W)
shadow_scale = Scale(controls_frame, from_=0, to=2, resolution=0.05, orient=HORIZONTAL, length=150)
shadow_scale.set(1.75)
shadow_scale.grid(row=5, column=1, sticky=W, padx=5)

watermark_color = StringVar(value="#FFFFFF")
Button(controls_frame, text="Choose Color", command=choose_color).grid(row=6, column=0, pady=10)
color_display = Label(controls_frame, bg=watermark_color.get(), width=3)
color_display.grid(row=6, column=1, sticky=W)

upload_btn = Button(controls_frame, text="Upload Image", command=upload_image)
upload_btn.grid(row=7, column=0, columnspan=2, pady=10)

export_btn = Button(controls_frame, text="Export Image", command=export_image)
export_btn.grid(row=7, column=3, columnspan=2, pady=10)

image_frame = Frame(window)
image_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

image_label = Label(image_frame, text="No image uploaded", bg="lightgray")
image_label.pack(expand=True, fill=BOTH)

# Bind UI changes to update image preview
window.bind("<Configure>", lambda e: display_resized_image())
watermark_text.trace_add('write', lambda *args: display_resized_image())
position_option.trace_add('write', lambda *args: display_resized_image())
watermark_color.trace_add('write', lambda *args: display_resized_image())
font_size_scale.bind('<ButtonRelease-1>', lambda e: display_resized_image())
font_selector.trace_add('write', lambda *args: display_resized_image())
transparency_scale.bind('<ButtonRelease-1>', lambda e: display_resized_image())
shadow_scale.bind('<ButtonRelease-1>', lambda e: display_resized_image())

window.mainloop()
