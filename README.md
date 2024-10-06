# Favicon Generator

A simple, user-friendly desktop application for generating favicon sets from a single image. This tool is perfect for developers and designers who want to quickly create favicon sets without the need to open complex design software.

## Features

- Generate multiple favicon sizes from a single image
- Supports various image formats (PNG, JPG, JPEG, BMP, GIF)
- Drag-and-drop functionality for easy image uploading
- Option to save favicons in the original image location or a separate folder
- Preview of generated favicons
- Progress bar for visual feedback during generation
- Maintains original image format for generated favicons

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository or download the `main.py` file.
3. Install the required dependencies:

```
pip install PyQt5 Pillow
```

## Usage

1. Run the script:

```
python main.py
```

2. The Favicon Generator application will launch.
3. Click the "Upload Image" button or drag and drop an image onto the application.
4. Choose whether to save the generated favicons in the original image location or a separate folder.
5. The application will generate the following favicon sizes:
   - Icon-512.png (512x512)
   - Icon-maskable-512.png (512x512)
   - Icon-192.png (192x192)
   - Icon-maskable-192.png (192x192)
6. Preview the generated favicons in the application.
7. Find the generated favicons in the chosen output location.

## Why Use Favicon Generator?

While learning Flutter, I stumbled upon the intricate world of favicons - specifically, the need for multiple sizes and precise naming conventions. This experience sparked the creation of the Favicon Generator.

This tool streamlines the process of creating favicon sets, eliminating the need to open complex design software or manually resize and rename images. It's an ideal solution for developers who want to:

- Quickly generate properly sized favicons for web and mobile projects
- Adhere to specific naming conventions without the hassle of manual renaming
- Save time and maintain focus on core development tasks
- Simplify the favicon creation process, especially for those new to web or app development

Whether you're building a Flutter app, a web application, or any project requiring favicons, this tool helps you overcome the favicon hurdle swiftly and efficiently.

## License

[MIT](https://choosealicense.com/licenses/mit/)