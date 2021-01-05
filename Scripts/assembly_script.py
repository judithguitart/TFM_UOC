$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘_1P.fastq’):
		f1 = f1.replace(‘_1P.fastq’,””)
		bashCommand = “spades.py –-careful -1 {}_1P.fastq -2 {}_2P.fastq -o {}_assembly”.format(f1,f1,f1)
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
