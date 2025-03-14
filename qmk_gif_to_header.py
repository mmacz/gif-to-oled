import argparse
from pathlib import Path
from PIL import Image, ImageSequence

def gif_to_qmk_header(gif_path: Path, threshold: int, invert: bool):
    gif_path = gif_path.resolve()
    output_header = gif_path.with_suffix(".h")

    with Image.open(gif_path) as img:
        frames = [frame.copy().convert('L').point(lambda p: 0 if (p > threshold) ^ invert else 1, '1') for frame in ImageSequence.Iterator(img)]
        
        if not frames:
            raise ValueError("No frames found in the GIF.")
        
        frames = [frame.resize((128, 32), Image.Resampling.LANCZOS) if frame.size != (128, 32) else frame for frame in frames]
        
        raw_frames = []
        for frame in frames:
            pixels = list(frame.getdata())
            frame_bytes = bytearray()
            
            for page in range(4):  
                for x in range(128):  
                    byte = 0
                    for bit in range(8):
                        y = page * 8 + bit
                        pixel_value = pixels[y * 128 + x]
                        if pixel_value == 1:  
                            byte |= (1 << bit)
                    frame_bytes.append(byte)
            raw_frames.append(frame_bytes)
        
        with output_header.open('w') as f:
            f.write("#pragma once\n\n")
            f.write("#include <stdint.h>\n#include \"oled_driver.h\"\n#include \"timer.h\"\n\n")
            f.write(f"#define ANIM_FRAMES {len(frames)}\n")
            f.write(f"#define ANIM_FRAME_SIZE {len(raw_frames[0])}\n")
            f.write(f"#define ANIM_DATA_SIZE {len(raw_frames) * len(raw_frames[0])}\n\n")
            
            f.write("void oled_update_animation(void);\n")
            f.write("void oled_init_animation(void);\n\n")
            
            f.write("const char oled_animation[ANIM_FRAMES][ANIM_FRAME_SIZE] = {\n")
            for frame_bytes in raw_frames:
                f.write("    {\n")
                for i in range(0, len(frame_bytes), 16):
                    f.write("        " + ", ".join(f"0x{b:02X}" for b in frame_bytes[i:i+16]) + ",\n")
                f.write("    },\n")
            f.write("};\n\n")
            
            f.write("uint32_t last_frame_time = 0;\n")
            f.write("uint8_t current_frame = 0;\n\n")
            
            f.write("void oled_update_animation(void) {\n")
            f.write("    uint32_t now = timer_read32();\n")
            f.write("    if (now - last_frame_time < 100) {\n")
            f.write("        return;\n")
            f.write("    }\n")
            f.write("    last_frame_time = now;\n\n")
            f.write("    oled_clear();\n")
            f.write("    oled_write_raw(oled_animation[current_frame], ANIM_FRAME_SIZE);\n\n")
            f.write("    current_frame = (current_frame + 1) % ANIM_FRAMES;\n")
            f.write("}\n\n")
            
            f.write("void oled_init_animation(void) {\n")
            f.write("    oled_clear();\n")
            f.write("    last_frame_time = timer_read32();\n")
            f.write("    current_frame = 0;\n")
            f.write("}\n")
    
    print(f"Header file '{output_header}' generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an animated GIF into a QMK-compatible OLED header file.")
    parser.add_argument("--input", type=Path, help="Path to the input GIF file.")
    parser.add_argument("--threshold", type=int, default=128, help="Threshold (0-255) to determine white vs black pixels.")
    parser.add_argument("--invert", action="store_true", help="Invert colors in the generated image")

    args = parser.parse_args()
    
    gif_to_qmk_header(args.input, args.threshold, args.invert)
