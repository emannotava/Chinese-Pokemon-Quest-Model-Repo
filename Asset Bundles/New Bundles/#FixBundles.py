#Script Credit: ElChicoEevee / ChicoEevee
import sys, os 


for filename in os.listdir("."):
    infile =  open(filename, 'rb')
    dump = infile.read()
    infile.close()

    header = dump[:4]
    
    if header == b'RRPP':
        outfile = open(filename + 'fixed.unity3d', 'wb')
        outfile.write(dump[4:])
        outfile.close()