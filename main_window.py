from tkinter import *
import customtkinter
from search import Search
from PIL import Image
import urllib3
from io import BytesIO
import webbrowser
from download import Download

http = urllib3.PoolManager()

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter YouTube Downloader")
        self.geometry("1100x800")

        self._fillInWidgets()

    def _fillInWidgets(self):
        self.topFrame = TopFrame(self)
        self.scrollableFrame = ScrollableFrame(self)

class TopFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack()
        self.master = master

        self._fillInWidgets()

    def _fillInWidgets(self):
        views = [ "Search Results", "Downloads"]
        viewSwitchButtonVariable = customtkinter.StringVar(value=views[0])
        viewSwitchButton = customtkinter.CTkSegmentedButton(self, values=views, command=switchViews, height=40, variable=viewSwitchButtonVariable, corner_radius=20)
        viewSwitchButton.grid(row = 0, column=0, pady=10, padx=5)

        downloadURLImage = Image.open('assets/url.png')
        downloadURLImageObj = customtkinter.CTkImage(dark_image=downloadURLImage, light_image=downloadURLImage, size=(30, 30))
        downloadURLButton = customtkinter.CTkButton(self, image=downloadURLImageObj, command=lambda: self.master.scrollableFrame.populate(viewSwitchButton.get()), width=40, height=40, text="Download URL", corner_radius=20)
        downloadURLButton.grid(row=0, column=1, pady = 10, padx=5)

        searchBox = customtkinter.CTkEntry(self, placeholder_text="Search YouTube", width=500, height=40, corner_radius=20, font=customtkinter.CTkFont(size=20))
        searchBox.grid(row=0, column=2, pady = 10, padx=5)

        searchImage = Image.open('assets/search.png')
        searchImageObj = customtkinter.CTkImage(dark_image=searchImage, light_image=searchImage, size=(30, 30))
        searchButton = customtkinter.CTkButton(self, image=searchImageObj, command=lambda: self.master.scrollableFrame.populate(viewSwitchButton.get(), searchBox.get()), width=40, height=40, text="", corner_radius=20)
        searchButton.grid(row=0, column=3, pady = 10, padx = 5)

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        master.update()
        super().__init__(master, width=master.winfo_width() - 100, height = master.winfo_height() - 135, corner_radius=20)
        self.pack(pady=10)
        self.master = master

    def populate(self, view, query = ""):
        for widget in self.winfo_children():
            widget.destroy()

        if view == "Search Results":
            videoFrames = []
            searchObj = Search(query)
            for i in range(25):
                videoFrame = VideoFrame(self, searchObj.getNext())
                videoFrames.append(videoFrame)

        else:
            print("Under Construction")


class VideoFrame(customtkinter.CTkFrame):
    def __init__(self, master, videoInfo : dict):
        master.update()
        super().__init__(master, width=master.winfo_width() - 10)
        self.master = master
        self.pack()

        self._fillInWidgets(videoInfo)

    def _fillInWidgets(self, videoInfo : dict):
        response = http.request('GET', videoInfo["thumbnail"])
        image_data = BytesIO(response.data)
        videoThumbnailImage = Image.open(image_data)

        videoThumbnailImageObj = customtkinter.CTkImage(dark_image= videoThumbnailImage, light_image=videoThumbnailImage, size=(360, 202))
        videoThumbnail = customtkinter.CTkLabel(self, text = "", image=videoThumbnailImageObj)
        videoThumbnail.grid(row=0, column=0, padx = 5, pady=5)

        # videoThumbnail.bind("<Enter>", self.on_enter)
        # videoThumbnail.bind("<Leave>", self.on_leave)

        videoLength = customtkinter.CTkLabel(self, text=videoInfo["length"])
        videoLength.grid(row=0, column=0, padx=5, pady=5, sticky='se')

        VideoTextFrame(self, videoInfo)

class VideoTextFrame(customtkinter.CTkFrame):
    def __init__(self, master, videoInfo : dict):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.grid(row=0, column=1, padx = 5, pady=5, sticky='nw')

        self._fillInWidgets(videoInfo)

    def _fillInWidgets(self, videoInfo : dict):
        videoTitle = customtkinter.CTkLabel(self, text=videoInfo["title"], width=600, anchor="nw", font=customtkinter.CTkFont(size=22), wraplength=600, justify="left", pady=3)
        videoTitle.grid(row=0, column=0, sticky='nw')

        videoStats = customtkinter.CTkLabel(self, text=f'{videoInfo["views"]}{videoInfo["released"]}', width=600, anchor="nw", font=customtkinter.CTkFont(size=15), wraplength=600, justify="left", pady=3, text_color="#E1D9D1")
        videoStats.grid(row=1, column=0, sticky="nw")
        
        response = http.request('GET', videoInfo["ownerThumbnail"])
        image_data = BytesIO(response.data)
        ownerThumbnailImage = Image.open(image_data)

        ownerThumbnailImageObj = customtkinter.CTkImage(dark_image= ownerThumbnailImage, light_image=ownerThumbnailImage, size=(24, 24))
        ownerThumbnail = customtkinter.CTkLabel(self, text="  " + videoInfo["owner"], width=600, anchor="nw", font=customtkinter.CTkFont(size=15), wraplength=600, justify="left", pady=3, image=ownerThumbnailImageObj, compound="left", text_color="#E1D9D1")
        ownerThumbnail.grid(row=2, column=0, sticky="nw")

        videoDescription = customtkinter.CTkLabel(self, text=videoInfo["description"], width=600, anchor="nw", font=customtkinter.CTkFont(size=15), wraplength=600, justify="left", pady=3, text_color="#E1D9D1")
        videoDescription.grid(row=3, column=0, sticky="nw", pady=3)

        if videoInfo["isSubtitle"]:
            videoCc = customtkinter.CTkLabel(self, text="CC", anchor="nw", font=customtkinter.CTkFont(size=16), wraplength=600, justify="left", pady=3, text_color="#E1D9D1", padx=4, fg_color="#5A5A5A")
            videoCc.grid(row=4, column=0, sticky="nw")

        ActionButtonFrame(self, videoInfo["id"])

class ActionButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, videoId):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.grid(row=1, column=0, padx = 5, pady=5, sticky='ne', rowspan=2)

        self._fillInWidgets(videoId)
    
    def _fillInWidgets(self, videoId):
        openLinkImage = Image.open('assets/open_link.png')
        openLinkImageObj = customtkinter.CTkImage(dark_image=openLinkImage, light_image=openLinkImage, size=(30, 30))
        openLinkButton = customtkinter.CTkButton(self, image=openLinkImageObj, width=40, height=40, text="", corner_radius=20, command=lambda: webbrowser.open(f'youtu.be/{videoId}'))
        openLinkButton.grid(row=0, column=0, pady = 3, padx=5, sticky="ne")

        downloadButtonImage = Image.open('assets/download.png')
        downloadButtonImageObj = customtkinter.CTkImage(dark_image=downloadButtonImage, light_image=downloadButtonImage, size=(30, 30))
        downloadButtonButton = customtkinter.CTkButton(self, image=downloadButtonImageObj, width=40, height=40, text="", corner_radius=20, command=lambda: Download([f'youtu.be/{videoId}'], self))
        downloadButtonButton.grid(row=0, column=1, pady = 3, padx=5, sticky="ne")

def switchViews(view):
    print(view)

