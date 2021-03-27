import sys

def get_alignmentID_from_mgf(mgfin, IDonly):
    '''
    :param mgfin: is the path to the mgf input
    :param IDonly: is a boolean, do you want only a list of IDs?
    :returns: Either a dict with ID as key and rest as value, or just IDs
    '''
    odict = {}
    with open(mgfin, 'r') as inp:
        inlin = inp.readline()
        while inlin:
            if inlin.startswith('BEGIN'):
                ostring = inlin
            elif inlin.startswith('SCAN'):
                aid = inlin.strip().split('=')[1]
                ostring += inlin
            elif inlin.startswith('END'):
                ostring += inlin
                inlin = inp.readline()
                ostring += inlin
                odict[aid] = ostring
            else:
                ostring += inlin
            inlin = inp.readline()
    if IDonly:
        return list(odict.keys())

    return odict

def get_charge_from_mgf(mgfin):
    '''
    :param mgfin: is the path to the mgf input
    :returns: IDs of doubly charged entries
    '''
    olist = []
    with open(mgfin, 'r') as inp:
        inlin = inp.readline()
        while inlin:
            if inlin.startswith('SCAN'):
                aid = inlin.strip().split('=')[1]
            elif inlin.startswith('CHARGE'):
                charge = inlin.strip().split('=')[1]
                if '2' in charge:
                    olist.append(aid)
            inlin = inp.readline()

    return olist

def get_alignmentID_from_file(conf_scorf):
    '''
    :param conf_scoref: is output of 4conf_score script with class "Flavonoids"
    :returns: List of Alignment IDs of canopus flavonoids passing thresholds
    '''
    fids, probs = [], []
    with open(conf_scorf, 'r') as flavin:
        flin = flavin.readline()
        flin = flavin.readline()
        while flin:
            fid = flin.strip().split('\t')[0]
            prob = float(flin.strip().split('\t')[1])
            clas = flin.strip().split('\t')[2]
            if clas == 'TP':
                fids.append(fid)
                probs.append(prob)
            flin = flavin.readline()

    flavids = [x for x,p in zip(fids, probs) if p >= 0.633337]

    return flavids

def filter_ms2_peaks(mgfdict):
    '''
    :param mgfdict: is a dict with values as mgf entries.
    :returns: dict but with ms2 peaks <3k removed
    '''
    filtd = {}
    for k, v in mgfdict.items():
        entrylist = v.split('\n')
        ostring = ''
        for lin in entrylist:
            try:
                if lin[0].isdigit():
                    abund = float(lin.strip().split(' ')[1])
                    if abund >= 3000:
                        ostring += (lin + '\n')
                elif lin.startswith('END'):
                    ostring += (lin + '\n\n')
                else:
                    ostring += (lin + '\n')
            except: 
                ostring += lin
        filtd[k] = ostring
    
    return filtd

def write_selected_mgf(mgfdict, ids, ofil):
    '''
    :param mgfdict: is the dict with values as mgf entries
    :param ids: list of ids to output
    :param ofil: is a string of path to output dir
    '''
    with open(ofil + '_allflav.mgf', 'w') as out:
        for k, v in mgfdict.items():
            if k in ids:
                out.write(v)

def make_metadata_file(canopus, anthos, ali, dcharge, ofil):
    '''
    :param canopus: list of canopus IDs
    :param anthos: list of anthocyanin IDs
    :param ali: list of ali's flavonoid IDs
    :param dcharge: list of doubly charged IDs
    :param ofil: string of output directory
    '''
    uniq = canopus + anthos + ali
    uniqueids = set(uniq)
    with open(ofil + '_node_metadata.tab', 'w') as out:
        out.write('Alignment.ID\tAli_flavo\tAntho\tCanopus\tCharge\n')
        for i in uniqueids:
            if i in canopus:
                canop = 1
            else: canop = 0
            if i in anthos:
                antho = 1
            else: antho = 0
            if i in ali:
                al = 1
            else: al = 0
            if i in dcharge:
                charge = 2
            else: charge = 1
            out.write(f'{i}\t{al}\t{antho}\t{canop}\t{charge}\n')

def main(flavmgf, anthomgf, allmgf, alinfil, ofil):
    '''
    All inputs are strings
    '''
    ##all Alignment IDs to output
    anthos = get_alignmentID_from_mgf(anthomgf, True)
    aliflavs = get_alignmentID_from_mgf(flavmgf, True)
    canopusflavs = get_alignmentID_from_file(alinfil)
    doublecharge = get_charge_from_mgf(flavmgf)

    all = anthos + aliflavs + canopusflavs
    allids = list(set(all))

    ##get whole mgf
    allmgf = get_alignmentID_from_mgf(allmgf, False)

    ##filter this
    allmgf_filt = filter_ms2_peaks(allmgf)

    ##write it out
    write_selected_mgf(allmgf_filt, allids, ofil)

    ##write out metadata
    make_metadata_file(canopusflavs, anthos, aliflavs, doublecharge, ofil)

if __name__ == '__main__':

    if len(sys.argv) != 6:
        sys.exit('ARGS: 1) flavonoid mgf (made from extract_flavonoids.py) 2) Anthocyanin mgf '\
            '3) Full mgf 4) conf_score file for flavonoids 5) output directory')

    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5])

    print('Done!')