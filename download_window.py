import customtkinter
from anyio import sleep
from setuptools.config._validate_pyproject import formats


class DownloadWindow(customtkinter.CTkToplevel):
    def __init__(self, master, choice, formats):
        super().__init__(master)
        self.master = master
        self.title("Download")
        self.geometry("600x600")
        self.choice = choice
        self.formats = formats

        self._fillInWidgets()

    def _fillInWidgets(self):
        self.menuFrame = MenuFrame(self)

class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        master.update()
        super().__init__(master, fg_color="transparent", width=master.winfo_width() - 10)
        self.pack()
        self.master = master
        
        self.__fillInWidgets()

    def __fillInWidgets(self):
        typeLabel = customtkinter.CTkLabel(self, text="Type:", font=customtkinter.CTkFont(size=18))
        typeLabel.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        typeMenu = customtkinter.CTkOptionMenu(self, values=["Video + Audio", "Video Only", "Audio Only"], corner_radius=20, command=self.__typeSelector)
        typeMenu.grid(row=0, column=1, sticky='news', padx=5, pady=5)

        self.typeFrame = TypeFrame(self, "Video + Audio");

        def downloadPressed():
            self.master.choice[2] = True
            self.master.destroy()
            self.master.update()

        downloadButton = customtkinter.CTkButton(self, text="Download", font=customtkinter.CTkFont(size=18), command=downloadPressed)
        downloadButton.grid(row=2, column=0, columnspan=2, sticky='news', padx=5, pady=5)

    def __typeSelector(self, option):
        self.typeFrame.destroy()
        self.master.choice[0] = self.master.choice[1] = None
        self.typeFrame = TypeFrame(self, option);

class TypeFrame(customtkinter.CTkFrame):
    def __init__(self, master, option):
        master.update()
        super().__init__(master, fg_color="transparent")
        self.grid(row=1, column=0, columnspan=2)
        self.master = master
        self.formats = self.master.master.formats
        self.choice = self.master.master.choice

        if (option == "Video + Audio"):
            self.videoRow = 0
            self.audioRow = 2
            self.__videoExtension(self.formats['video'])
            self.__audioExtension(self.formats['audio'])
        elif (option == "Video Only"):
            self.videoRow = 0
            self.__videoExtension(self.formats['video'])
        elif (option == "Audio Only"):
            self.audioRow = 0
            self.__audioExtension(self.formats['audio'])

    def __videoExtension(self, format):
        extensionLabel = customtkinter.CTkLabel(self, text="Video Extension:", font=customtkinter.CTkFont(size=18))
        extensionLabel.grid(row=self.videoRow, column=0, sticky='w', padx=5, pady=5)
        extensionMenu = customtkinter.CTkOptionMenu(self, values=list(format.keys()), corner_radius=20, command=self.__videoResolution)
        extensionMenu.grid(row=self.videoRow, column=1, sticky='news', padx=5, pady=5)

        self.__videoResolution(list(format.keys())[0])

    def __videoResolution(self, extension):
        resolutions = self.formats['video'][extension]
        choice = self.choice

        def finalResolution(selected):
            choice[0]=resolutions[selected]

        resolutionLabel = customtkinter.CTkLabel(self, text="Video Resolution:", font=customtkinter.CTkFont(size=18))
        resolutionLabel.grid(row=self.videoRow + 1, column=0, sticky='w', padx=5, pady=5)
        resolutionMenu = customtkinter.CTkOptionMenu(self, values=list(resolutions.keys()), corner_radius=20, command=finalResolution)
        resolutionMenu.grid(row=self.videoRow + 1, column=1, sticky='news', padx=5, pady=5)

        finalResolution(list(resolutions.keys())[0])

    def __audioExtension(self, format):
        extensionLabel = customtkinter.CTkLabel(self, text="Audio Extension:", font=customtkinter.CTkFont(size=18))
        extensionLabel.grid(row=self.audioRow, column=0, sticky='w', padx=5, pady=5)
        extensionMenu = customtkinter.CTkOptionMenu(self, values=list(format.keys()), corner_radius=20, command=self.__audioQuality)
        extensionMenu.grid(row=self.audioRow, column=1, sticky='news', padx=5, pady=5)

        self.__audioQuality(list(format.keys())[0])

    def __audioQuality(self, extension):
        qualities = self.formats['audio'][extension]
        choice = self.choice

        def finalQuality(selected):
            choice[1]=qualities[selected]

        resolutionLabel = customtkinter.CTkLabel(self, text="Audio Quality:", font=customtkinter.CTkFont(size=18))
        resolutionLabel.grid(row=self.audioRow+1, column=0, sticky='w', padx=5, pady=5)
        resolutionMenu = customtkinter.CTkOptionMenu(self, values=list(qualities.keys()), corner_radius=20, command=finalQuality)
        resolutionMenu.grid(row=self.audioRow+1, column=1, sticky='news', padx=5, pady=5)

        finalQuality(list(qualities.keys())[0])



        