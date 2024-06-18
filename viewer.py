import sys
import os
import numpy as np
import nibabel as nib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QWidget, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Ensure required folders exist
required_folders = ['CT', 'Ground_truth', 'Predicted']
for folder in required_folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to load nii.gz files
def load_nii(file_path):
    return nib.load(file_path).get_fdata()

# Function to normalize the CT scan intensities to be between given min and max
def normalize_ct_scan(ct_scan, min_intensity, max_intensity):
    ct_scan = np.clip(ct_scan, min_intensity, max_intensity)
    return (ct_scan - min_intensity) / (max_intensity - min_intensity) * 90

# Define min and max intensity values
min_intensity = 0
max_intensity = 90

# Load the CT scan and Ground Truth data
def load_subject_data(subject_name):
    # Initialize variables to None
    ct_scan = ground_truth = predicted = None

    # Load the CT scan
    ct_scan_path = f'CT/{subject_name}.nii.gz'
    if os.path.exists(ct_scan_path):
        ct_scan = load_nii(ct_scan_path)
        ct_scan = normalize_ct_scan(ct_scan, min_intensity, max_intensity)
        ct_scan = np.flip(np.rot90(ct_scan))  # Correct orientation if necessary

    # Load the Ground Truth data
    ground_truth_path = f'Ground_truth/{subject_name}.nii.gz'
    if os.path.exists(ground_truth_path):
        ground_truth = load_nii(ground_truth_path)
        ground_truth = np.flip(np.rot90(ground_truth))  # Correct orientation if necessary

    # Load the Predicted data
    predicted_path = f'Predicted/{subject_name}.nii.gz'
    if os.path.exists(predicted_path):
        predicted = load_nii(predicted_path)
        predicted = np.flip(np.rot90(predicted))  # Correct orientation if necessary

    # Ensure the dimensions match if all images are present
    if ct_scan is not None and ground_truth is not None:
        assert ct_scan.shape == ground_truth.shape, "CT scan and ground truth dimensions do not match!"
    if ct_scan is not None and predicted is not None:
        assert ct_scan.shape == predicted.shape, "CT scan and predicted dimensions do not match!"

    return ct_scan, ground_truth, predicted

class MplCanvas(FigureCanvas):
    # Initialize the matplotlib canvas with black background and white text
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='black')
        self.axes1 = fig.add_subplot(131)
        self.axes2 = fig.add_subplot(132)
        self.axes3 = fig.add_subplot(133)
        super(MplCanvas, self).__init__(fig)

    # Plot slices of the CT scan and the ground truth overlay
    def plot_slices(self, slice_index, min_intensity, max_intensity, ct_scan, ground_truth, predicted=None, show_overlay=True):
        self.axes1.clear()
        self.axes2.clear()
        self.axes3.clear()

        if ct_scan is not None:
            # Plot the CT scan slice
            self.axes1.imshow(ct_scan[:, :, slice_index], cmap='gray', vmin=min_intensity, vmax=max_intensity)
            self.axes1.set_title(f'CT Scan Slice {slice_index}', color='white')
        else:
            self.axes1.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes1.transAxes)
            self.axes1.set_title('CT Scan', color='white')
        self.axes1.axis('off')
        for spine in self.axes1.spines.values():
            spine.set_edgecolor('white')

        if ct_scan is not None and ground_truth is not None:
            # Normalize the slice data to the range [0, 1]
            slice_data = ct_scan[:, :, slice_index]
            normalized_slice = (slice_data - min_intensity) / (max_intensity - min_intensity)
            ct_rgb = np.stack([normalized_slice]*3, axis=-1)

            if show_overlay:
                # Create a red mask where the ground truth is 1
                red_mask = (ground_truth[:, :, slice_index] == 1)
                not_red_mask = np.logical_not(red_mask)

                # Apply the red mask
                ct_rgb[not_red_mask == False] = 0
                red_condition = np.all(ct_rgb == 0, axis=-1) & (red_mask == 1)
                ct_rgb[red_condition] = [1, 0, 0]

            # Plot the CT scan with ground truth overlay
            self.axes2.imshow(ct_rgb)
            self.axes2.set_title(f'CT Scan with Ground Truth Slice {slice_index}', color='white')
        else:
            self.axes2.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes2.transAxes)
            self.axes2.set_title('CT Scan with Ground Truth', color='white')
        self.axes2.axis('off')
        for spine in self.axes2.spines.values():
            spine.set_edgecolor('white')

        if ct_scan is not None and predicted is not None:
            ct_rgb_pred = np.stack([normalized_slice]*3, axis=-1)
            if show_overlay:
                pred_mask = (predicted[:, :, slice_index] == 1)
                not_pred_mask = np.logical_not(pred_mask)

                # Apply the red mask for prediction
                ct_rgb_pred[not_pred_mask == False] = 0
                red_condition_pred = np.all(ct_rgb_pred == 0, axis=-1) & (pred_mask == 1)
                ct_rgb_pred[red_condition_pred] = [1, 0, 0]

            self.axes3.imshow(ct_rgb_pred)
            self.axes3.set_title(f'CT Scan with Predicted Slice {slice_index}', color='white')
        else:
            self.axes3.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes3.transAxes)
            self.axes3.set_title('CT Scan with Predicted', color='white')
        self.axes3.axis('off')
        for spine in self.axes3.spines.values():
            spine.set_edgecolor('white')

        self.draw()

class MainWindow(QMainWindow):
    # Initialize the main window with customized UI elements
    def __init__(self):
        super().__init__()

        self.setWindowTitle('3D CT Scan Viewer')
        self.setStyleSheet("background-color: black; color: white;")
        # self.resize(1200, 800)  # Increase window size

        layout = QVBoxLayout()

        # Add subject controls at the top
        self.subject_controls_layout = QHBoxLayout()
        self.prev_subject_button = QPushButton('<')
        self.prev_subject_button.setFixedWidth(30)
        self.subject_input = QLineEdit()
        self.subject_input.setText('001')
        self.subject_input.setFixedWidth(50)
        self.next_subject_button = QPushButton('>')
        self.next_subject_button.setFixedWidth(30)
        
        subject_label = QLabel('ID:')
        subject_label.setStyleSheet("font-size: 16px;")  # Increase font size
        layout.addWidget(subject_label, alignment=Qt.AlignLeft)
        self.subject_controls_layout.addWidget(self.prev_subject_button, alignment=Qt.AlignCenter)
        self.subject_controls_layout.addWidget(self.subject_input, alignment=Qt.AlignCenter)
        self.subject_controls_layout.addWidget(self.next_subject_button, alignment=Qt.AlignCenter)
        self.subject_controls_layout.addStretch()
        layout.addLayout(self.subject_controls_layout)
        self.canvas = MplCanvas(self, width=15, height=5, dpi=100)
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(99)  # Default value, will be updated later
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_plot)

        self.min_intensity_input = QLineEdit()
        self.min_intensity_input.setText(str(min_intensity))
        self.min_intensity_input.setFixedWidth(50)
        self.max_intensity_input = QLineEdit()
        self.max_intensity_input.setText(str(max_intensity))
        self.max_intensity_input.setFixedWidth(50)

        self.duration_input = QLineEdit()
        self.duration_input.setText("20")
        self.duration_input.setFixedWidth(50)

        self.prev_button = QPushButton('<')
        self.next_button = QPushButton('>')
        self.animate_button = QPushButton('Animate Slices')
        self.toggle_overlay_button = QPushButton('Toggle Overlay')

        # Connect button actions to their respective functions
        self.prev_button.clicked.connect(self.prev_slice)
        self.next_button.clicked.connect(self.next_slice)
        self.animate_button.clicked.connect(self.animate_slices)
        self.toggle_overlay_button.pressed.connect(self.hide_overlay)
        self.toggle_overlay_button.released.connect(self.show_overlay)
        self.prev_subject_button.clicked.connect(self.prev_subject)
        self.next_subject_button.clicked.connect(self.next_subject)
        self.subject_input.returnPressed.connect(self.load_subject)

        # Set up styles for buttons
        button_style = """
        QPushButton {
            background-color: #4CAF50;  /* Green background */
            color: white;  /* White text */
            border-radius: 10px;  /* Rounded corners */
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;  /* Darker green on hover */
        }
        """
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        self.animate_button.setStyleSheet(button_style)
        self.toggle_overlay_button.setStyleSheet(button_style)
        self.prev_subject_button.setStyleSheet(button_style)
        self.next_subject_button.setStyleSheet(button_style)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel('Min Intensity:'))
        controls_layout.addWidget(self.min_intensity_input)
        controls_layout.addWidget(QLabel('Max Intensity:'))
        controls_layout.addWidget(self.max_intensity_input)
        controls_layout.addWidget(QLabel('Duration (ms):'))
        controls_layout.addWidget(self.duration_input)
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.slider)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.animate_button)
        controls_layout.addWidget(self.toggle_overlay_button)

        layout.addLayout(controls_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show_overlay_flag = True
        self.load_subject()

    # Load the subject data and update the plot
    def load_subject(self):
        subject_name = self.subject_input.text().zfill(3)  # Ensure subject name has leading zeros
        try:
            self.ct_scan, self.ground_truth, self.predicted = load_subject_data(subject_name)
            if self.ct_scan is not None:
                self.slider.setMaximum(self.ct_scan.shape[2] - 1)
            else:
                self.slider.setMaximum(0)
            self.update_plot()
        except Exception as e:
            self.subject_input.setText('Error')
            print(f"Error loading subject {subject_name}: {e}")

    # Navigate to the previous subject
    def prev_subject(self):
        current_subject = int(self.subject_input.text())
        self.subject_input.setText(str(current_subject - 1).zfill(3))
        self.load_subject()

    # Navigate to the next subject
    def next_subject(self):
        current_subject = int(self.subject_input.text())
        self.subject_input.setText(str(current_subject + 1).zfill(3))
        self.load_subject()

    # Update the plot based on the current slider value and intensity inputs
    def update_plot(self):
        slice_index = self.slider.value()
        min_intensity = int(self.min_intensity_input.text())
        max_intensity = int(self.max_intensity_input.text())
        self.canvas.plot_slices(slice_index, min_intensity, max_intensity, self.ct_scan, self.ground_truth, self.predicted, self.show_overlay_flag)

    # Move to the previous slice
    def prev_slice(self):
        current_value = self.slider.value()
        if current_value > 0:
            self.slider.setValue(current_value - 1)

    # Move to the next slice
    def next_slice(self):
        current_value = self.slider.value()
        if current_value < self.slider.maximum():
            self.slider.setValue(current_value + 1)

    # Animate through all slices
    def animate_slices(self):
        duration = int(self.duration_input.text())
        for i in range(self.ct_scan.shape[2] if self.ct_scan is not None else 1):
            self.slider.setValue(i)
            QApplication.processEvents()
            QThread.msleep(duration)

    # Hide overlay
    def hide_overlay(self):
        self.show_overlay_flag = False
        self.update_plot()

    # Show overlay
    def show_overlay(self):
        self.show_overlay_flag = True
        self.update_plot()

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
