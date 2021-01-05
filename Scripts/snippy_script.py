$ import os, subprocess
$ for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘_1P.fastq’):
		f1 = f1.replace(‘_1P.fastq’,””)
		bashCommand = “snippy --cpus 8 --R1 {}_1P.fastq --R2 {}_2P.fastq --ref GCF_000006945.2_ASM694v2_genomic.fna --report --outdir {}_snippy”.format(f1,f1,f1)
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stoud = subprocess.PIPE)
		output, error = process.communicate()
