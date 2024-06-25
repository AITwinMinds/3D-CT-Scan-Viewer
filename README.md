<h1 align="left">3D CT Scan Viewer</h1>

<img align="right" width="50" height="50" src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/127874551/b9385586-cff6-4b2a-91cc-1563e756114b" alt="ChatGPT Interface">

A graphical user interface (GUI) for viewing 3D CT scans and overlaying ground truth and predicted segmentation masks.

<br>
<p align="center">
  <img src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/100919352/218bd145-2e37-4276-9c9e-b3afadff8d7a" alt="3D CT Scan Viewer">
</p>

## Updates

- Update the `plot_slices` method in the `MplCanvas` class to differentiate and overlay predictions for two labels (1 and 2) on CT scan slices, using distinct colors (e.g., red for label 1 and blue for label 2).
- Implement a square `QPushButton` styled with dynamic color changes and toggling between start (▶) and stop (■) signs to control animation, synchronizing playback from the current slice in the 3D CT scan viewer application.

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

## References

[1] Li, X., Luo, G., Wang, K., Wang, H., Li, S., Liu, J., Liang, X., Jiang, J., Song, Z., Zheng, C., Chi, H., Xu, M., He, Y., Ma, X., Guo, J., Liu, Y., Li, C., Chen, Z., Siddiquee, M.M., Myronenko, A., Sanner, A.P., Mukhopadhyay, A., Othman, A.E., Zhao, X., Liu, W., Zhang, J., Ma, X., Liu, Q., MacIntosh, B.J., Liang, W., Mazher, M., Qayyum, A., Abramova, V., & Llad'o, X. (2023). The state-of-the-art 3D anisotropic intracranial hemorrhage segmentation on non-contrast head CT: The INSTANCE challenge. ArXiv, abs/2301.03281.

[2] X. Li, G. Luo, W. Wang, K. Wang, Y. Gao and S. Li, "Hematoma Expansion Context Guided Intracranial Hemorrhage Segmentation and Uncertainty Estimation," in IEEE Journal of Biomedical and Health Informatics, vol. 26, no. 3, pp. 1140-1151, March 2022, doi: 10.1109/JBHI.2021.3103850.
