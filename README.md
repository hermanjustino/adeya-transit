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
git clone https://github.com/yourusername/adeya-transit.git
cd adeya-transit

# Create and activate a virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration
Edit `config.py` to set your desired station IDs.
- Find your Stop ID in the [MTA Stop List](https://data.ny.gov/Transportation/MTA-Subway-Stops/u855-bhbe).
- Example: `L11` is Bedford Av.

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