//https://forum.image.sc/t/stardist-not-generating-label-image-in-batch-macro/54982/9
// Ask for the input folder
input = getDirectory("Choose the Input Folder");

// Ask for the output folder
output = getDirectory("Choose the Output Folder");

//Create a series of folders in the output folder 
ROI_folder = output + File.separator + "ROIs";
File.makeDirectory(ROI_folder);

Label_folder = output + File.separator + "Label images";
File.makeDirectory(Label_folder);

Results_folder = output + File.separator + "Results";
File.makeDirectory(Results_folder);

Background_Results_folder = output + File.separator + "background results";
File.makeDirectory(Background_Results_folder);

processFolder(input);

roiManager("reset");
close("*"); // Close the images
run("Clear Results");

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
    list = getFileList(input);
    list = Array.sort(list);
    for (i = 1; i < list.length; i++) {
        // Check if the file is a TIFF file
        if (endsWith(list[i], ".tif")) {
            // Do the processing here by adding your own code.
            // Leave the print statements until things work, then remove them.
            open(input + list[i]);
            print(i);
            original1 = getTitle();
            original2 = File.nameWithoutExtension;

            // Duplicate Channel 1
            run("Duplicate...", "duplicate channels=1");
            rename("copy");

            // Run StarDist on the duplicated image
            run("Command From Macro", "command=[de.csbdresden.stardist.StarDist2D], args=['input':copy, 'modelChoice':'Versatile (fluorescent nuclei)', 'normalizeInput':'true', 'percentileBottom':'1.0', 'percentileTop':'99.8', 'probThresh':'0.5', 'nmsThresh':'0.4', 'outputType':'Both', 'nTiles':'1', 'excludeBoundary':'2', 'roiPosition':'Automatic', 'verbose':'false', 'showCsbdeepProgress':'false', 'showProbAndDist':'false'], process=[false]");

            // Use the ROIs on both channels
            roiManager("deselect"); // Select all ROIs
            run("Set Measurements...", "area mean standard integrated median redirect=None decimal=3");
            selectWindow(original1);
            roiManager("Multi Measure");
            saveAs("Results", output + "/Results/" +original2 + "_results.csv");
            run("Clear Results");
            
            //now get the background measurements by combining ROIs and making inverse 
            // set threshold first to remove background
            selectWindow(original1);
            roiManager("deselect");
           run("Duplicate...", "duplicate channels=2");
            setThreshold(300, 65535, "raw");
			//run("Convert to Mask", "background=Dark calculate black list create");
			//roiManager("deselect");
			//selectWindow("MASK_" + original2);
			run("Create Selection");
			roiManager("add");
            roiManager("deselect");
			roiManager("XOR");
			roiManager("add");
			count = roiManager("count");
			roiManager("select", count-1); 
			//run("Make Inverse");
			//roiManager("add");
			//count = roiManager("count");
			//roiManager("select", count-1); 
			selectWindow(original1);
			run("Set Measurements...", "area mean standard integrated median redirect=None decimal=3");
			roiManager("Multi Measure");
			saveAs("Results", output + "/background results/" +original2 + "_backgroundresults.csv");

            selectWindow("Label Image");
            saveAs("tiff", output + "/Label images/" + original2 + "_labels.csv");
            roiManager("save", output + "/ROIs/ROI_" + original2 + ".zip");

            roiManager("reset");
            close("ROI Manager");
            close("*"); // Close the images
            print("Processing: " + input + list[i]);
            print("Saving to: " + output);
            run("Clear Results");
        }
    }
}
