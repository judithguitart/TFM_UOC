$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘_scaffolds.fasta’):
		f1 = f1.replace(‘_scaffolds.fasta’,””)
		bashCommand = “busco -m genome -i {}_scaffolds.fasta --lineage_dataset enterobacterales_odb10 -o busco_{}”.format(f1,f1) 
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
