This script detects motion using your webcam and triggers keyboard actions based on the detected motion. It's designed to work with Minecraft or other applications where you might want to simulate key presses based on movement.

## Features
- Detects motion and identifies "Walking" and "Jumping" movements.
- Simulates key presses for "Walking" and "Jumping".
- Configurable via a configuration file.
- Displays movement status on the video feed.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- Keyboard

## Installation

1. Clone the repository:
Create a virtual environment:

python -m venv venv
source venv/bin/activate    # On Windows use `venv\Scripts\activate`
Install the required packages:

pip install -r requirements.txt
Configuration
Create a configuration file named config in the same directory as the script. The configuration file should have the following format:

min_area=500
line_height=200
key_walk=w
key_jump=space
use_keyboard=True
start_delay=5
min_area: Minimum contour area to consider as motion.
line_height: Height of the horizontal line for detecting "Walking" and "Jumping".
key_walk: Key to press when "Walking" is detected.
key_jump: Key to press when "Jumping" is detected.
use_keyboard: Whether to simulate key presses.
start_delay: Number of seconds to wait before starting the detection.
Usage
Run the script using the following command:

python motion_detection.py
Ensure your application (e.g., Minecraft) is in focus and ready to receive key presses.

Notes
The script will display "Subscribe to pycrafting_tv" on the video feed.
Press the q key to exit the script.
Troubleshooting
If you encounter any issues, ensure that:

Your webcam is properly connected and accessible.
All required packages are installed.
The configuration file is correctly formatted and located in the same directory as the script.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

Acknowledgements
This project uses the following open-source libraries:

OpenCV
NumPy
Keyboard
