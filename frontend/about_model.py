import spotify_manager
import os


ABOUT_PAGE_SIZE = 8
ABOUT_RENDER = 3


class Rendering():
    def __init__(self, type):
        self.type = type

    def unsubscribe(self):
        pass


class AboutRendering(Rendering):
    def __init__(self, header = "", lines = [], page_start = 0, total_count = 0):
        super().__init__(ABOUT_RENDER)
        self.lines = lines
        self.header = header
        self.page_start = page_start
        self.total_count = total_count
        self.now_playing = False
        self.has_internet = True

class AboutLineItem():
    def __init__(self, title = "", valeur ="", show_arrow = False):
        self.title = title
        self.valeur = valeur
        self.show_arrow = show_arrow


class AboutPage():
    def __init__(self, previous_page, has_sub_page= True, is_title = False):
        self.index = 0
        self.page_start = 0
        self.header = "About"
        self.has_sub_page = "True"
        self.previous_page = previous_page
        self.is_title = is_title
        self.aboutItems = self.get_content()
        self.num_aboutItems = len(self.aboutItems)


    def get_index_jump_up(self):
        return 1

    def get_index_jump_down(self):
        return 1

    def nav_back(self):
        return self.previous_page

    def nav_up(self):
        jump = self.get_index_jump_up()
        if (ABOUT_PAGE_SIZE >= self.total_size() - self.page_start):
            return
        self.page_start = self.page_start + jump
        self.index = self.page_start + ABOUT_PAGE_SIZE - 1

    def nav_down(self):
        jump = self.get_index_jump_down()
        if(self.page_start <= (jump - 1)):
            return
        self.page_start = self.page_start - jump
        self.index = self.page_start

    def getserial(self):
        # Extract serial from cpuinfo file
        cpuserial = "DEV000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
        return cpuserial
    
    def getversion(self):
        # Extract serial from cpuinfo file
        version = "ERROR"
        try:
            f = open('/proc/version','r')
            for line in f:
                version = line[14:]
            f.close()
        except:
            version = "ERROR"
        return version

    def getuptime(self):
        t = os.popen('uptime -p').read()[3:-1]
        return t

    def getcapacity(self):
        # Extract serial from cpuinfo file
        capacity = "0"
        try:
            capacity = os.popen(' df -h').read()[:-1]
        except:
            capacity = "ERROR"
        return capacity

    def get_content(self):
        aboutList = []
        aboutList.append(AboutLineItem("Model", "Zero"))
        aboutList.append(AboutLineItem("Capacity", "32 Gib"))
        aboutList.append(AboutLineItem("Version", self.getversion()))
        aboutList.append(AboutLineItem("Serial", self.getserial()))
        aboutList.append(AboutLineItem("Uptime", self.getuptime()))
        return aboutList


    def total_size(self):
        return self.num_aboutItems


    def render(self):
        content = self.aboutItems
        lines = []
        total_size = self.total_size()
        for i in range(self.page_start, self.page_start + ABOUT_PAGE_SIZE):
            if (i < total_size):
                page = content[i]
                if (page is None) :
                    lines.append(AboutLineItem())
                else:
                    lines.append(page)
            else:
                lines.append(AboutLineItem())
        return AboutRendering(lines=lines, header=self.header, page_start=self.index, total_count=total_size)