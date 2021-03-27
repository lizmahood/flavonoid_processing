A series of scripts used for flavonoid identification in Bennett et al, 2021

USAGE FOR:
./in_house_flavonoid_extraction/extract_flavonoids.py

python ./in_house_flavonoid_extraction/extract_flavonoids.py ./in_house_flavonoid_extraction/masses.list.combinations ./example_inputs/example_compounds.mgf 3000

#####This script extracts peaks with fragments matching those in masses.list.combinations from the input mgf. Outputs new mgf into the same directory as the input.
#####First argument: masses.list.combinations
#####Second argument: input mgf
#####Third argument: masses of aglycone and sugar peaks must be at least this value



USAGE FOR:
./running_canopus/1make_and_launch_compounds_individually.py

python ./running_canopus/1make_and_launch_compounds_individually.py ./example_inputs/example_compounds.mgf.fil.thresh3000.mgf <siriusdir> <mgfdir> ./example_inputs/example_alignment.tsv <instype>

#####This script launches the CANOPUS software (part of the SIRIUS4 suite) on each of your metabolites individually. The individual mgfs are put in mgfdir, and the output is in siriusdir
#####First argument: Input mgf to classify. Note that the example input here is NOT included in this repo. It is only created after the above script has been run.
#####Second argument: Full path to where you want SIRIUS/CANOPUS to output your classifications.
#####Third argument: Full path for where individual mgfs (one per compound) will be stored. This CANNOT be the same directory as the second argument.
#####Fourth argument: The alignment file corresponding to your mgf
#####Fifth argument: MS instrument type. Two choices are possible: qtof OR orbitrap



USAGE FOR: 
./running_canopus/2concatenate_individual_sirius_outputs.py

python ./running_canopus/2concatenate_individual_sirius_outputs.py <full path to siriusdir> <output name>

#####This script combines Sirius/CANOPUS outputs made for individual compounds into one file. The output (two tsv files) gets put into the directory of sirius output files
#####First argument: FULL directory FROM ROOT to sirius output files, must end in /
#####Second argument: output name (not directory! no path!) for concatenated sirius output files



USAGE FOR:
./running_canopus/3get_confidence_scores.py 

python ./running_canopus/3get_confidence_scores.py <siriusdir> <compound class> <false positive class> <mode> <canopus summary file> <formula summary file> <output name>

#####This script is quite versatile. Usage scenario 1: you are analyzing data of a certain type of compound, and want to see how well CANOPUS did in predicting
the correct class of your molecules. Usage scenario 2: You don't know the correct compound class of your molecules, but want to see how "sure" CANOPUS is about
your molecules belonging to their predicted class. In each scenario, a probability score plot and tsv are output.
#####First argument: Path to where your SIRIUS outputs were put
#####Second argument: The compound class you think your molecules are OR Unknown. If your class has spaces, substitue them with _
#####Third argument: The class you want to check False Positive instances of OR none
#####Fourth argument: The ionization mode your samples were collected in. pos OR neg
#####Fifth argument: Path to canopus summary file (output of 2concatenate_individual_sirius_outputs.py)
#####Sixth argument: Path to formula summary file (the other output of 2concatenate_individual_sirius_outputs.py)
#####Seventh argument: Path and name of output files









