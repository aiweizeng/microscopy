// Set the input and output directory paths
inputDir = getDirectory("")
outputDir = getDirectory("")

// List all the files in the input directory
list = getFileList(inputDir);

// Set the Gaussian blur sigma (adjust as needed)
sigma = 1.5;

// Process each image in the list
for (i = 0; i < list.length; i++) {
    // Open the current image
    open(inputDir + list[i]);
    
    // Set the number of frames to keep (e.g., 100 frames)
    numFramesToKeep = 100;
    
    // Delete frames beyond the first 100 frames
    run("Delete Slice", "delete=" + (numFramesToKeep + 1) + "-100");

    // Apply Gaussian blur to each frame
    for (frame = 1; frame <= numFramesToKeep; frame++) {
        selectImage(frame);
        run("Gaussian Blur...", "sigma=" + sigma);
    }
    
    // Save the modified image with only the first 100 frames and Gaussian blur
    saveAs("Tiff", outputDir + list[i]);
    close();
}

// Close all open images
close("*");





