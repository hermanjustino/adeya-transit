import time
import sys
import signal
from mta_client import MTAClient
from display_renderer import DisplayRenderer
import config

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class SubwayApp:
    def __init__(self):
        self.client = MTAClient(api_key=config.MTA_API_KEY)
        self.renderer = DisplayRenderer(config.MATRIX_WIDTH, config.MATRIX_HEIGHT)
        self.last_good_data = None
        
        if HAS_HARDWARE:
            options = RGBMatrixOptions()
            options.rows = config.MATRIX_ROWS
            options.cols = config.MATRIX_COLS
            options.hardware_mapping = config.MATRIX_HARDWARE_MAPPING
            options.gpio_slowdown = config.GPIO_SLOWDOWN
            self.matrix = RGBMatrix(options = options)
        else:
            print("!!! Hardware not found. Running in VIRTUAL mode (saving preview.png).")
            self.matrix = None

    def run(self):
        print(f"Tracking {len(config.TRACKED_LINES)} lines...")
        
        while True:
            display_data = []
            
            for item in config.TRACKED_LINES:
                line = item['line']
                stop_id = item['stop_id']
                label = item['label']
                
                arrivals = None
                try:
                    arrivals = self.client.get_next_arrivals(stop_id, line)
                    # Cache successful fetches globally (per line)
                    if arrivals:
                        if not hasattr(self, 'cache'): self.cache = {}
                        self.cache[f"{line}_{stop_id}"] = arrivals
                except Exception as e:
                    print(f"Error fetching {line} @ {stop_id}: {e}")
                    if hasattr(self, 'cache'):
                        arrivals = self.cache.get(f"{line}_{stop_id}")

                display_data.append({
                    'line': line,
                    'arrivals': arrivals
                })

            # 3. Render
            image = self.renderer.render_multi_lines(display_data)

            # 4. Display or Save
            if HAS_HARDWARE:
                self.matrix.SetImage(image.convert('RGB'))
            else:
                self.renderer.save_preview(image)

            print(f"Updated at {time.strftime('%H:%M:%S')}. Sleeping {config.REFRESH_INTERVAL}s")
            time.sleep(config.REFRESH_INTERVAL)

def handle_signal(sig, frame):
    print("\nShutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    app = SubwayApp()
    app.run()
