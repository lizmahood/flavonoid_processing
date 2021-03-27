import sys
file1=open(sys.argv[1], 'r')
line1=file1.readline()
plist=[]
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        pairs=tab1[0].split(',')
        plist.append(pairs)
    line1=file1.readline()
file1.close()

file1=open(sys.argv[2], 'r') #MGF file
thresh=sys.argv[3]
out1=open(sys.argv[2]+".fil.thresh{}.mgf".format(thresh),'w')


#implist=[9244,11041,11394,11836,12295,12460,12510,12668,13099,13316,13390,13949]
line1=file1.readline(); pcount=0; scanlist=[]
while line1:
    #print (line1)
    if line1.startswith('BEGIN IONS'):
        list1=[line1]; flag=0; mlist=[]
        #print (list1)

    elif line1.startswith('END IONS'):
        list1.append(line1)
        #print (plist)
        #print (mlist)

        #See if overlapping fragments
        flag2=0
        for pairs in plist:
            #print (pairs)
            v1=pairs[0]; v2=pairs[1]
            if v1 in mlist and v2 in mlist:
                flag2=1
                
        if flag2==1:
            if 'SCANS=' in list1[1]:
                scanlist.append(int(list1[1].split('=')[1]))
                                               
            for line in list1:
                out1.write(line)
            pcount+=1
            out1.write('\n')
        list1=[]; mlist=[]
    
    elif 'PEPMASS=' in line1:
        mass1=line1.strip().split('=')[1].split('.')[0]
        mlist.append(mass1)
        list1.append(line1)
        
    elif '=' not in line1 and line1.strip()!='':
        mass2=line1.strip().split()[0].split('.')[0]
        intensity=int(line1.strip().split()[1])
        if intensity>int(thresh):
            list1.append(line1)
            if mass2 not in mlist:
                mlist.append(mass2)
        
    else:
        list1.append(line1)
        
    
    line1=file1.readline()
    
file1.close(); out1.close()

#for scan in implist:
#    if scan not in scanlist:
#        print (scan)

print ("# of peaks written: ", pcount)

print ("Done!")
