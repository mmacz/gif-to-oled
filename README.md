# GIF to QMK OLED Header Converter

This repository contains a Python script that converts an animated GIF into a QMK-compatible OLED header file. The generated header file can be used to display animations on an OLED screen in a QMK-powered keyboard.

## Features
- Converts animated GIFs into a format compatible with QMK's OLED display.
- Automatically resizes frames to fit a 128x32 pixel OLED display.
- Allows threshold-based black-and-white conversion.
- Option to invert colors.
- Outputs a `.h` header file containing animation data for use in QMK firmware.

## Requirements

Ensure you have Python installed along with the following dependencies:

```sh
pip install pillow
```

## Usage

Run the script using the following command:

```sh
python gif_to_qmk.py --input <path-to-gif> [--threshold <0-255>] [--invert]
```

### Arguments:
- `--input`: Path to the input GIF file.
- `--threshold`: Threshold (0-255) to determine white vs black pixels (default: 128).
- `--invert`: Optional flag to invert the colors.

### Example Usage

```sh
python gif_to_qmk.py --input animation.gif --threshold 150 --invert
```

This will process `animation.gif` and generate `animation.h` with the animation data.

## Output

The generated `.h` file includes:
- Animation frame data stored as a 2D byte array.
- OLED animation update functions.
- Definitions for animation frame count and size.

Example output structure:

```c
#pragma once

#include <stdint.h>
#include "oled_driver.h"
#include "timer.h"

#define ANIM_FRAMES X
#define ANIM_FRAME_SIZE Y
#define ANIM_DATA_SIZE Z

void oled_update_animation(void);
void oled_init_animation(void);

const char oled_animation[ANIM_FRAMES][ANIM_FRAME_SIZE] = { ... };
```

## Integrating with QMK

1. Copy the generated `.h` file into your QMK firmware source directory.
2. Include the header in your `keymap.c` file:
   ```c
   #include "animation.h"
   ```
3. Initialize the animation in your OLED initialization function in your `oled_init_user()` function to initialize the framework:
   ```c
   oled_init_animation();
   ```
4. Call `oled_update_animation();` in your `oled_task_user()` function to update the frames.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to open issues or submit pull requests to improve the script!

