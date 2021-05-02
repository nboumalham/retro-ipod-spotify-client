from config import *
from base_frame import *
from PIL import ImageTk, Image

class AboutFrame(BaseFrame):
    def __init__(self, parent, controller):
        BaseFrame.__init__(self, parent, controller)
        self.grid_rowconfigure(2, weight=1)
        listFrame = tk.Canvas(self.contentFrame)
        listFrame.configure(bg="red", bd=0, highlightthickness=0)
        listFrame.grid(row=0, column=0, sticky="nsew")

        self.listItems = []
        self.valeurs=[]
        for x in range(8):
            item = tk.Label(listFrame, text =" " + str(x), justify=tk.LEFT, anchor="w", font = MED_FONT, background=SPOT_BLACK, foreground=SPOT_GREEN, padx=(30 * SCALE))
            item.grid(row = x, column = 0, sticky="w",padx = (10, 0))
            itemValue = tk.Label(listFrame, text =" " + str(x), justify=tk.RIGHT, anchor="e", font = MED_FONT, background=SPOT_BLACK, foreground=SPOT_GREEN, padx=(30 * SCALE))
            itemValue.grid(row=x, column=1, sticky="e", padx = (0, 30))
            self.listItems.append(item)
            self.valeurs.append(itemValue)
        listFrame.grid_columnconfigure(0, weight=1)
        # listFrame.grid_columnconfigure(1, weight=1)



    def set_about_list_item(self, index, text, valeur, line_type = LINE_NORMAL, show_arrow = False):
        bgColor = "SPOT_GREEN" if line_type == LINE_HIGHLIGHT else SPOT_BLACK
        txtColor = SPOT_BLACK if line_type == LINE_HIGHLIGHT else \
            (SPOT_GREEN if line_type == LINE_NORMAL else SPOT_WHITE)
        self.listItems[index].configure(background=bgColor, foreground=txtColor, text=text)
        self.valeurs[index].configure(background=bgColor, foreground=txtColor, text=valeur)
