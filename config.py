# Configuration for the Subway LED Display

# Your MTA API Key
# NOTE: Confirmed unnecessary as of nyct-gtfs 1.3.2 (pinned in requirements.txt)
# — MTA's GTFS-realtime feeds no longer require a key. NYCTFeed still takes
# this param, but None is accepted and live-tested (2026-09-06) as returning
# real-time data for all TRACKED_LINES below. If MTA ever reinstates key
# enforcement, grab one at https://api.mta.info/ and set it here.
MTA_API_KEY = None

# Tracked Lines and Stops
# Each entry: (Line, StopID, DirectionLabel)
# 125N is 59 St-Columbus Circle Northbound
# A24N is 59 St-Columbus Circle Northbound (for B/C)
TRACKED_LINES = [
    {"line": "1", "stop_id": "125N", "label": "Uptown"},
    {"line": "B", "stop_id": "A24N", "label": "Uptown"},
    {"line": "C", "stop_id": "A24N", "label": "Uptown"},
]

# Refresh rate in seconds
REFRESH_INTERVAL = 30

# Display settings
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32

# Hardware settings (rpi-rgb-led-matrix)
MATRIX_ROWS = 32
MATRIX_COLS = 64
MATRIX_HARDWARE_MAPPING = 'adafruit-hat-pwm'  # -pwm suffix: Quality mode + GPIO4/GPIO18 jumper
GPIO_SLOWDOWN = 2
