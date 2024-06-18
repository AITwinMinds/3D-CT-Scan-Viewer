# 3D CT Scan Viewer

A graphical user interface (GUI) for viewing 3D CT scans and overlaying ground truth and predicted segmentation masks.

<p align="center">
  <img src="" alt="3D CT Scan Viewer">
</p>

## Required Libraries

Install the required libraries using pip:

```bash
pip install numpy nibabel PyQt5 matplotlib
```

## How to Use

### Prepare Directories

Ensure the following directories exist in the project root:
- `CT`
- `Ground_truth`
- `Predicted`

If they do not exist, the script will create them automatically.

### Naming Conventions

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

### Run the Application

Execute the script to start the GUI:

```bash
python viewer.py
```

### Using the GUI

- Use the left (`<`) and right (`>`) arrow buttons to navigate through different subjects.
- Enter the subject ID directly in the input field to load a specific subject.
- Adjust the slider to navigate through slices.
- Change the minimum and maximum intensity values to adjust the CT scan contrast.
- Use the `Animate Slices` button to animate through all slices.
- Toggle the overlay of ground truth and predicted segmentation masks using the `Toggle Overlay` button.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [AITwinMinds@gmail.com](mailto:AITwinMinds@gmail.com).
