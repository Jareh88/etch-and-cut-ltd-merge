(function () {

    // The script code goes inside this anonymous function.

    process();

    function process() {
	var inMergeDoc = app.activeDocument;

  	var s = String(app.activeDocument.fullName);
  	var ss = s.replace('.indd', '.txt');

	var inMergeFile = File(s);
	var inDataFile = File(ss);
//  	var file_input = File(ss);

	options = app.activeDocument.dataMergeOptions;
	options.removeBlankLines = true;

  	target = app.activeDocument.dataMergeProperties;
  	target.removeDataSource()
  	target.selectDataSource(inDataFile)
  	target.mergeRecords()

	inMergeDoc.close(SaveOptions.no);
	inMergeFile.remove()
	inDataFile.remove()
    }

})();