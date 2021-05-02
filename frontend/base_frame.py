from config import *
import tkinter as tk
from PIL import ImageTk, Image

class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=SPOT_BLACK)
        self.grid_columnconfigure(0, weight=1)

        #FIXME
        self.green_arrow_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_arrow_grn.png')))
        self.black_arrow_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_arrow_blk.png')))
        self.empty_arrow_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_arrow_empty.png')))
        self.play_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_play.png')))
        self.pause_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_pause.png')))
        self.space_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_space.png')))
        self.wifi_image = ImageTk.PhotoImage(self.flattenAlpha(Image.open('pod_wifi.png')))
        header_container = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        header_container.grid(sticky='we')
        self.header_label = tk.Label(header_container, text ="piPod", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN)
        self.header_label.grid(sticky='we', column=1, row=0, padx=(0, 10))
        self.play_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.play_indicator.grid(sticky='w', column=0, row=0, padx=(70 * SCALE,0))
        self.wifi_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.wifi_indicator.grid(sticky='w', column=2, row=0, padx=(0,90 * SCALE))
        header_container.grid_columnconfigure(1, weight=1)

        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=10, padx=(10, 10))


        self.contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        self.contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        self.contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        self.contentFrame.grid(row = 2, column = 0, sticky ="nswe")

        # scrollbar
        self.scrollFrame = tk.Canvas(self.contentFrame)
        self.scrollFrame.configure(bg="orange", width=int(50 * SCALE), bd=0, highlightthickness=4, highlightbackground=SPOT_GREEN)
        self.scrollBar = tk.Canvas(self.scrollFrame, bg=SPOT_GREEN, highlightthickness=0, width=int(20 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5,  y=int(10 * SCALE), anchor="n", relwidth=.6, relheight=.9)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))


    def set_header(self, header, now_playing = None, has_wifi = False):
        truncd_header = header if len(header) < 20 else header[0:17] + "..."
        self.header_label.configure(text=truncd_header)
        play_image = self.space_image
        if now_playing is not None:
            play_image = self.play_image if now_playing['is_playing'] else self.pause_image
        self.play_indicator.configure(image = play_image)
        self.play_indicator.image = play_image
        wifi_image = self.wifi_image if has_wifi else self.space_image
        self.wifi_indicator.configure(image = wifi_image)
        self.wifi_indicator.image = wifi_image



    def show_scroll(self, index, total_count):
        scroll_bar_y_rel_size = max(0.9 - (total_count - MENU_PAGE_SIZE) * 0.06, 0.03)
        scroll_bar_y_raw_size = scroll_bar_y_rel_size * self.scrollFrame.winfo_height()
        percentage = index / (total_count - 1)
        offset = ((1 - percentage) * (scroll_bar_y_raw_size + int(20 * SCALE))) - (scroll_bar_y_raw_size + int(10 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5, rely=percentage, y=offset, anchor="n", relwidth=.66, relheight=scroll_bar_y_rel_size)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))

    def hide_scroll(self):
        self.scrollFrame.grid_forget()



    def flattenAlpha(self, img):
        global SCALE
        [img_w, img_h] = img.size
        img = img.resize((int(img_w * SCALE), int(img_h * SCALE)), Image.ANTIALIAS)
        alpha = img.split()[-1]  # Pull off the alpha layer
        ab = alpha.tobytes()  # Original 8-bit alpha

        checked = []  # Create a new array to store the cleaned up alpha layer bytes

        # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
        transparent = 50  # change to suit your tolerance for what is and is not transparent

        p = 0
        for pixel in range(0, len(ab)):
            if ab[pixel] < transparent:
                checked.append(0)  # Transparent
            else:
                checked.append(255)  # Opaque
            p += 1

        mask = Image.frombytes('L', img.size, bytes(checked))

        img.putalpha(mask)

        return img
