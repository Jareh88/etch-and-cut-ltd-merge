(function () {

    // The script code goes inside this anonymous function.

    process();


    function process() {
	var mergeDoc = app.documents[0]; 


	var myPDFExportPreset = app.pdfExportPresets.item("Adobe PDF Press Quality ZIP");
	var myPDFFileName     = mergeDoc.name

	const pattern = /([0-9]{8})[_]+([0-9]{3})[_]+([A-Z]+)[_]+([\w\d]+)/;
	const result  = myPDFFileName.match(pattern);

	var outDate            = result[1]
	var outPlateNum        = result[2]
	var outMaterialCode    = result[3]
	var outProductTypeCode = result[4]

//	alert(myPDFFileName);
//	alert(result[1] + '-' + result[2] + '-' + result[3] + '-' + result[4]);

	var myPDFExportPath   = "S:/MERGE/OUTPUT/" + outDate + "-US" + "/" + outMaterialCode + "_" + outProductTypeCode + "/"
	var myPDFFilePathName = myPDFExportPath.concat(outDate, "_", outPlateNum, "_", outMaterialCode, "_", outProductTypeCode, ".pdf");

	var pagein  = mergeDoc.pages;
	var pageout = [];
	
	for(i=0; i<pagein.length; i++){
		var thisPage   = pagein[i];
		var pageColour = thisPage.pageColor.toString();		
		var pageNumb   = thisPage.documentOffset + 1;

		if (pageColour == 'GREEN'){
			pageout.push(pageNumb);
		}
	}

	            
// 	the pages aren't ordered
        var sortPage = pageout.join(',').split(',').sort(function(a, b){return a-b});
		
	app.pdfExportPreferences.pageRange = pageout.join(",");
	var thisDocument = app.documents[0];

	thisDocument.exportFile(ExportFormat.pdfType, File(myPDFFilePathName), true);
//	thisDocument.exportFile(ExportFormat.pdfType, File(myPDFFilePathName), true, myPDFExportPreset);
//	app.activeDocument.exportFile(ExportFormat.pdfType, File(myPDFFilePathName), false, myPDFExportPreset);

    }

})();