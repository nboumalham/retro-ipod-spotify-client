import spotify_manager

ABOUT_PAGE_SIZE = 6
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
        self.header = "About"
        self.has_sub_page = "True"
        self.previous_page = previous_page
        self.is_title = is_title
        self.aboutItems = self.get_content()
        self.num_aboutItems = len(self.aboutItems)

    def nav_back(self):
        return self.previous_page

    def get_content(self):
        aboutList = []
        aboutList.append(AboutLineItem("Songs", "0"))
        aboutList.append(AboutLineItem("Photos", "0"))
        aboutList.append(AboutLineItem("Videos", "0"))       
        aboutList.append(AboutLineItem("Version", "0.1"))
        aboutList.append(AboutLineItem("Model", "Zero"))
        aboutList.append(AboutLineItem("Capacity", "32 GB"))
        aboutList.append(AboutLineItem("S/N", "8KN7F54DE12ZQ56"))
        return aboutList


    def total_size(self):
        return self.num_aboutItems

    def render(self):
        total_size = self.total_size()
        lines = self.get_content()
        return AboutRendering(lines=lines, header=self.header, page_start=0, total_count=total_size)