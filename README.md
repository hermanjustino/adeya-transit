# Adeya Transit: Real-Time Subway LED Display

A custom real-time subway arrival display for a 64x32 RGB LED Matrix, designed as a standalone appliance.

## Hardware Components
- **Raspberry Pi Zero 2 W**
- **HUB75 64x32 RGB LED Matrix** (3mm pitch)
- **Adafruit RGB Matrix Bonnet**
- **5V 4A+ Power Supply** (Dedicated for the matrix)
- **Raspberry Pi OS Lite**

## Software Setup

### 1. Install System Dependencies
On your Raspberry Pi, run:
```bash
sudo apt-get update
sudo apt-get install -y git python3-pip python3-pil python3-dev
```

### 2. Install Hardware Library
The display uses the [hzeller/rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.
```bash
curl -sSL https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh | bash
```
*Note: During installation, select "Adafruit RGB Matrix Bonnet" and "Quality (disable sound)" when prompted.*

### 3. Clone and Setup this Project
```bash
git clone https://github.com/hermanjustino/adeya-transit.git
cd adeya-transit

# Install dependencies system-wide (NOT in a venv).
# The rgb-matrix.sh installer above binds the `rgbmatrix` C-extension to
# system python3. If you instead `pip install` into a venv, main.py's
# `import rgbmatrix` will fail and it will silently fall back to virtual
# mode (saving preview.png) instead of driving the real panel.
pip3 install -r requirements.txt --break-system-packages
```
*(`--break-system-packages` is needed on Raspberry Pi OS Bookworm's
PEP 668-managed Python; omit it on older Raspberry Pi OS versions.)*

A venv is still fine for developing off-Pi, where there's no `rgbmatrix`
module to worry about and the app just runs in virtual mode.

### 4. Configuration
Edit `config.py` to set your desired station IDs. Out of the box it tracks
the 1/B/C trains, Uptown, at 59 St-Columbus Circle.
- Find your Stop ID in the [MTA Stop List](https://data.ny.gov/Transportation/MTA-Subway-Stops/u855-bhbe).
- Stop IDs end in `N` or `S` for direction (e.g. `125N` = Uptown 1 train at 59 St-Columbus Circle).
- `MTA_API_KEY` can be left as `None` — MTA's realtime feeds no longer require one.

### 5. Run manually
```bash
sudo python3 main.py
```
*(Sudo is required for GPIO access by the hardware library)*

## Auto-Start on Boot
To make the display start automatically on power-up:

1. Copy the service file:
   ```bash
   sudo cp subway.service /etc/systemd/system/subway.service
   ```
2. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable subway.service
   sudo systemctl start subway.service
   ```

## Key Files
- `main.py`: Main application loop.
- `mta_client.py`: Fetches real-time GTFS-RT data.
- `display_renderer.py`: Handles 64x32 layout and color coding.
- `config.py`: User settings (Stations, Refresh rate).