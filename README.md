# 3D CT Scan Viewer

A graphical user interface (GUI) for viewing 3D CT scans and overlaying ground truth and predicted segmentation masks.

<p align="center">
  <img src="https://github.com/AITwinMinds/3D-CT-Scan-Viewer/assets/100919352/218bd145-2e37-4276-9c9e-b3afadff8d7a" alt="3D CT Scan Viewer">
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

## References

[1] Li, X., Luo, G., Wang, K., Wang, H., Li, S., Liu, J., Liang, X., Jiang, J., Song, Z., Zheng, C., Chi, H., Xu, M., He, Y., Ma, X., Guo, J., Liu, Y., Li, C., Chen, Z., Siddiquee, M.M., Myronenko, A., Sanner, A.P., Mukhopadhyay, A., Othman, A.E., Zhao, X., Liu, W., Zhang, J., Ma, X., Liu, Q., MacIntosh, B.J., Liang, W., Mazher, M., Qayyum, A., Abramova, V., & Llad'o, X. (2023). The state-of-the-art 3D anisotropic intracranial hemorrhage segmentation on non-contrast head CT: The INSTANCE challenge. ArXiv, abs/2301.03281. [Arxiv]

[2] X. Li, G. Luo, W. Wang, K. Wang, Y. Gao and S. Li, "Hematoma Expansion Context Guided Intracranial Hemorrhage Segmentation and Uncertainty Estimation," in IEEE Journal of Biomedical and Health Informatics, vol. 26, no. 3, pp. 1140-1151, March 2022, doi: 10.1109/JBHI.2021.3103850. [Paper]
