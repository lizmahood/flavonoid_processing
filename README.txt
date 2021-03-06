A series of scripts used for flavonoid identification in Bennett et al, 2021

NOTES ON USAGE:
These scripts assume that you are working on a Windows computer and have processed your metabolomic data with MS-DIAL (http://prime.psc.riken.jp/compms/msdial/main.html)
From MSDIAL, you should output an MGF of the aligned results and a PeakHeight or PeakArea file. THEN: REMOVE THE FIRST 4 ROWS OF THIS FILE.
These scripts launch the program CANOPUS (part of the SIRIUS4 package https://bio.informatik.uni-jena.de/software/sirius/). 
They assume you have downloaded and set up SIRIUS4.
For the script entitled make_flavonoid_mgf.py, you also need an MGF containing entries of known flavonoids.


USAGE FOR:
in_house_flavonoid_extraction/extract_flavonoids.py

python in_house_flavonoid_extraction/extract_flavonoids.py in_house_flavonoid_extraction/masses.list.combinations example_inputs/example_compounds.mgf 3000

#####This script extracts peaks with fragments matching those in masses.list.combinations from the input mgf. Outputs new mgf into the same directory as the input.
#####First argument: masses.list.combinations
#####Second argument: input mgf
#####Third argument: masses of aglycone and sugar peaks must be at least this value



USAGE FOR:
running_canopus/1make_and_launch_compounds_individually.py

python running_canopus/1make_and_launch_compounds_individually.py example_inputs/example_compounds.mgf <siriusdir> <mgfdir> example_inputs/example_alignment.tsv <instype>

#####This script launches the CANOPUS software (part of the SIRIUS4 suite) on each of your metabolites individually. The individual mgfs are put in mgfdir, and the output is in siriusdir
#####First argument: Input mgf to classify. 
#####Second argument: Full path to where you want SIRIUS/CANOPUS to output your classifications. This directory must exist before the script is run - the 
script does not create this directory and will error out if it doesn't exist.
#####Third argument: Full path for where individual mgfs (one per compound) will be stored. This CANNOT be the same directory as the second argument.
#####Fourth argument: The alignment file corresponding to your mgf
#####Fifth argument: MS instrument type. Two choices are possible: qtof OR orbitrap



USAGE FOR: 
running_canopus/2concatenate_individual_sirius_outputs.py

python running_canopus/2concatenate_individual_sirius_outputs.py <full path to siriusdir> <output name>

#####This script combines Sirius/CANOPUS outputs made for individual compounds into one file. The output (two tsv files) gets put into the directory of sirius output files
#####First argument: FULL directory FROM ROOT to sirius output files, must end in /
#####Second argument: output name (not directory! no path!) for concatenated sirius output files



USAGE FOR:
running_canopus/3get_confidence_scores.py 

python running_canopus/3get_confidence_scores.py <siriusdir> <compound class> <false positive class> <mode> <canopus summary file> <formula summary file> <output name>

#####This script is versatile. Usage scenario 1: you are analyzing data of a certain type of compound, and want to see how well CANOPUS did in predicting
the correct class of your molecules. Usage scenario 2: You don't know the correct compound class of your molecules, but want to see how "sure" CANOPUS is about
your molecules belonging to their predicted class. In each scenario, a probability score plot and tsv are output.
#####First argument: Path to where your SIRIUS outputs were put
#####Second argument: The compound class you think your molecules are OR Unknown. In our paper, we used class Flavonoids. If your class has spaces, substitue them with _
#####Third argument: The class you want to check False Positive instances of OR none
#####Fourth argument: The ionization mode your samples were collected in. pos OR neg
#####Fifth argument: Path to canopus summary file (output of 2concatenate_individual_sirius_outputs.py)
#####Sixth argument: Path to formula summary file (the other output of 2concatenate_individual_sirius_outputs.py)
#####Seventh argument: Path and name of output files



USAGE FOR: 
make_flavonoid_mgf.py 

python make_flavonoid_mgf.py example_inputs/example_compounds.mgf.fil.thresh3000.mgf example_inputs/example_anthocyanins.mgf example_inputs/example_compounds.mgf <confidence score tsv> <output>

#####This script combines all anthocyanins, in-house predicted flavonoids, and CANOPUS predicted flavonoids (passing the confidence score threshold) into one mgf.
This mgf was used by the authors to create the molecular network as seen in our paper. It also outputs a tsv listing metadata for each metabolite.
#####First argument: The mgf of in-house predicted flavonoids, produced by extract_flavonoids.py
#####Second argument: Input mgf of known anthocyanins
#####Third argument: Input mgf of all compounds (this mgf must have been used to run CANOPUS, and create the confidence score file output by 3get_confidence_scores.py)
#####Fourth argument: Confidence score file, output of 3get_confidence_scores.py. This has to have been made from the mgf used in the third argument.
#####Fifth argument: Desired path and prefix of output file names


