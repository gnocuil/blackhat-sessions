from html.parser import HTMLParser

prefix="https://defcon.org/html/defcon-32/dc-32-speakers.html"

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
        day = day.replace("Friday", "8/9")
        day = day.replace("Saturday", "8/10")
        day = day.replace("Sunday", "8/11")
        self.day = day
        self.time = time
    def setURL(self, id):
        #print(url)
        global prefix
        self.url = prefix + "#" + id

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
            if tag == "article":
                if "class" in d:
                    if d["class"] == "talk":
                        self.cur = Session()
                        self.cur.setURL(d["id"])
                        self.state = 1
                        #print("id="+d["id"])
        elif self.state == 1:
            if tag == "h3":
                if "class" in d and d["class"] == "talk-title":
                    self.state = 2
            elif tag == "p":
                if "class" in d and d["class"] == "time-room":
                    self.state = 3
            

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.state == 2:
            #print("title["+data+"]")
            self.cur.setTitle(data)
            self.state = 1
        elif self.state == 3:
            #print(data)
            line=data.split(" ")
            #print(line)
            self.cur.setDayTime(line[0], line[2])
            track=data[data.find("(")+1:-1]
            #print("{"+track+"}")
            self.cur.setPosition(track)
            self.sessions.append(self.cur)
            self.state = 0
        

#main
with open("speaker.html", "r") as f:
    parser = MyHTMLParser()
    parser.feed(f.read())
    
    prefix = "https://defcon.org/html/defcon-32/dc-32-creator-talks.html"
    with open("creator talk.html", "r") as f3:
        parser.feed(f3.read())

        with open("list.csv", "w") as f2:
            i=1    
            for s in parser.sessions:
                f2.write(s.day+","+s.time+",\""+s.pos+"\",\"=HYPERLINK(\"\""+s.url+"\"\",\"\""+s.title+"\"\")\"\n")
                i=i+1
