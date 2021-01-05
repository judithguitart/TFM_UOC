$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘_1P.fastq’):
		f1 = f1.replace(‘_1P.fastq’,””)
		bashCommand = “ariba run out.card.prepareref {}_1P.fastq {}_2P.fastq {}_out.run”.format(f1,f1,f1)
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
