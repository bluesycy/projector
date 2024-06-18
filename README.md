# Projector

Repo for generating projector image for an desired output at the image plane. Check `/code` folder for up-to-date code, if no `/data` folder is created, create one under `/projector`

## Dependencies
Install miniconda: https://docs.anaconda.com/miniconda/, then install the preconfigured environment as follows:
```
conda env create --name envname --file=environments.yml
```
Activate environment:
```
conda activate -n envname
```
Add env kernel (and use that kernel for following notebooks):
```
python -m ipykernel install --user --name=projector
```

For julia packages, please refer to correspondong notebooks.

## Steps

1. (optional) Generate calibration image `image_dmd.npy`
2. Take off the ir filter, project the calibration image (keep the pattern on): 
```
python3 projector_dmd.py
```
After the code above, collect background image, turn off the gui after 5s. If you don't see grating patterns, maybe the display is eaxctly out of phase, try rerunning the code above.
```
evt-viewer evt_bg_collection.h5
```
3. Generate calibration background image using `calibration_make_bg.ipynb`
4. Put the chamber on, save the background image again
```
evt-viewer evt_bg_collection.h5
```
5. Generate chamber background image using `chamber_make_bg.ipynb`
6. Solve geometries with `detect_chamber_bg.ipynb` using results from `chamber_make_bg.ipynb`
7. Define rois in `save_roi.ipynb`
8. Solve projective transformation in `projective transformation.ipynb`
9. Turn off the pattern of calibration image, project the roi image using results from `projective_transformation.ipynb`
```
python3 projector_roi.py
```