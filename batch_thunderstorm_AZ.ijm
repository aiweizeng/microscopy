macro "Batch Thunderstorm QD" {

path = getDirectory("Choose source Directory ");
//subfolders = getFileList(path);
//path=replace(path, "\\\\","\\\\\\\\");
files = getFileList(path);	


	//subfolders[li]=replace(subfolders[li], "/","\\\\\\\\");
	//files = getFileList(path+subfolders[li]);
	
	for (j=0; j<files.length; j++) {
		showProgress(j+1, files.length);
 
	if (endsWith(files[j], ".nd2")==1){
name=files[j];
open(name);
print(name);
id = getImageID;

//gaussian fit
run("Camera setup", "isemgain=false photons2adu=0.1 pixelsize=80");
run("Run analysis", "filter=[Wavelet filter (B-Spline)] scale=2.0 order=4 detector=[Local maximum] connectivity=8-neighbourhood threshold=std(Wave.F1) estimator=[PSF: Gaussian] sigma=1.6 fitradius=2 method=[Maximum likelihood] full_image_fitting=false mfaenabled=false renderer=[No Renderer]");
run("Export results", "floatprecision=5 filepath="+path+name+".csv  fileformat=[CSV (comma separated)] sigma=true intensity=true offset=true saveprotocol=true x=true y=true bkgstd=true id=true uncertainty_xy=true frame=true");

selectImage(id); 
close();
}





			}
}