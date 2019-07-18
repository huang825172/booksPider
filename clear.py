f = open("get.prn","r")
o = open("out.prn","w")
ls = f.readlines()
for l in ls:
    o.write(l.replace("[专著]",""))
f.close()
o.close()