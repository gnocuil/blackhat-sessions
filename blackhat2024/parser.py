from html.parser import HTMLParser

prefix="https://www.blackhat.com/us-24/briefings/schedule/index.html"

positions=[]

class Session:
    def __init__(self):
        self.title = ""
        
    def isEmpty(self):
        return self.title == ""
        
    def setTitle(self, title):
        self.title = title.replace('\n', '')
        self.title = self.title.replace("\r", "")
        self.title = self.title.replace("\"", "\"\"\"\"")
        
    def setPosition(self, pos):
        #line = pos.split(",")
        #print(pos+str(len(line)))
        self.pos = pos
        #self.level = line[1]
        global positions
        if not pos in positions:
            positions.append(pos)
            print(pos)
    def setDayTime(self, day, time):
        day = day.replace("Wednesday", "8/7")
        day = day.replace("Thursday", "8/8")
        self.day = day
        self.time = time
    def setURL(self, url):
        #print(url)
        global prefix
        self.url = prefix + url

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.state=0
        self.sessions=[]
        
    
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag + str(attrs))
        d=dict()
        for a in attrs:
            d[a[0]] = a[1]
        if self.state == 0:
            if tag == "a":
                if "itemprop" in d:
                    #print(d["itemprop"])
                    if d["itemprop"] == "summary":
                        self.state = 1
                        self.cur = Session()
                        self.cur.setURL(d["href"])
            elif tag == "div":
                if "class" in d:
                    if d["class"] == "start_time_wrapper":
                        #print(d)
                        self.state = 10
        elif self.state == 2:
            if tag == "strong":
                self.state = 3

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.state == 1:
            #print("Title["+data+"]")
            self.cur.setTitle(data)
            self.cur.setDayTime(self.day, self.time)
            self.state = 2
        elif self.state == 3:
            #print("3["+data+"]")
            if data == "Location":
                self.state = 4
            else:
                self.state = 2
        elif self.state == 4:
            #print("4["+data+"]")
            self.cur.setPosition(data[2:])
            self.sessions.append(self.cur)
            self.state = 0
        elif self.state == 10:
            #print("10["+data+"]")
            line = data.split("|")
            self.day = line[0][:-1]
            self.time = line[1][1:-1]
            #print("{"+self.day+"}")
            #print("{"+self.time+"}")
            self.state = 0

#main
with open("raw.html", "r") as f:
    parser = MyHTMLParser()
    parser.feed(f.read())

    with open("list.csv", "w") as f2:
        i=1    
        for s in parser.sessions:
            f2.write(s.day+","+s.time+",\""+s.pos+"\",\"=HYPERLINK(\"\""+s.url+"\"\",\"\""+s.title+"\"\")\"\n")
            i=i+1
