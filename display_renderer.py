from PIL import Image, ImageDraw, ImageFont
import os

class DisplayRenderer:
    """
    Handles rendering the 64x32 virtual matrix with circular line icons.
    """
    def __init__(self, width=64, height=32, font_path=None):
        self.width = width
        self.height = height
        
        # MTA Colors
        self.line_colors = {
            '1': (238, 53, 46),   # Red
            '2': (238, 53, 46),
            '3': (238, 53, 46),
            'B': (255, 99, 25),   # Orange
            'D': (255, 99, 25),
            'F': (255, 99, 25),
            'M': (255, 99, 25),
            'A': (0, 57, 166),    # Blue
            'C': (0, 57, 166),
            'E': (0, 57, 166),
            'L': (160, 160, 160), # Grey
            'G': (110, 199, 69),  # Lime
        }

        # ImageFont.load_default() renders a tiny ~6x10px bitmap glyph that's
        # thin and hard to read on a 3mm-pitch panel viewed up close. Prefer a
        # bold TTF at a size tuned for 32px-tall rows; fall back gracefully if
        # no TTF is available (e.g. a minimal Raspberry Pi OS Lite install
        # without fonts-dejavu-core).
        ttf_candidates = [
            font_path,
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ]
        self.font = None
        for path in ttf_candidates:
            if path and os.path.exists(path):
                try:
                    self.font = ImageFont.truetype(path, 8)
                    break
                except Exception:
                    continue
        if self.font is None:
            print("!!! No TTF font found, falling back to tiny built-in bitmap font. "
                  "Run `sudo apt-get install fonts-dejavu-core` for legible text.")
            self.font = ImageFont.load_default()

    def render_multi_lines(self, line_data):
        """
        line_data: List of dicts: {'line': '1', 'arrivals': [min1, min2]}
        """
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)

        # Space out 3 lines evenly on 32px height
        y_step = 10
        y_start = 1

        for i, data in enumerate(line_data[:3]):
            y = y_start + (i * y_step)
            line = data['line']
            arrivals = data.get('arrivals', [])

            # 1. Draw Circle Icon
            color = self.line_colors.get(line, (255, 255, 255))
            # Circle bounding box [x0, y0, x1, y1]
            draw.ellipse([1, y, 9, y+8], fill=color)
            
            # Center the text inside the circle
            text_x = 3 if line in ['1', 'L', 'G'] else 2 # Slight adjustment for wider letters
            draw.text((text_x, y-1), line, font=self.font, fill="white")

            # 2. Draw arrival times
            if not arrivals:
                draw.text((15, y), "No data", font=self.font, fill=(100, 100, 100))
            else:
                # Format: "2, 12 min"
                time_strings = [f"{m}" for m in arrivals[:2]]
                time_text = ", ".join(time_strings) + " min"
                
                # Check urgency for color
                text_color = (0, 255, 0) # Green
                if arrivals[0] < 2: text_color = (255, 50, 50) # Red
                elif arrivals[0] < 5: text_color = (255, 165, 0) # Orange
                
                draw.text((15, y), time_text, font=self.font, fill=text_color)

        return img

    def save_preview(self, image, filename="preview.png"):
        preview = image.resize((self.width * 10, self.height * 10), resample=Image.NEAREST)
        preview.save(filename)
        print(f"Saved preview to {filename}")

if __name__ == "__main__":
    renderer = DisplayRenderer()
    sample = [
        {'line': '1', 'arrivals': [2, 12]},
        {'line': 'B', 'arrivals': [5, 15]},
        {'line': 'C', 'arrivals': [8, 18]},
    ]
    img = renderer.render_multi_lines(sample)
    renderer.save_preview(img)
