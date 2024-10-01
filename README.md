# Image to Bitmap and PROGMEM Array Converter

This application allows you to convert an image into a bitmap format and then generate a PROGMEM array for Arduino OLED displays. The app features a user-friendly dark mode interface, with the option to switch to light mode. It also provides basic image editing capabilities such as rotating, flipping, and cropping the image.

## Features

- **Image Selection**: Supports `.png`, `.jpg`, `.jpeg`, and `.bmp` image formats.
- **Bitmap Conversion**: Converts the selected image into a bitmap format.
- **PROGMEM Array Generation**: Generates the PROGMEM array for Arduino OLED displays based on the specified height or width.
- **Copy to Clipboard**: Easily copy the generated PROGMEM array to the clipboard.
- **Display Calculated Dimensions**: Displays the calculated width and height of the bitmap image.
- **Image Manipulation**: Allows rotating, flipping, cropping and inverting the image before conversion.
- **Output File Name**: Customizable output name, with the default being the selected image's file name.
- **Dark/Light Mode**: Toggle between dark and light mode for the application interface.

## Prerequisites

To run this application, you will need Python 3.x and the following libraries:

- `Pillow` (for image processing)
- `pyperclip` (for copying the PROGMEM array to the clipboard)
- `tkinter` (for the graphical user interface)

## Installation

Make sure you have `pip` installed, and then run the following command to install the necessary libraries:

```bash
pip install -r requirements.txt
```

## How to Use

1. **Open the Application**: Run the Python script.
2. **Select an Image**: Use the "Open Image" button to select an image from your file system.
3. **Edit the Image (Optional)**: Use the rotate, flip, crop and invert buttons to modify the image as needed.
4. **Set Dimensions**: Specify either the height or width of the desired output. The other dimension will be automatically calculated.
5. **Output File Name (Optional)**: You can enter a custom output name, or leave it as the default (the original file name).
6. **Process the Image**: Click the "Process Image" button to generate the bitmap and PROGMEM array.
7. **Copy to Clipboard**: Once processed, you can copy the generated array to the clipboard for use in your Arduino project.
8. **Dark/Light Mode**: Toggle between dark and light mode using the mode button.

## Example Workflow

1. **Select an Image**: Choose an image (e.g., [`example.jpg`](assets/example.jpg)) to be converted.
2. **Edit the Image**: Rotate, flip or invert the image as necessary using the image manipulation buttons.
3. **Set Height or Width**: Specify a height or width, such as 64 pixels for an OLED display.
4. **Process**: Click "Process Image" to convert it into a bitmap.
5. **Copy to Clipboard**: After conversion, click "Copy Array to Clipboard" to use the generated PROGMEM array in your Arduino code.

## Image Manipulation Features

- **Rotate**: Rotates the image 90 degrees counterclockwise.
- **Flip**: Flips the image horizontally.
- **Crop**: Crops the image by 20% from each side.
- **Invert**: Inverts the colors of the image.

## Example Output

For an image named `example.jpg` with a height of 64 pixels, the generated PROGMEM array will look like this:

```cpp
static const unsigned char PROGMEM example[] = {
  0b11111111, 0b00000000, 0b11111111, // Example output
  // ... more binary data
};
```

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).