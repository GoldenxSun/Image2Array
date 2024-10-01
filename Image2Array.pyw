import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import pyperclip
import os


class Image2Array:
    def __init__(self, root):
        """Initialize the application, setting up the GUI and default state."""
        self.root = root
        self.root.title("Image to Bitmap and Array Converter")

        # Dark mode flag
        self.dark_mode = True
        self.current_image = None
        self.progmem_array_global = None
        self.image_path = None

        # Set up the interface
        self.setup_gui()
        self.apply_dark_mode()

    def setup_gui(self):
        """Sets up the main GUI components."""
        # Main frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20, padx=20)

        # Output name label and entry
        self.output_name_label = tk.Label(self.frame, text="Output Name:")
        self.output_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.output_name_entry = tk.Entry(self.frame)
        self.output_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Height entry
        self.height_label = tk.Label(self.frame, text="Height (Pixels):")
        self.height_label.grid(row=1, column=0, padx=10, pady=10)

        self.height_entry = tk.Entry(self.frame)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        # Width entry
        self.width_label = tk.Label(self.frame, text="Width (Pixels):")
        self.width_label.grid(row=2, column=0, padx=10, pady=10)

        self.width_entry = tk.Entry(self.frame)
        self.width_entry.grid(row=2, column=1, padx=10, pady=10)

        # Dimension label
        self.dimension_label = tk.Label(self.frame, text="Calculated Dimensions: ")
        self.dimension_label.grid(row=3, columnspan=2, pady=10)

        # Process button
        self.process_button = tk.Button(self.frame, text="Process Image", command=self.process_image)
        self.process_button.grid(row=4, columnspan=2, pady=10)

        # Clipboard button
        self.clipboard_button = tk.Button(self.frame, text="Copy Array to Clipboard", state=tk.DISABLED, command=self.copy_to_clipboard)
        self.clipboard_button.grid(row=5, columnspan=2, pady=10)

        # Preview frame
        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(pady=20)

        self.preview_label = tk.Label(self.preview_frame)
        self.preview_label.pack()

        # Image controls
        self.image_controls = tk.Frame(self.root)
        self.image_controls.pack(pady=10)

        self.open_button = tk.Button(self.image_controls, text="Open Image", command=self.open_image)
        self.open_button.grid(row=0, column=0, padx=10)

        self.rotate_button = tk.Button(self.image_controls, text="Rotate", command=self.rotate_image)
        self.rotate_button.grid(row=0, column=1, padx=10)

        self.flip_button = tk.Button(self.image_controls, text="Flip", command=self.flip_image)
        self.flip_button.grid(row=0, column=2, padx=10)

        self.crop_button = tk.Button(self.image_controls, text="Crop", command=self.crop_image)
        self.crop_button.grid(row=0, column=3, padx=10)

        # Invert color button
        self.invert_button = tk.Button(self.image_controls, text="Invert Colors", command=self.invert_colors)
        self.invert_button.grid(row=0, column=4, padx=10)

        # Mode toggle button
        self.mode_button = tk.Button(self.root, text="Switch to Light Mode", command=self.toggle_mode)
        self.mode_button.pack(pady=10)

    def convert_to_bitmap(self, image_path, output_path):
        """Converts an image to bitmap format."""
        img = Image.open(image_path)
        img.save(output_path)

    def bitmap_to_progmem(self, bitmap_path, height=None, width=None):
        """Converts a bitmap to a PROGMEM array for Arduino OLED displays."""
        img = Image.open(bitmap_path).convert('1')  # Convert to 1-bit pixels

        if height is not None:
            aspect_ratio = img.width / img.height
            width = int(height * aspect_ratio)
        elif width is not None:
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)
        else:
            raise ValueError("Either height or width must be specified.")

        img = img.resize((width, height), Image.LANCZOS)

        binary_array = []
        for y in range(height):
            for x in range(0, width, 8):
                byte = 0
                for bit in range(8):
                    if x + bit < width:
                        pixel = img.getpixel((x + bit, y))
                        if pixel == 0:
                            byte |= (1 << (7 - bit))
                binary_array.append(f'0b{byte:08b}')

        filename = os.path.splitext(os.path.basename(bitmap_path))[0]
        progmem_array = f'static const unsigned char PROGMEM {filename}[] = {{\n'
        for i in range(0, len(binary_array), 8):
            line = ', '.join(binary_array[i:i + 8]) + ','
            progmem_array += f'  {line}\n'
        progmem_array += '};'

        return progmem_array, width, height

    def save_array_to_file(self, array, output_path):
        """Saves the PROGMEM array to a text file."""
        with open(output_path, 'w') as f:
            f.write(array)

    def copy_to_clipboard(self):
        """Copies the generated PROGMEM array to the clipboard."""
        pyperclip.copy(self.progmem_array_global)
        messagebox.showinfo("Copied", "The array has been copied to the clipboard.")

    def process_image(self):
        """Processes the selected image, converts it to a bitmap, and generates the PROGMEM array."""
        if self.current_image:
            try:
                output_name = self.output_name_entry.get()
                if not output_name:
                    output_name = os.path.splitext(os.path.basename(self.image_path))[0]

                output_bitmap = f"{output_name}.bmp"
                self.current_image.save(output_bitmap)

                height = self.height_entry.get()
                width = self.width_entry.get()

                if height:
                    height = int(height)
                    progmem_array, calculated_width, calculated_height = self.bitmap_to_progmem(output_bitmap, height=height)
                elif width:
                    width = int(width)
                    progmem_array, calculated_width, calculated_height = self.bitmap_to_progmem(output_bitmap, width=width)
                else:
                    messagebox.showwarning("Input Warning", "Please provide either height or width.")
                    return

                output_txt = f"{output_name}.txt"
                self.save_array_to_file(progmem_array, output_txt)

                self.dimension_label.config(text=f"Calculated Dimensions: {calculated_width} x {calculated_height} pixels")
                self.clipboard_button.config(state=tk.NORMAL)

                self.progmem_array_global = progmem_array

            except Exception as e:
                messagebox.showerror("Error", f"Processing error: {str(e)}")
        else:
            messagebox.showwarning("Cancelled", "No file selected.")

    def load_image_preview(self):
        """Loads and displays the image preview in the application."""
        img_bw = self.current_image.convert('L')  # Convert to black and white
        img_tk = ImageTk.PhotoImage(img_bw)
        self.preview_label.config(image=img_tk)
        self.preview_label.image = img_tk

    def open_image(self):
        """Opens an image file and loads it into the application."""
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if self.image_path:
            self.current_image = Image.open(self.image_path)
            self.output_name_entry.delete(0, tk.END)
            self.output_name_entry.insert(0, os.path.splitext(os.path.basename(self.image_path))[0])
            self.load_image_preview()

    def rotate_image(self):
        """Rotates the current image by 90 degrees."""
        if self.current_image:
            self.current_image = self.current_image.rotate(-90, expand=True)
            self.load_image_preview()

    def flip_image(self):
        """Flips the current image horizontally."""
        if self.current_image:
            self.current_image = ImageOps.mirror(self.current_image)
            self.load_image_preview()

    def crop_image(self):
        """Crops the current image by 20%."""
        if self.current_image:
            width, height = self.current_image.size
            new_width = int(width * 0.8)
            new_height = int(height * 0.8)
            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2
            self.current_image = self.current_image.crop((left, top, right, bottom))
            self.load_image_preview()

    def invert_colors(self):
        """Inverts the colors of the current image."""
        if self.current_image:
            self.current_image = ImageOps.invert(self.current_image.convert('RGB'))
            self.load_image_preview()

    def toggle_mode(self):
        """Toggles between dark mode and light mode."""
        if self.dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()

    def apply_dark_mode(self):
        """Applies the dark mode to the interface."""
        self.root.configure(bg="#2E2E2E")
        self.update_widget_colors(bg="#2E2E2E", fg="#FFFFFF", entry_bg="#3E3E3E", entry_fg="#FFFFFF")
        self.mode_button.config(text="Switch to Light Mode", bg="#4A4A4A", fg="#FFFFFF")
        self.dark_mode = True

    def apply_light_mode(self):
        """Applies the light mode to the interface."""
        self.root.configure(bg="#F0F0F0")
        self.update_widget_colors(bg="#F0F0F0", fg="#000000", entry_bg="#FFFFFF", entry_fg="#000000")
        self.mode_button.config(text="Switch to Dark Mode", bg="#D0D0D0", fg="#000000")
        self.dark_mode = False

    def update_widget_colors(self, bg, fg, entry_bg, entry_fg):
        """Updates the colors of the widgets based on the current mode."""
        widgets = [self.frame, self.preview_frame, self.image_controls]
        labels = [self.output_name_label, self.height_label, self.width_label, self.dimension_label]
        entries = [self.output_name_entry, self.height_entry, self.width_entry]
        buttons = [self.process_button, self.clipboard_button, self.open_button, self.rotate_button, self.flip_button, self.crop_button, self.invert_button]

        for widget in widgets:
            widget.config(bg=bg)

        for label in labels:
            label.config(bg=bg, fg=fg)

        for entry in entries:
            entry.config(bg=entry_bg, fg=entry_fg)

        for button in buttons:
            button.config(bg=bg, fg=fg)


if __name__ == "__main__":
    root = tk.Tk()
    app = Image2Array(root)
    root.mainloop()
