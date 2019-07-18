from urllib import request
import re
filename = input("Filename:")
inf = open(filename,"r")
lines = inf.readlines()
output = open("get.prn","w")
i = 0
for isbn in lines:
    i+=1
    isbn = isbn.strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
    fval = "2J2VFD619642EVGM4KMVPX2TPQ8Y221T6XNB6UBUQ982BHBRTU-09863"
    lurl = "http://opac.nlc.cn/F/"+fval+"?func=find-b&find_code=ISB&request="
    rurl = "&local_base=NLC01&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
    url = lurl+isbn+rurl
    with request.urlopen(url) as file:
        data = file.read()
        try:
            html = str(data,encoding="utf-8")
            titlematch = re.search("题名与责任[\S\s]*?</A",html).span()
            titleRaw = html[titlematch[0]:titlematch[1]]
            titlematch = re.search(";'>[\S\s]*?</A",titleRaw).span()
            titleRaw = titleRaw[titlematch[0]:titlematch[1]]
            titleRaw = titleRaw[3:len(titleRaw)-3]
            titleRaw = titleRaw.strip().replace("&nbsp;"," ").replace(";"," ").strip()
            titleAuth = titleRaw.split("/")
            title = titleAuth[0]
            author = titleAuth[1]

            html = str(data,encoding="utf-8")
            imprintmatch = re.search("出版项[\S\s]*?</A",html).span()
            imprintRaw = html[imprintmatch[0]:imprintmatch[1]]
            imprintmatch = re.search(";'>[\S\s]*?</A",imprintRaw).span()
            imprintRaw = imprintRaw[imprintmatch[0]:imprintmatch[1]]
            imprintRaw = imprintRaw[3:len(imprintRaw)-3]
            imprint = imprintRaw.strip().replace("&nbsp;"," ").replace(";"," ").strip()

            html = str(data,encoding="utf-8")
            callmatch = re.search("载体形态项[\S\s]*?</tr",html).span()
            callRaw = html[callmatch[0]:callmatch[1]]
            callmatch = re.search("left >[\S\s]*?</td",callRaw).span()
            callRaw = callRaw[callmatch[0]:callmatch[1]]
            callRaw = callRaw[6:len(callRaw)-5]
            call = callRaw.strip().replace("&nbsp;"," ").replace(";"," ").strip()

            html = str(data,encoding="utf-8").strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
            kindmatch = re.search("p>中图分类号[\S\s]*?</A",html).span()
            kindRaw = html[kindmatch[0]:kindmatch[1]]
            kindmatch = re.search(";'>[\S\s]*?</A",kindRaw).span()
            kindRaw = kindRaw[kindmatch[0]:kindmatch[1]]
            kindRaw = kindRaw[3:len(kindRaw)-3]
            kind = kindRaw.strip().replace("&nbsp;"," ").replace(";"," ").strip()

        except BaseException as e:
            print(str(i) + " Get fail: "+ isbn)
            print(e)
            output.write(isbn)
            output.write('\n')
        else:
            print(str(i) + " Get Success: "+ isbn)
            output.write(isbn+"~")
            output.write(title+"~")
            output.write(author+"~")
            output.write(imprint+"~")
            output.write(call+"~")
            output.write(kind+"~")
            output.write("\n")
output.close()