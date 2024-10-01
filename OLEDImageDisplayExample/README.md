# Image2Array - OLED Display Example

This project demonstrates how to display a custom image on an OLED screen connected to an Arduino Uno using the PlatformIO environment. The project includes example code that displays both text and a bitmap image stored in program memory (PROGMEM) on a 128x64 OLED display.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Wiring](#wiring)
- [Example Code](#example-code)
- [Credits](#credits)

## Requirements

To run this project, you will need the following hardware and software:

### Hardware

- Arduino Uno or compatible board
- 128x64 OLED display (using SSD1306 driver and I2C interface)
- Jumper wires

### Software

- [PlatformIO](https://platformio.org/) installed (can be integrated into VS Code)
- PlatformIO packages:
  - Framework: Arduino
  - Libraries: 
    - Adafruit SSD1306 
    - Adafruit GFX

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GoldenxSun/Image2Array.git
   ```

2. Open the project folder in [PlatformIO IDE](https://platformio.org/):

   ```bash
   cd Image2Array/OLEDImageDisplayExample
   ```

3. PlatformIO will automatically detect the required libraries based on the `platformio.ini` file and install them when you build the project.

4. Connect your Arduino Uno to your computer.

## Usage

### Uploading the Code

1. Open the project in PlatformIO.
2. Ensure your board is selected (Arduino Uno by default in `platformio.ini`).
3. Build the project by clicking on the **Build** button in the toolbar or using the shortcut `Ctrl + Alt + B`.
4. Once the build completes successfully, upload the code to your Arduino Uno by clicking the **Upload** button or using the shortcut `Ctrl + Alt + U`.

### Expected Behavior

After uploading the code, the OLED display will first show the text "Hello, World!" centered on the screen for 2 seconds, followed by the display of a custom bitmap image defined in the code as a PROGMEM array.

## Wiring

To connect your Arduino Uno to the OLED display, use the following wiring setup (I2C connection):

| OLED Pin  | Arduino Uno Pin |
|-----------|-----------------|
| VCC       | 5V              |
| GND       | GND             |
| SDA       | A4 (SDA)        |
| SCL       | A5 (SCL)        |

## Example Code

Here’s a snippet of the key functionality in `main.cpp`:

```cpp
#define BITMAP_WIDTH 64
#define BITMAP_HEIGHT 64

void drawBitmap(const uint8_t *bitmap, uint8_t width, uint8_t height, bool vertical = true, bool horizontal = true) {
  oled.clearDisplay();
  oled.drawBitmap((oled.width() - width) / 2, (oled.height() - height) / 2, bitmap, width, height, WHITE);
  oled.display();
}

void setup() {
  
  drawBitmap(example, BITMAP_WIDTH, BITMAP_HEIGHT);
}
```

## Adding Your Own Images

If you'd like to display your own image:

1. Convert your image to a bitmap array using an image-to-array converter.
2. Replace the `example[]` array in the code with your bitmap array.
3. Adjust the `BITMAP_WIDTH` and `BITMAP_HEIGHT` macros to match the dimensions of your image.

## Credits

This project uses the following libraries:

- [Adafruit GFX Library](https://github.com/adafruit/Adafruit-GFX-Library)
- [Adafruit SSD1306 Library](https://github.com/adafruit/Adafruit_SSD1306)

Special thanks to the PlatformIO and Arduino communities for their support.

### Key Sections:

- **Installation:** Guides users through the process of cloning the repository and building the project using PlatformIO.
- **Usage:** Includes instructions on how to upload the code to the Arduino Uno and what to expect.
- **Wiring:** Provides a simple table for connecting the OLED to the Arduino Uno using I2C.
- **Example Code:** A snippet showcasing the most important parts of the project.
- **Adding Your Own Images:** Explains how to replace the provided bitmap with your own image. 


## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).