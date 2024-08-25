---

# Face Swap Application

This repository contains a face swapping application built using Python. The application utilizes computer vision techniques to detect and swap faces between two images. It features a graphical user interface (GUI) built with Tkinter, and leverages OpenCV, dlib, and PIL libraries for image processing.

## Features

- **Face Detection**: Uses dlib's frontal face detector and 68-point facial landmark detector to locate and identify faces in images.
- **Face Swapping**: Allows for swapping faces between a source and a destination image, including optional color correction to match skin tones.
- **GUI**: Provides an easy-to-use interface to load images, apply face swapping, and save the results.
- **Image Blending**: Smoothly blends the swapped face with the destination image using a color-based mask to ensure seamless integration.
- **Face Size Scaling**: Option to adjust the size of the swapped face to better fit the destination image.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/face-swap-app.git
   cd face-swap-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the dlib shape predictor model:**
   - Download the `shape_predictor_68_face_landmarks.dat` file from [dlib's model repository](http://dlib.net/files/).
   - Place the file in the project directory.

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Using the GUI:**
   - Click "Choose Source Image" to select the image from which the face will be swapped.
   - Click "Choose Destination Image" to select the image where the face will be swapped in.
   - Optionally, check "Apply Color Correction" to match the skin tones between images.
   - Adjust the "Face Size Scale" to fit the face size according to the destination image.
   - Click "Swap Faces" to perform the face swap operation.
   - Click "Save Result" to save the final image with the swapped face.

## Code Overview

- **`main.py`**: The main script that initializes the Tkinter GUI and handles user interactions.
- **`face_swap.py`**: Contains functions for detecting faces, applying color correction, warping images, creating masks, blending faces, and swapping faces.

## Requirements

- Python 3.x
- OpenCV
- dlib
- Pillow (PIL)
- NumPy
- Tkinter (usually included with Python)

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Make sure to follow the project's coding style and include tests for any new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [dlib](http://dlib.net/): For face detection and landmark detection.
- [OpenCV](https://opencv.org/): For image processing.
- [Pillow](https://python-pillow.org/): For image handling in Tkinter.

---

Feel free to adjust or add any additional information specific to your project or preferences.
