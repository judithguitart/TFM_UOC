$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘_scaffolds.fasta’):
		f1 = f1.replace(‘_scaffolds.fasta’,””)
		bashCommand = “prokka {}_scaffolds.fasta --genus Salmonella --species enterica --outdir prokka_{} --prefix {}”.format(f1,f1,f1)
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
