import os, subprocess
for f1 in os.listdir(os.getcwd()):
	if f1.endswith(‘.sra_1.fastq’):
		f1 = f1.replace(‘.sra_1.fastq’,””)
		print(f1)
		bashCommand = “trimmomatic PE –threads 5 {}.sra_1.fastq {}.sra_2.fastq –baseout tm_{}/ ILLUMINACLIP:adaptors.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 -trimlog {}_trimm.log > {}_trimm.log 2> {}_trimm.err”.format(f1,f1,f1,f1,f1,f1)
		print(bashCommand)
		try:
			process = subprocess.check_output(bashCommand, shell = True)
		except subprocess.CalledProcessError as err:
			print(err)
