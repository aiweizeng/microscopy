// Open all files from a source directory
// and save them in a target directory in TIFF format

source_dir = getDirectory("Source Directory");
target_dir = getDirectory("Target Directory");
if (File.exists(source_dir) && File.exists(target_dir)) {
    setBatchMode(true);
    list = getFileList(source_dir);
    for (i=0; i<list.length; i++) {
        if (endsWith(list[i], ".czi")) { //change this fiel type ending 
            open(source_dir + "/" + list[i]);
            run("Z Project...", "projection=[Max Intensity]"); 
	    saveAs("tiff", target_dir + "/" + list[i] + ".tif");
	    close();
	    showProgress(i, list.length);
        }
    }
}
