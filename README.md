# microscopy

These are bits of microscopy image analysis code that might be useful. 

To open them, just drag the .ijm file into the ImageJ toolbar


## Simple code bits

### Save_all_images.ijm
This is for when you have multiple images open in ImageJ and you want to save them all at once and then close the windows. 

### batch_convert_any_to_max_intensity_tif.ijm
For images with multiple z-planes. Open all images from a folder, create a maximum intensity z-projection and save the result

### SPLITCHANNEL_MAX_batch.ijm
For images with multiple z-planes and channels. Open all images from a folder, create a maximum intensity z-projection, split the channels and save the resulting channels

### Duplicate_with_gaussian_blur.ijm
For time series images. Open all the images from a folder, gaussian blur, keep a few slices from a timeseries and save the result 


## Tracking dots with Trackmate

Trackmate is an ImageJ plugin for tracking: https://imagej.net/plugins/trackmate/ 

You can use the GUI in ImageJ to test out the parameters based on your images and then subsequently plug in those parameters in to the batch script below (under the section that says Prepare Settings Object). 

I didn't end up using it in the end for the Zeng 2024 paper but it is still useful to have. 

### trackmate_process_batch.py
This is written with Jython. 


## CellProfiler

I used CellProfiler a lot as it is really good for detecting cells in a monolayer. 
https://cellprofiler.org/ 

Input = 2D or 3D images that are split into channels with the same base name e.g. C1_image.tif and C2_image.tif

To open the project file, just download the project file and open it from within the CellProfiler application. 


