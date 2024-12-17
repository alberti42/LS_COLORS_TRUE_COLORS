# Andrea Alberti, 2024

from ntpath import isdir
import re
import sys

# ANSI 256-color to RGB mapping (example completed for all 256 values)
ansi_256_to_rgb = {
    **{i: (0, 0, 0) for i in range(16)},  # Placeholder for the first 16 colors
    **{16 + 36 * r + 6 * g + b: (r * 51, g * 51, b * 51)
       for r in range(6) for g in range(6) for b in range(6)},  # 216-color cube
    **{232 + i: (8 + i * 10, 8 + i * 10, 8 + i * 10) for i in range(24)},  # Grayscale ramp
}

# Regular ANSI 16-color mapping (non-bright)
ansi16_regular = {
    30: (0, 0, 0),       # Black
    31: (128, 0, 0),     # Red
    32: (0, 128, 0),     # Green
    33: (128, 128, 0),   # Yellow
    34: (0, 0, 128),     # Blue
    35: (128, 0, 128),   # Magenta
    36: (0, 128, 128),   # Cyan
    37: (192, 192, 192)  # White
}

# Bright ANSI 16-color mapping
ansi16_bright = {
    30: (128, 128, 128), # Bright Black
    31: (255, 0, 0),     # Bright Red
    32: (0, 255, 0),     # Bright Green
    33: (255, 255, 0),   # Bright Yellow
    34: (0, 0, 255),     # Bright Blue
    35: (255, 0, 255),   # Bright Magenta
    36: (0, 255, 255),   # Bright Cyan
    37: (255, 255, 255)  # Bright White
}
def convert_ansi_to_rgb(colors):
    """
    Converts ANSI color specifications to true color where applicable.
    Handles:
      - Regular and bright ANSI 16 colors (30–37, 40–47 with optional 1 modifier).
      - Extended 256 colors (<code>;5;<n>).
      - True color (<code>;2;<R>;<G>;<B>).
      - Preserves text attributes (e.g., 0, 4, 5).
    """
    components = colors.split(';')
    result = []

    i = 0
    while i < len(components):
        try:
            code = int(components[i])

            # Bright modifier "1" followed by a standard color
            if code == 1 and i + 1 < len(components):
                next_code = int(components[i + 1])
                if 30 <= next_code <= 37:  # Bright foreground
                    r, g, b = ansi16_bright[next_code]
                    result.append(f"38;2;{r};{g};{b}")
                    i += 2
                    continue
                elif 40 <= next_code <= 47:  # Bright background
                    r, g, b = ansi16_bright[next_code - 10]
                    result.append(f"48;2;{r};{g};{b}")
                    i += 2
                    continue

            # Regular ANSI 16 foreground colors (30–37)
            if 30 <= code <= 37:
                r, g, b = ansi16_regular[code]
                result.append(f"38;2;{r};{g};{b}")
                i += 1
                continue

            # Regular ANSI 16 background colors (40–47)
            if 40 <= code <= 47:
                r, g, b = ansi16_regular[code - 10]  # Background maps to foreground equivalent
                result.append(f"48;2;{r};{g};{b}")
                i += 1
                continue

            # Extended 256 colors (38;5;<n>)
            if code == 38 and components[i + 1] == "5":
                ansi_code = int(components[i + 2])
                r, g, b = ansi_256_to_rgb.get(ansi_code, (255, 255, 255))
                result.append(f"38;2;{r};{g};{b}")
                i += 3
                continue

            # True color (38;2;<R>;<G>;<B>)
            if code == 38 and components[i + 1] == "2":
                result.extend(components[i:i + 5])
                i += 5
                continue

            # Pass through unrecognized codes
            result.append(components[i])
            i += 1

        except (ValueError, IndexError):
            result.append(components[i])
            i += 1

    return ';'.join(result)


def process_line(line):
    """
    Processes a single line of the table, preserving comments and converting colors.
    Handles:
      - `name`: The file type or attribute (e.g., "BLK", "NORMAL").
      - `colors`: The ANSI color code or sequence.
      - `comment`: Comments at the end of the line (e.g., "# core").
    """
    # Match the line format using regex
    match = re.match(r'^\s*([^#\s]+\s+)([^#\s]+)(\s*)(#.*)?', line)
    if not match:
        return line  # Return the line unchanged if it doesn't match the expected format

    name, colors, spaces, comment = match.groups()

    # Process the color codes (convert ANSI to true color if applicable)
    processed_colors = convert_ansi_to_rgb(colors)

    # Rebuild and return the processed line
    return f"{name}{processed_colors}{spaces}{comment}"

def process_table(input_text: str):
    """
    Processes the entire table and converts all ANSI colors to true colors.
    """
    lines = input_text.splitlines()
    processed_lines = [process_line(line) for line in lines]
    return '\n'.join(processed_lines)

def main(filepath):
    """
    Reads a file, processes its content, and prints the result.
    """
    try:
        with open(filepath, 'r') as file:
            input_text = file.read()
        output_text = process_table(input_text)
        print(output_text)
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    main(filepath)
