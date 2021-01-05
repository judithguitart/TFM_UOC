# TFM_UOC

## 1. Environment and sample preparation 

### Conda environment:
``` 
conda create –n jguitart python = 3.6.11
source activate jguitart
```

### SRA-toolkit:
```
conda install –c bioconda sra-tools
prefetch –-option-file SraAccList.txt
cd sra
fasterq-dump *.sra
```

## 2. Quality control of raw reads

### FastQC:
```
conda install –c bioconda fastqc
fastqc *.fastq
```

### MultiQC for FastQC:
```
conda install –c bioconda multiqc
multiqc *.zip
```


### Kraken:
```
conda install –c bioconda kraken    
wget https://ccb.jhu.edu/software/kraken/dl/minikraken_20171019_8GB.tgz         # To download minikraken database
tar –xvzf minikraken_20171019_8GB.tgz 
kraken --threads 4 --preload --fastq-input –db ~/judith/minikaken_20171019_8GB --paired SRR{}_1.fastq SRR{}_2.fastq --output kraken_{}.txt
kraken-report --db ~/judith/minikraken_20171019_8GB kraken_{}.txt > report_{}.output    	# For individual reports
$ multiqc *.output
```


### Krona:
```
curl -LOk   https://github.com/marbl/Krona/releases/download/v2.7/KronaTools-2.7.tar  
tar xvf KronaTools-2.7.tar
./install.pl –prefix ~/jguitart/downloads 
./updateTaxonomy.sh   # in dir ~/judith/downloads/KronaTools-2.7/
ktImportTaxonomy –o kraken_krona_{}.html –t 3 –s 4 kraken_{}.txt
```


## 3. Adapter trimming

### Trimmomatic:
```
conda install –c bioconda trimmomatic
mkdir trimmedReads
python trimm_script.py

mv *.log *.err tm_* trimmedReads/
multiqc *.err
```


### FastQC after Trimmomatic:
```
mkdir fastqc
cp *P fastqc    # Copy paired-reads from the Trimmomatic output
cd fastqc
for f in *; do mv “$f” “$f.fastq”; done
fastqc *.fastq
multiqc *.zip
``` 


## 4. De novo Assembly

### SPAdes:
```
conda install –c bioconda spades
mkdir assembly
cp *.fastq assembly/
cd assembly
nohup python assembly_script.py > assembly.log 2> assembly.err &

mkdir scaffolds
for i in `dir tm_*_assembly/scaffolds.fasta`; do echo $i; name=$(echo $i | sed “s/tm_//” | sed “s/assembly\///”); cp $i scaffolds/$name; done
cd scaffolds
grep ‘>’ *_scaffolds.fasta | wc -l
```

### BUSCO evaluation:
```
conda install –c bioconda busco
nohup python busco_script.py > busco.log 2> busco.err &

mkdir busco_summaries
for i in `dir busco_SRR*/short_summary.specific.enterobacterales_odb10*`; do cp $i busco_summaries/; done
cd busco_summaries
rename ‘s/.specific.enterobacterales_odb10./_/’ *
multiqc *.txt 
```

### QUAST evaluation:
```
conda install –c bioconda quast
mkdir quast_results
quast *_scaffolds.fasta –r GCF_000006945.2_ASM694v2_genomic.fna -g GCF_000006945.2_ASM694v2_genomic.gff
cd quast_results/results_*
    # Inside this directory there are the report.pdf, report.html and report.tsv files with the results. 
multiqc report.tsv
```


## 5. Annotation

### Prokka:
```
conda install –c bioconda prokka
mkdir annotation
cp *_scaffolds.fasta annotation/
cd annotation
nohup python prokka_script.py > annotation.log 2> annotation.err &
```

### BUSCO evaluation:
```
mkdir busco_annotation
for i in `dir prokka_SRR*/*.faa`; do cp $i busco_annotation/; done
cd busco_annotation_script.py
python busco_annotation_script.py

mkdir busco_summaries
for i in `dir   busco_anno_SRR*/short_summary.specific.enterobacterales_odb10*`; do cp $i busco_summaries/; done
cd busco_summaries
rename ‘s/.specific.enterobacterales_odb10./_/’ *
multiqc *.txt 
```

### GREP search from Prokka:
```
    # inside annotation/ directory:
mkdir AMR_grep_search
for i in `dir prokka_SRR*/*.tsv`; do cp $i AMR_grep_search/; done
grep antibiotic *SRR* > antibiotic.csv
grep resistance *SRR* > resistance.csv
grep multidrug *SRR* > multidrug.csv
```



## 6. Resistance identification


### ARIBA:
```
conda install –c bioconda ariba
mkdir ariba
cp tm_*.fastq ariba/
ariba getref card out.card    # to get reference data from CARD
ariba prepareref –f out.card.fa –m out.card.tsv out.card.prepareref
nohup python ariba_script.py &

mkdir ariba_report
for i in `dir *out.run/report.tsv`; do echo $i; name=$(echo $i | sed “s/out.run\///”); cp $i ariba_report/$name; done
ariba summary out.summary *.tsv
     # The output of this analysis is a .csv table of all the AMR genes absent or present in all samples and a phandango tree in .newick format.
```


## 7. Variant calling

##Snippy:
```
conda install –c conda-forge –c bioconda –c defaults snippy
mkdir snippy
cp tm_*.fastq snippy/
nohup python snippy_script.py > snippy.log 2> snippy.err &

snippy-core *_snippy –-ref GCF_000006945.2_ASM694v2_genomic.fna
```



## 8. Phylogenetic reconstruction

### IQtree:
```
conda install –c bioconda iqtree
iqtree –s core.aln –m MFP    # to find best-fit model
mkdir bootstrap
cp core.aln bootstrap/
cd bootstrap
iqtree –s core.aln –m TVM+F+ASC –B 1000 –alrt 1000
iqtree –s core.aln –m TVM+F+ASC –B 5000 –alrt 1000
```



## 9. Plasmid assembly

### plasmidSPAdes:
```
    # Inside assembly directory
mkdir plasmids
nohup python plasmid_script.py > plasmid.log 2> plasmid.err &
    # After analysis, scaffolds.fasta files of each sample are saved in the new directory named ‘plasmids’ for further analysis: 
for i in `dir tm_*_plasmid/scaffolds.fasta`; do echo $i; name=$(echo $i | sed “s/tm_//” | sed “s/\//_/”); p $i plasmids/$name; done
cp GCF_000006945.2_ASM694v2_genomic.fna GCF_000006945.2_ASM694v2_genomic.gff plasmids/
cd plasmids/
grep ‘>’ *.fasta > plasmids.csv   # Table to count plasmids per sample
```

### QUAST evaluation:
```
mkdir quast_results
quast *_scaffolds.fasta –r GCF_000006945.2_ASM694v2_genomic.fna g GCF_000006945.2_ASM694v2_genomic.gff
multiqc report.tsv
```




