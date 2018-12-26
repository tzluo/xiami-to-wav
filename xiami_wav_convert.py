#coding=utf-8
import os
filelist = []#文件列表
#获取当前目录下后缀为XM的文件列表
for root,dirs,files in os.walk(os.curdir):
	if root<>'.':#不考虑子目录
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
        f.seek(15,0)#略过前15个字节
        pcmoff = ord(f.read(1))#第16个字节=偏移量pcmoff
        c = f.read(36)#读取WAV文件头
        print("writing WAV Head:"+c)
        outfile.write(c)
        c = f.read()#读取剩下的全部文件内容
        datastart = c.find("data")#查找data块的起始位置，如果没有LIST块，起始位置是0
        listinfo = c[0:datastart]#从文件头结束到data块之前的都是LIST块
        print("listinfo:%s" %(listinfo))
        pcmhead = c[datastart:datastart+8]#data块的头8个字节，'data'+4个字节表示的数据长度
        print("writing pcmhead:"+pcmhead)
        outfile.write(pcmhead)
        c = c[datastart+8:len(c)]#去掉头8个字节后得到波形数据
        print("pcmlength:%dbytes" %(len(c)))
##        len1per=int(len(c)/100)#数据总长度/100，统计进度用
        progress = 0
        for cindex, cb in enumerate(c):
##            if cindex%len1per==0:
            if progress < int((cindex+1)*100/len(c)):
                progress = int((cindex+1)*100/len(c))
                print("\r%2d%% finished" %(progress)),
            cb = bytes(chr((ord(cb)-pcmoff)&0xff))#减去偏移量，考虑溢出的情况，结果截取低8位
            outfile.write(cb)
        outfile.write(listinfo)
        outfile.close()
        f.close()
raw_input("Press <enter>")
