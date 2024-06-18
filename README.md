# projector

Check `/code` folder for up-to-date code, if no `/data` folder is created, create one under `/projector`

1. (optional) generate calibration image `image_dmd.npy`
2. project the calibration image
```
python3 projector_dmd.py image_dmd.npy
```
after the code above, collect background image
```
evt-viewer evt_bg_collection.h5
```
3. generate calibration background image using `calibration_make_bg.ipynb`
4. put the chamber on, save the background image again
```
evt-viewer evt_bg_collection.h5
```

5. generate chamber background image using `chamber_make_bg.ipynb`
6. solve geometries using results from `chamber_make_bg.ipynb`
7. define rois in `save_roi.ipynb`
8. solve projective transformation in `projective transformation.ipynb`
9. project the image using results from `projective transformation.ipynb`
```
python3 projector_dmd.py data/roi_transform.npy
```