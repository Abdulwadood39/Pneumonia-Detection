# Medical Data Processing and Visualization Platform

## Overview

This project is a web application designed to facilitate the processing and visualization of medical data specifically X-Ray Images. It aims to provide a platform where users can interact with medical data, view reports, and potentially classify medical images for diagnostic purposes.

## Technologies and Frameworks

- **Flask**: A lightweight web framework for Python, used for building the web application.
- **Matplotlib**: A plotting library for Python, used for generating graphs and visualizations.
- **NumPy**: A library for numerical operations on arrays, used for data manipulation.
- **Pillow**: The Python Imaging Library, used for image processing tasks.
- **TensorFlow**: An open-source machine learning framework, potentially used for image classification tasks.
- **WeasyPrint**: A visual rendering engine for HTML and CSS that can export to PDF, used for generating PDF reports.

## Setup and Installation

1. **Clone the repository**:

   ```
   git clone https://github.com/Abdulwadood39/Pneumonia-Detection.git
   ```
2. **Navigate to the project directory**:

   ```
   cd Pneumonia-Detection
   ```
3. **Install the required packages**:

   ```
   pip install -r requirements.txt
   ```
4. **Set up the database** (if applicable):

   - Follow the instructions in `database.py` to set up the database.
   - Read the comments at the top of the file.
5. **Download Models:**

   - Drive Link: [Models](https://drive.google.com/drive/folders/1tfgOim7M0FWiJB4sizWSET-SAToytTdx?usp=sharing)
   - place the models in directory Pneumonia-Detection/models
6. **Run the application**:

   ```
   python app.py
   ```

## Usage

- **Access the application**: Open a web browser and navigate to `http://localhost:5000` (or the port specified in your Flask application).
- **User Authentication**: Use the provided login functionality to access user-specific features.
- **Viewing Reports**: Navigate to the reports section to view and download medical reports.
- **Image Classification** (if applicable): Upload medical images for classification and visualization.

## Contact

For any questions or concerns, please contact the project maintainer at `<abdulwadoodwaseem@gmail.com>`.

This template provides a comprehensive overview of your project, including its purpose, technologies used, setup instructions, and how to contribute. You can customize it further based on your project's specific needs and features.
