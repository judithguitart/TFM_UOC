$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘.faa’):
		f1 = f1.replace(‘.faa’,””)
		bashCommand = “busco -m protein -i {}.faa --lineage_dataset enterobacterales_odb10 -o busco_anno_{}”.format(f1,f1) 
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
