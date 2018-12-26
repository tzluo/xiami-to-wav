#coding=utf-8
import os
filelist = []#define a list to store filenames and directory
#get list of .xm files in current directory
for root,dirs,files in os.walk(os.curdir):
	if root<>'.':#exclude subdirectories
		continue
	else:
		for file in files:
			if file[-2:]=='xm':
				filelist.append(os.path.join(root,file))
print(str(len(filelist))+" xiami files found.")
for xmfile in filelist:	
        print("processing %d of %d:%s" %(filelist.index(xmfile)+1,len(filelist),xmfile))
        f = open(xmfile,"rb")
        outfile = open(xmfile[:-2]+"wav","wb")
        f.seek(15,0)#skip first 15 bytes
        pcmoff = ord(f.read(1))#the 16th Byte = offset value
        c = f.read(36)#WAV Head, aka "RIFF" and "fmt" chunk
        print("writing WAV Head:"+c)
        outfile.write(c)
        c = f.read()#rest of file
        datastart = c.find("data")#find the position where "data" chunk starts(should be 0 if no LIST chunk exists)
        listinfo = c[0:datastart]#get LIST chunk - it's between "fmt" and "data" chunk
        print("listinfo:%s" %(listinfo))
        pcmhead = c[datastart:datastart+8]#first 8 Bytes of "data chunk" = 'data'(4Bytes)+size of sound data(4 Bytes)
        print("writing pcmhead:"+pcmhead)
        outfile.write(pcmhead)
        c = c[datastart+8:len(c)]#cut first 8 Bytes and get raw sound data
        print("pcmlength:%dbytes" %(len(c)))
        progress = 0#for progress displaying
        for cindex, cb in enumerate(c):
            if progress < int((cindex+1)*100/len(c)):
                progress = int((cindex+1)*100/len(c))#update progress on screen when new percentage value comes up
                print("\r%2d%% finished" %(progress)),
            cb = bytes(chr((ord(cb)-pcmoff)&0xff))#minus a known offset to get true data, only preserve low 8 Bytes in case there's negative value
            outfile.write(cb)
        outfile.write(listinfo)
        outfile.close()
        f.close()
raw_input("Press <enter>")
