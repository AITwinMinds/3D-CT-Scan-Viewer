import sys
import os
import numpy as np
import nibabel as nib
from PyQt5.QtWidgets import (QApplication, QGroupBox, QCheckBox, QComboBox, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QWidget, QLineEdit, QLabel, QRadioButton, QButtonGroup, QDialog)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
import matplotlib.pyplot as plt


color_map = {
    'red': [1, 0, 0],
    'green': [0, 1, 0],
    'blue': [0, 0, 1],
    'yellow': [1, 1, 0],
    'cyan': [0, 1, 1],
    'magenta': [1, 0, 1],
}

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

def load_subject_data(subject_name):
    # Initialize variables to None
    global ct_raw
    ct_scan = ground_truth = predicted = None

    # Load the CT scan
    ct_scan_path = f'CT/{subject_name}.nii.gz'
    if os.path.exists(ct_scan_path):
        ct_scan = load_nii(ct_scan_path)
        ct_raw = ct_scan.copy()
        ct_scan = normalize_ct_scan(ct_scan, min_intensity, max_intensity)

    # Load the Ground Truth data
    ground_truth_path = f'Ground_truth/{subject_name}.nii.gz'
    if os.path.exists(ground_truth_path):
        ground_truth = load_nii(ground_truth_path)

    # Load the Predicted data
    predicted_path = f'Predicted/{subject_name}.nii.gz'
    if os.path.exists(predicted_path):
        predicted = load_nii(predicted_path)

    # Ensure the dimensions match if all images are present
    if ct_scan is not None and ground_truth is not None:
        assert ct_scan.shape == ground_truth.shape, "CT scan and ground truth dimensions do not match!"
    if ct_scan is not None and predicted is not None:
        assert ct_scan.shape == predicted.shape, "CT scan and predicted dimensions do not match!"

    return ct_scan, ground_truth, predicted

class MplCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='black')
        self.axes1 = fig.add_subplot(131)
        self.axes2 = fig.add_subplot(132)
        self.axes3 = fig.add_subplot(133)
        super(MplCanvas, self).__init__(fig)

    def plot_slices(self, slice_index, min_intensity, max_intensity, ct_scan, ground_truth, predicted=None, show_overlay=True, view='axial', show_contour=False, label1_color='red', label2_color='blue', opacity=0.5, line_width=0.7):
        self.axes1.clear()
        self.axes2.clear()
        self.axes3.clear()

        if view == 'axial':
            ct_slice = ct_scan[:, :, slice_index] if ct_scan is not None else None
            gt_slice = ground_truth[:, :, slice_index] if ground_truth is not None else None
            pred_slice = predicted[:, :, slice_index] if predicted is not None else None

            if ct_slice is not None:
                ct_slice = np.flip(np.rot90(ct_slice))  # Adjust orientation for display
            if gt_slice is not None:
                gt_slice = np.flip(np.rot90(gt_slice))  # Adjust orientation for display
            if pred_slice is not None:
                pred_slice = np.flip(np.rot90(pred_slice))  # Adjust orientation for display

        elif view == 'coronal':
            ct_slice = ct_scan[:, slice_index, :] if ct_scan is not None else None
            gt_slice = ground_truth[:, slice_index, :] if ground_truth is not None else None
            pred_slice = predicted[:, slice_index, :] if predicted is not None else None

            if ct_slice is not None:
                ct_slice = np.rot90(ct_slice)  # Adjust orientation for display
            if gt_slice is not None:
                gt_slice = np.rot90(gt_slice)  # Adjust orientation for display
            if pred_slice is not None:
                pred_slice = np.rot90(pred_slice)  # Adjust orientation for display

        elif view == 'sagittal':
            ct_slice = ct_scan[slice_index, :, :] if ct_scan is not None else None
            gt_slice = ground_truth[slice_index, :, :] if ground_truth is not None else None
            pred_slice = predicted[slice_index, :, :] if predicted is not None else None

            if ct_slice is not None:
                ct_slice = np.flip(np.rot90(ct_slice, 3, (1, 0)), 1)  # Adjust orientation for display
            if gt_slice is not None:
                gt_slice = np.flip(np.rot90(gt_slice, 3, (1, 0)), 1)  # Adjust orientation for display
            if pred_slice is not None:
                pred_slice = np.flip(np.rot90(pred_slice, 3, (1, 0)), 1)  # Adjust orientation for display

        if ct_scan is not None:
            self.axes1.imshow(ct_slice, cmap='gray', vmin=min_intensity, vmax=max_intensity)
            self.axes1.set_title('CT', color='white')
        else:
            self.axes1.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes1.transAxes)
            self.axes1.set_title('CT', color='white')
        self.axes1.axis('off')
        for spine in self.axes1.spines.values():
            spine.set_edgecolor('white')

        if ct_scan is not None and ground_truth is not None:
            normalized_slice = (ct_slice - min_intensity) / (max_intensity - min_intensity)
            ct_rgb = np.stack([normalized_slice]*3, axis=-1)

            if show_overlay and not show_contour:
                label1_mask = (gt_slice == 1)
                label2_mask = (gt_slice == 2)
                color1 = color_map[label1_color] + [opacity]
                color2 = color_map[label2_color] + [opacity]
                ct_rgb[label1_mask] = (1 - opacity) * ct_rgb[label1_mask] + opacity * np.array(color_map[label1_color])
                ct_rgb[label2_mask] = (1 - opacity) * ct_rgb[label2_mask] + opacity * np.array(color_map[label2_color])

            self.axes2.imshow(ct_rgb)
            if show_contour:
                self.axes2.contour(gt_slice == 1, colors=label1_color, linewidths=line_width)
                self.axes2.contour(gt_slice == 2, colors=label2_color, linewidths=line_width)
            self.axes2.set_title('CT + Ground Truth', color='white')
        else:
            self.axes2.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes2.transAxes)
            self.axes2.set_title('CT + Ground Truth', color='white')
        self.axes2.axis('off')
        for spine in self.axes2.spines.values():
            spine.set_edgecolor('white')

        if ct_scan is not None and predicted is not None:
            normalized_slice = (ct_slice - min_intensity) / (max_intensity - min_intensity)
            ct_rgb_pred = np.stack([normalized_slice]*3, axis=-1)

            if show_overlay and not show_contour:
                pred_mask1 = (pred_slice == 1)
                pred_mask2 = (pred_slice == 2)
                ct_rgb_pred[pred_mask1] = (1 - opacity) * ct_rgb_pred[pred_mask1] + opacity * np.array(color_map[label1_color])
                ct_rgb_pred[pred_mask2] = (1 - opacity) * ct_rgb_pred[pred_mask2] + opacity * np.array(color_map[label2_color])

            self.axes3.imshow(ct_rgb_pred)
            if show_contour:
                self.axes3.contour(pred_slice == 1, colors=label1_color, linewidths=line_width)
                self.axes3.contour(pred_slice == 2, colors=label2_color, linewidths=line_width)
            self.axes3.set_title('CT + Prediction', color='white')
        else:
            self.axes3.text(0.5, 0.5, 'No Image', color='white', ha='center', va='center', transform=self.axes3.transAxes)
            self.axes3.set_title('CT + Prediction', color='white')
        self.axes3.axis('off')
        for spine in self.axes3.spines.values():
            spine.set_edgecolor('white')

        self.draw()

    def set_axes_visibility(self, show_ground_truth, show_prediction):
        self.axes2.set_visible(show_ground_truth)
        self.axes3.set_visible(show_prediction)
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('3D CT Scan Viewer')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: black; color: white;")

        self.base_resolution = (1920, 1080)
        self.screen_resolution = QApplication.desktop().screenGeometry()

        if self.screen_resolution.width() > self.screen_resolution.height():
            self.window_width_percentage = 44
            self.window_height_percentage = 56
            self.scaling_factor_width = self.screen_resolution.width() / self.base_resolution[0]
            self.scaling_factor_height = self.screen_resolution.height() / self.base_resolution[1]
        else:
            self.window_width_percentage = 56
            self.window_height_percentage = 44
            self.scaling_factor_width = self.screen_resolution.width() / self.base_resolution[1]
            self.scaling_factor_height = self.screen_resolution.height() / self.base_resolution[0]

        # Styles   
        line_edit_style = """
        QLineEdit {
            background-color: #0b130d;
            border: 2px solid #555;
            padding: 5px;
            border-radius: 5px;
            color: white;
            max-width: {30 * self.scaling_factor_width}px
        }
        """
        
        colors_style = """
        QComboBox {
            background-color: #0b130d;
            border: 1px solid #555;
            padding: 5px;
            border-radius: 5px;
            color: white;
        }
        """

        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
            width: {60 * self.scaling_factor_width}px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        square_button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        checkbox_style = """
        QCheckBox {
            color: #FFFFFF;
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: {30 * self.scaling_factor_width}px;
            height: {30 * self.scaling_factor_height}px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #555;
            background-color: #0b130d;
        }
        QCheckBox::indicator:checked {
            background-color: #176cbe;
            border: 2px solid #176cbe;
        }
        QCheckBox::indicator:hover {
            border: 2px solid #104f8b;
        }
        """
        groupbox_style = """
        QGroupBox {
            border: 2px solid #555;
            border-radius: 5px;
            margin-top: 2px;
            font-weight: bold;
            color: #FFFFFF;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: #0b130d;
        }
        """
        groupbox_style2 = """
        QGroupBox {
            border: 2px solid #555;
            border-radius: 5px;
            margin-top: 2px;
            font-weight: bold;
            color: #FFFFFF;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: #0b130d;
        }
        """
        opacity_slider_style = """
        QSlider::groove:horizontal {
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #5CACEE;
                border: 1px solid #5CACEE;
                width: 14px;
                margin: -2px 0;
                border-radius: 6px;
            }
        """

        layout = QVBoxLayout()

        self.subject_controls_layout = QHBoxLayout()
        self.prev_subject_button = QPushButton('<')
        self.prev_subject_button.setFixedWidth(int(40 * self.scaling_factor_width))
        self.subject_input = QLineEdit()
        self.subject_input.setText('SUB_001')
        self.subject_input.setFixedWidth(int(150 * self.scaling_factor_width))
        self.next_subject_button = QPushButton('>')
        self.next_subject_button.setFixedWidth(int(40 * self.scaling_factor_width))

        self.shape_label = QLabel()
        self.shape_label.setFixedHeight(int(60 * self.scaling_factor_height))
        self.shape_label.setText("Shape: Not loaded")

        self.subject_controls_layout.addWidget(self.prev_subject_button)
        self.subject_controls_layout.addWidget(self.subject_input)
        self.subject_controls_layout.addWidget(self.next_subject_button)
        self.subject_controls_layout.addWidget(self.shape_label)
        self.subject_controls_layout.addStretch()

        layout.addLayout(self.subject_controls_layout)

        horizontal_layout = QHBoxLayout()

        # Create GroupBox
        self.Mode_options = QGroupBox("Mode")
        self.Mode_options.setStyleSheet(groupbox_style)
        self.Mode_options.setFixedHeight(int(70 * self.scaling_factor_height))



        # Create layout for GroupBox
        self.view_controls_layout = QHBoxLayout()

        self.axial_radio_button = QRadioButton('Axial')
        self.axial_radio_button.setChecked(True)  # Set axial as the default view
        self.coronal_radio_button = QRadioButton('Coronal')
        self.sagittal_radio_button = QRadioButton('Sagittal')

        self.view_button_group = QButtonGroup()
        self.view_button_group.addButton(self.axial_radio_button)
        self.view_button_group.addButton(self.coronal_radio_button)
        self.view_button_group.addButton(self.sagittal_radio_button)

        self.view_controls_layout.addWidget(self.axial_radio_button)
        self.view_controls_layout.addWidget(self.coronal_radio_button)
        self.view_controls_layout.addWidget(self.sagittal_radio_button)
        self.view_controls_layout.addStretch()
        
        # Set layout for GroupBox
        self.Mode_options.setLayout(self.view_controls_layout)


        # Create GroupBox
        self.visualization_options = QGroupBox("Visualization")
        self.visualization_options.setStyleSheet(groupbox_style2)
        self.visualization_options.setFixedHeight(int(70 * self.scaling_factor_height))


        # Create layout for GroupBox
        visualization_layout = QHBoxLayout()

        # Create and style checkboxes
        self.show_ground_truth_checkbox = QCheckBox('Show Ground Truth')
        self.show_ground_truth_checkbox.setChecked(True)
        self.show_ground_truth_checkbox.stateChanged.connect(self.update_plot)
        self.show_ground_truth_checkbox.setStyleSheet(checkbox_style)

        self.show_prediction_checkbox = QCheckBox('Show Prediction')
        self.show_prediction_checkbox.setChecked(True)
        self.show_prediction_checkbox.stateChanged.connect(self.update_plot)
        self.show_prediction_checkbox.setStyleSheet(checkbox_style)

        # Add checkboxes to layout
        visualization_layout.addWidget(self.show_ground_truth_checkbox)
        visualization_layout.addWidget(self.show_prediction_checkbox)

    
        self.show_contour_checkbox = QCheckBox('Show Contour')
        self.show_contour_checkbox.setChecked(False)
        self.show_contour_checkbox.stateChanged.connect(self.contour_mode_changed)
        self.show_contour_checkbox.setStyleSheet(checkbox_style)


        self.line_width_label = QLabel('Contour Line Width:')
        self.line_width_label.setHidden(True)
        self.line_width_input = QLineEdit()
        self.line_width_input.setText('1.1')  # Default value
        self.line_width_input.setFixedWidth(int(40 * self.scaling_factor_width))
        self.line_width_input.setValidator(QDoubleValidator(0, 10, 2))
        self.line_width_input.setStyleSheet(line_edit_style)
        self.line_width_input.setHidden(True)
        self.line_width_input.returnPressed.connect(self.update_plot)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(75)
        self.opacity_slider.setTickInterval(1)
        self.opacity_slider.valueChanged.connect(self.update_plot)
        self.opacity_slider.setStyleSheet(opacity_slider_style)
        # self.opacity_slider.setFixedSize(int(150 * self.scaling_factor_width), int(20 * self.scaling_factor_height))
    

        self.opacity_input = QLineEdit()
        self.opacity_input.setText('75')
        self.opacity_input.setFixedWidth(int(40 * self.scaling_factor_width))
        self.opacity_input.textChanged.connect(self.update_opacity_slider)
        self.opacity_input.setValidator(QIntValidator(0, 100))

        self.label1_color_combo = QComboBox()
        self.label1_color_combo.addItems(['red', 'green', 'blue', 'yellow', 'cyan', 'magenta'])
        self.label1_color_combo.currentIndexChanged.connect(self.update_plot)
        self.label1_color_combo.setStyleSheet(colors_style)

        self.label2_color_combo = QComboBox()
        self.label2_color_combo.addItems(['blue', 'green', 'red', 'yellow', 'cyan', 'magenta'])
        self.label2_color_combo.currentIndexChanged.connect(self.update_plot)
        self.label2_color_combo.setStyleSheet(colors_style)

        visualization_layout.addWidget(self.show_contour_checkbox)
        visualization_layout.addWidget(self.line_width_label)
        visualization_layout.addWidget(self.line_width_input)

        visualization_layout.addWidget(QLabel('Opacity:'))
        visualization_layout.addWidget(self.opacity_slider)
        visualization_layout.addWidget(self.opacity_input)

        visualization_layout.addWidget(QLabel('Label 1 Color:'))
        visualization_layout.addWidget(self.label1_color_combo)
        visualization_layout.addWidget(QLabel('Label 2 Color:'))
        visualization_layout.addWidget(self.label2_color_combo)
        visualization_layout.addStretch()

        self.visualization_options.setLayout(visualization_layout)

        # Add both GroupBoxes to the horizontal layout
        horizontal_layout.addWidget(self.Mode_options)
        horizontal_layout.addWidget(self.visualization_options)
        horizontal_layout.addStretch(1)
        layout.addLayout(horizontal_layout)


        self.canvas = MplCanvas(self, width=int(30 * self.scaling_factor_width), height=int(5 * self.scaling_factor_height), dpi=100)
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(99)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_plot)

        self.min_intensity_input = QLineEdit()
        self.min_intensity_input.setText(str(min_intensity))
        self.min_intensity_input.setFixedWidth(int(60 * self.scaling_factor_width))
        self.max_intensity_input = QLineEdit()
        self.max_intensity_input.setText(str(max_intensity))
        self.max_intensity_input.setFixedWidth(int(60 * self.scaling_factor_width))

        self.duration_input = QLineEdit()
        self.duration_input.setText("20")
        self.duration_input.setFixedWidth(int(60 * self.scaling_factor_width))

        self.prev_button = QPushButton('<')
        self.next_button = QPushButton('>')
        self.animate_button = QPushButton('▶')
        self.toggle_overlay_button = QPushButton('Toggle Overlay')
        self.plot_histogram_button = QPushButton('Plot Intensity Histogram')

        self.plot_histogram_button.clicked.connect(self.plot_intensity_histogram)
        self.prev_button.clicked.connect(self.prev_slice)
        self.next_button.clicked.connect(self.next_slice)
        self.animate_button.clicked.connect(self.toggle_animation)
        self.toggle_overlay_button.pressed.connect(self.hide_overlay)
        self.toggle_overlay_button.released.connect(self.show_overlay)
        self.prev_subject_button.clicked.connect(self.prev_subject)
        self.next_subject_button.clicked.connect(self.next_subject)
        self.subject_input.returnPressed.connect(self.load_subject)

        self.axial_radio_button.toggled.connect(self.update_plot)
        self.coronal_radio_button.toggled.connect(self.update_plot)
        self.sagittal_radio_button.toggled.connect(self.update_plot)

        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        self.animate_button.setStyleSheet(button_style)
        self.toggle_overlay_button.setStyleSheet(button_style)
        self.prev_subject_button.setStyleSheet(button_style)
        self.next_subject_button.setStyleSheet(button_style)
        self.plot_histogram_button.setStyleSheet(button_style)
        

        self.animate_button.setStyleSheet(square_button_style)

        self.min_intensity_input.setStyleSheet(line_edit_style)
        self.min_intensity_input.returnPressed.connect(self.update_plot)
        self.max_intensity_input.setStyleSheet(line_edit_style)
        self.max_intensity_input.returnPressed.connect(self.update_plot)
        self.duration_input.setStyleSheet(line_edit_style)
        self.subject_input.setStyleSheet(line_edit_style)
        self.opacity_input.setStyleSheet(line_edit_style)

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
        controls_layout.addWidget(self.plot_histogram_button)


        layout.addLayout(controls_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show_overlay_flag = True
        self.is_animating = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_slice)

        self.load_subject()

    def contour_mode_changed(self):
        show_contour = self.show_contour_checkbox.isChecked()
        self.line_width_label.setHidden(not show_contour)
        self.line_width_input.setHidden(not show_contour)
        self.update_plot()

    def update_opacity_slider(self):
        try:
            value = int(self.opacity_input.text())
            if value < 0:
                self.opacity_slider.setValue(0)
            elif value > 100:
                self.opacity_slider.setValue(100)
            else:
                self.opacity_slider.setValue(value)
        except ValueError:
            pass

    def load_subject(self):
        subject_name = self.subject_input.text()
        try:
            self.ct_scan, self.ground_truth, self.predicted = load_subject_data(subject_name)
            self.update_plot()
        except Exception as e:
            self.subject_input.setText('Error')
            print(f"Error loading subject {subject_name}: {e}")
        self.update_shape_label()

    def prev_subject(self):
        current_subject = self.subject_input.text()
        subject_num = int(current_subject.split('_')[-1])
        new_subject = f"SUB_{str(subject_num - 1).zfill(3)}"
        self.subject_input.setText(new_subject)
        self.load_subject()

    def next_subject(self):
        current_subject = self.subject_input.text()
        subject_num = int(current_subject.split('_')[-1])
        new_subject = f"SUB_{str(subject_num + 1).zfill(3)}"
        self.subject_input.setText(new_subject)
        self.load_subject()

    def update_plot(self):
        show_ground_truth = self.show_ground_truth_checkbox.isChecked()
        show_prediction = self.show_prediction_checkbox.isChecked()

        if show_ground_truth and show_prediction:
            self.canvas.set_axes_visibility(True, True)
        elif show_ground_truth:
            self.canvas.set_axes_visibility(True, False)
        elif show_prediction:
            self.canvas.set_axes_visibility(False, True)
        else:
            self.canvas.set_axes_visibility(False, False)

        min_intensity = int(self.min_intensity_input.text())
        max_intensity = int(self.max_intensity_input.text())
        view = self.view_type()
        line_width = float(self.line_width_input.text())
        show_contour = self.show_contour_checkbox.isChecked()
        label1_color = self.label1_color_combo.currentText()
        label2_color = self.label2_color_combo.currentText()
        opacity = self.opacity_slider.value() / 100.0
        self.opacity_input.setText(str(self.opacity_slider.value()))

        if self.ct_scan is not None:
            if view == 'axial':
                self.slider.setMaximum(self.ct_scan.shape[2] - 1)
            elif view == 'coronal':
                self.slider.setMaximum(self.ct_scan.shape[1] - 1)
            elif view == 'sagittal':
                self.slider.setMaximum(self.ct_scan.shape[0] - 1)
        else:
            self.slider.setMaximum(0)
        slice_index = self.slider.value()
        self.canvas.plot_slices(slice_index, min_intensity, max_intensity, self.ct_scan, self.ground_truth, self.predicted, self.show_overlay_flag, view, show_contour, label1_color, label2_color, opacity, line_width)
        self.update_shape_label()

    def view_type(self):
        if self.axial_radio_button.isChecked():
            view = 'axial'
        elif self.coronal_radio_button.isChecked():
            view = 'coronal'
        else:
            view = 'sagittal'
        return view
    
    def prev_slice(self):
        current_value = self.slider.value()
        if current_value > 0:
            self.slider.setValue(current_value - 1)

    def next_slice(self):
        current_value = self.slider.value()
        if current_value < self.slider.maximum():
            self.slider.setValue(current_value + 1)

    def toggle_animation(self):
        if self.is_animating:
            self.stop_animation()
        else:
            self.start_animation()

    def start_animation(self):
        duration = int(self.duration_input.text())
        self.timer.start(duration)
        self.animate_button.setText('■')
        self.animate_button.setStyleSheet("""
        QPushButton {
            background-color: #f44336;
            color: white;
            border-radius: {5 * self.scaling_factor_width}px;
            padding: {10 * self.scaling_factor_width}px;
        }
        QPushButton:hover {
            background-color: #d32f2f;
        }
        """)
        self.is_animating = True

    def stop_animation(self):
        self.timer.stop()
        self.animate_button.setText('▶')
        self.animate_button.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: {5 * self.scaling_factor_width}px;
            padding: {10 * self.scaling_factor_width}px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """)
        self.is_animating = False

    def hide_overlay(self):
        self.show_overlay_flag = False
        self.update_plot()

    def show_overlay(self):
        self.show_overlay_flag = True
        self.update_plot()

    def plot_intensity_histogram(self):
        if hasattr(self, 'ct_scan') and ct_raw is not None:
            # Flatten the ct_raw data
            data = ct_raw.flatten()

            # Compute statistics
            mean_intensity = np.mean(data)
            median_intensity = np.median(data)

            plt.figure(figsize=(10, 6))

            # Plot histogram
            plt.hist(data, bins=170, color='#4682B4', alpha=0.7, rwidth=0.85)

            # Plot mean and median lines
            plt.axvline(mean_intensity, color='red', linestyle='--', linewidth=1, label=f'Mean: {mean_intensity:.2f}')
            plt.axvline(median_intensity, color='green', linestyle='-', linewidth=1, label=f'Median: {median_intensity:.2f}')

            # Add title and labels
            plt.title('CT Scan Intensity Histogram', fontsize=16, fontweight='bold')
            plt.xlabel('Intensity', fontsize=14)
            plt.ylabel('Frequency', fontsize=14)

            # Add grid
            plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.7)

            # Add legend
            plt.legend()

            # Adding annotations
            plt.annotate(f'Mean: {mean_intensity:.2f}', xy=(mean_intensity, plt.ylim()[1] * 0.9), 
                        xytext=(mean_intensity + 100, plt.ylim()[1] * 0.9),
                        arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12, color='red')
            plt.annotate(f'Median: {median_intensity:.2f}', xy=(median_intensity, plt.ylim()[1] * 0.8), 
                        xytext=(median_intensity + 100, plt.ylim()[1] * 0.8),
                        arrowprops=dict(facecolor='green', shrink=0.05), fontsize=12, color='green')

            # Display the plot
            plt.show()
        else:
            print('No CT scan data loaded.')

    def update_shape_label(self):
        if self.ct_scan is not None:
            shape_text = f"Shape: {self.ct_scan.shape} | Slice: {self.slider.value()}"
        else:
            self.shape_label.setText("Shape: Not loaded")
        self.shape_label.setText(shape_text)


          
# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
