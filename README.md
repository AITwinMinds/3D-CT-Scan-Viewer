<h1 align="left">3D CT Scan Viewer</h1>

<img align="right" width="50" height="50" src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/127874551/b9385586-cff6-4b2a-91cc-1563e756114b" alt="ChatGPT Interface">

A graphical user interface (GUI) for viewing 3D CT scans and overlaying ground truth and predicted segmentation masks.

<br>
<p align="center">
  <img src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/100919352/709e1fa6-0baf-4c80-8d86-3ca7683b2017">
</p>

<p align="center">
  <img src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/100919352/c5b373fe-1de8-420f-aaa5-32ee979daa4b">
</p>


## Required Libraries

Install the required libraries using pip:

```bash
pip install numpy nibabel PyQt5 matplotlib
```

## How to Use

Here is the updated README to clarify both methods of naming the folders and files:

### Prepare Directories

Ensure the following directories exist in the project root:
- `CT`
- `Ground_truth`
- `Predicted`

If they do not exist, the script will create them automatically.

### Naming Conventions

You can name your files using one of the following two methods:

1. **Numeric Only IDs:**

   - **CT scans:** Place files in the `CT` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     CT/
     ├── 001.nii.gz
     ├── 002.nii.gz
     └── 003.nii.gz
     ```

   - **Ground truth segmentations:** Place files in the `Ground_truth` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     Ground_truth/
     ├── 001.nii.gz
     ├── 002.nii.gz
     └── 003.nii.gz
     ```

   - **Predicted segmentations:** Place files in the `Predicted` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     Predicted/
     ├── 001.nii.gz
     ├── 002.nii.gz
     └── 003.nii.gz
     ```

2. **Alphanumeric IDs:**

   - **CT scans:** Place files in the `CT` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     CT/
     ├── SUB_001.nii.gz
     ├── SUB_002.nii.gz
     └── SUB_003.nii.gz
     ```

   - **Ground truth segmentations:** Place files in the `Ground_truth` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     Ground_truth/
     ├── SUB_001.nii.gz
     ├── SUB_002.nii.gz
     └── SUB_003.nii.gz
     ```

   - **Predicted segmentations:** Place files in the `Predicted` directory. Name them as `<subject_id>.nii.gz`.

     Example:
     ```
     Predicted/
     ├── SUB_001.nii.gz
     ├── SUB_002.nii.gz
     └── SUB_003.nii.gz
     ```

Execute the script to start the GUI:

```bash
python viewer.py
```

### Using the GUI

- Use the left `<` and right `>` arrow buttons to navigate through different subjects. You can use either numeric or alphanumeric IDs for the subjects (e.g., 001, SUB_001).
- Enter the subject ID directly in the input field to load a specific subject.
- View Controls: Switch between axial, coronal, and sagittal views.
- Toggle contour display and adjust contour line width.
- Adjust colors for labels and opacity of overlays.
- Adjust the slider to navigate through slices.
- Change the minimum and maximum intensity values to adjust the CT scan contrast.
- Use the `▶` button to animate through the slices automatically.
- Toggle the overlay of ground truth and predicted segmentation masks using the `Toggle Overlay` button.
- Plot intensity histogram

## Support Us

If you find it helpful, consider supporting us in the following ways:

- ⭐ Star this repository on [GitHub](https://github.com/AITwinMinds/3D-CT-Scan-Viewer).
  
- 🐦 Follow us on X (Twitter): [@AITwinMinds](https://twitter.com/AITwinMinds)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [AITwinMinds@gmail.com](mailto:AITwinMinds@gmail.com).
