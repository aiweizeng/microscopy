# microscopy

These are bits of microscopy image analysis code that might be useful. 


## Simple ImageJ macros

To open them, just drag the .ijm file into the ImageJ toolbar.

This link has all of the possible ImageJ macro functions: https://imagej.net/ij/developer/macro/functions.html 

### Save_all_images.ijm
This is for when you have multiple images open in ImageJ and you want to save them all at once and then close the windows. 

### batch_convert_any_to_max_intensity_tif.ijm
For images with multiple z-planes (not timeseries). Open all images from a folder, create a maximum intensity z-projection and save the result

### SPLITCHANNEL_MAX_batch.ijm
For images with multiple z-planes and channels (not timeseries). Open all images from a folder, create a maximum intensity z-projection, split the channels and save the resulting channels

### Duplicate_with_gaussian_blur.ijm
For time series images. Open all the images from a folder, gaussian blur, keep a few slices from a timeseries and save the result 

******************************************
## Stardist

Stardist is a nuclei/cell detection method that picks up star-convex shapes. https://github.com/stardist/stardist 

### stardist_batch_macro_plusbackground.ijm
They have an ImageJ plugin but you can also use it in Python if you prefer. Here, I have uploaded a macro to use the ImageJ plugin. The plugin has been trained on a nuclei dataset https://imagej.net/plugins/stardist

The input is an image of mouse cortex with 2 channels: DAPI and SYTO. The macro uses Stardist to detect nuclei in the DAPI channel, and use those ROIs to measure both the DAPI and SYTO channels. Also in the code (which can be deleted optionally) I have set a threshold, and then measured the background (i.e. everything not in the nucleus) by combining the thresholded image with the ROIs found by Stardist.  

I have provided a sample image (2023_06_15_SYTO_F1_slice2-1.tif)

![image](https://github.com/aiweizeng/microscopy/assets/65457201/99ad3d93-fdfb-49e5-8602-33c03224d144)

******************************************
## Tracking dots with Trackmate

Trackmate is an ImageJ plugin for tracking dots in time series data: https://imagej.net/plugins/trackmate/ 

### trackmate_process_batch.py

This is written with Jython, which you can open in ImageJ.

You can use the GUI in ImageJ to test out the parameters based on your images and then subsequently plug in those parameters in to the batch script below (under the section that says Prepare Settings Object). 

I didn't end up using it in the end for the Zeng 2024 paper but it is still useful to have. 

******************************************
## Tracking and analysing GEMs

I followed Manu Derivery's code for tracking quantum dots in Stangherlin 2021. Follow this link for comprehensive instructions.  https://github.com/deriverylab/Stangherlin2021/tree/main

Ideally your movie will have around 1000 frames, 10 ms interval 

### Step 1: detection of GEMs (batch_thunderstorm_AZ.ijm)
Thunderstorm plugin for ImageJ is used to track GEMs by Gaussian fitting. https://zitmen.github.io/thunderstorm/ 

### Step 2: Tracking tracks and calculating MSD (AZ_tracking_MSD_batch_dataset.m)
The detected GEMs are tracked in MATLAB, and kept only if they are longer than 15 time points. Then the MSD is calculated and diffusion coefficient calculated by MSD(t) = 4Dt^alpha
https://tinevez.github.io/msdanalyzer/

NB: you need to make sure you have curve fitting toolbox in your MATLAB 
In the same folder as the MATLAB file, you need these files: 
- msdanalyzer.m - function to calculate MSD
- track2.m - function to create tracks 
- 1.tif_timingms2.xls (an excel sheet with the actual timings of each image)

### Step 3: extracting average diffusion coefficients (AZ_FOV_medianMSD_batch.m)
Filters out tracks with good fit (R<0.9) and immobile (alpha < 0.45) then calculates the median diffusion coefficient for each field of view. 

### Step 4: create representative tracking images (GEM_track_analysis_test_3t3_making_plots_csv.mlx)
This reads in individual tracking files, calculates MSD, and plots the tracks coloured by the diffusion coefficient. I added an option to choose the axis limits in order to zoom in on the relevant representative areas. It saves the plots as a very high resolution png. 

### Differences between my code and Manu 
I made only minor changes to the code to fit my experiment:
1. I adapted the thunderstorm tracking code and tweaked the parameters for my microscope set up (100x spinning disk) and for the behaviour of the GEMs
2. AZ_tracking_MSD_batch_dataset.m: I adapted the code so that all of my image files were in the same folder (Derivery code is assuming that the images are grouped in different folders).
3. AZ_FOV_medianMSD_batch.m : I adapted the code so that all of my image files were in the same folder (Derivery code is assuming that the images are grouped in different folders). I also changed it so that it reads in individual tracks files instead of the pooled tracks 

******************************************
## CellProfiler

I used CellProfiler a lot as it is really good for detecting cells in a monolayer. 
https://cellprofiler.org/ 

### Analysing_nuclear_intensity_cellprofiler.cpproj 
This code analyses the nucleus and cytoplasm of a two-channel image, where one of the channels marks the nucleus. In this case, I used it to analyse the nuclear intensity of RNA in a monolayer of fibroblasts. 

Input = 2D or 3D images that are split into channels with the same base name e.g. C1_image.tif and C2_image.tif 

I have provided two example images, where C1- is the RNA channel, and C2- is the DNA channel. 

To open the project file, just download the project file and open it from within the CellProfiler application. 

### CellProfiler_analysis.Rmd
This is an R notebook (open using RStudio) to format the results of CellProfiler into an easier-to-handle format for downstream analysis e.g. in Prism. I have provided an example CellProfiler output (MaskedNuclei.csv) to try. 



