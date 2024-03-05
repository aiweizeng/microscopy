input= getDirectory("Choose a Directory");
output= getDirectory("Choose a Directory");
list= getFileList(input);

for(i=0; i<list.length;i++){
	full=input + list[i];
	open(full);
	run("Z Project...", "projection=[Max Intensity]");
	Stack.setChannel(1);
	//run("Brightness/Contrast...");
	setMinAndMax(107, 325);
	Stack.setChannel(2);
	//run("Brightness/Contrast...");
	setMinAndMax(128, 268);

	t= getTitle();


	run("Split Channels");
	selectWindow("C1-"+t);
	t1=getTitle();
	saveAs("tiff", output + t1);
	selectWindow("C2-"+t);
	t2=getTitle();
	saveAs("tiff", output + t2);
	run("Close All");

	
}


