

# вот этот блок сам поставит библиотеки из списка
def install_and_import(package):
    try:
        import importlib
        importlib.import_module(package)
        print("importlib installed  " +package)
    except ImportError:
        try:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--upgrade"])
            print("subprocess installed  " +package)
        except:
            try:
                import pip
                pip.main(['install', package])
                print("pip installed  " +package)
            except Exception as e:
                print("ни один способ импорта на сработал. Ошибка:  " +str(e))

    try:
        globals()[package] = importlib.import_module(package)
    except Exception as e:
        print("Не получается импортировать модуль " + package + " напрямую. Ошибка:  " +str(e))
        pass

usingList = ['tkinterdnd2']
for module in usingList:
    install_and_import(module)

import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import ttk
import subprocess


class microVideo:

    myName = "newVideo"
    source = ""

    entryStart = None
    middleentry = None
    entryEnd = None

    def offset_time(self, time_str, offsetTime, vector=1):
        from datetime import datetime, timedelta
        time_obj = datetime.strptime(time_str, "%H:%M:%S")

        if vector>0:
            new_time_obj = time_obj + timedelta(minutes=int(offsetTime.split(":")[0]),
                                            seconds=int(offsetTime.split(":")[1]))
        else:
            new_time_obj = time_obj - timedelta(minutes=int(offsetTime.split(":")[0]),
                                            seconds=int(offsetTime.split(":")[1]))
        new_time_str = new_time_obj.strftime("%H:%M:%S")
        return new_time_str

    def cut_video(self):
        file_path = self.source
        start_time = self.entryStart.get()
        end_time = self.entryEnd.get()
        output_path = str(self.myName.replace(":", "-"))+".mp4"
        print("рендерю " + output_path)
        import subprocess
        command = [
            'ffmpeg',
            '-i', file_path,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',
            output_path
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Video cut successfully, saved to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error cutting video: {e}")

    def startEnd(self):
        return self.entryStart, self.entryEnd


    def __init__(self, frame,source, myName, middleTime, timeOffset ):
        self.myName = myName
        self.source = source
        self.entryStart = ttk.Entry(frame)
        self.entryStart.pack(side="left", expand=True, fill="x", padx=5)
        self.entryStart.insert(0, self.offset_time(middleTime, timeOffset, vector = -1))

        self.middleentry = ttk.Entry(frame)
        self.middleentry.pack(side="left", expand=True, fill="x", padx=5)
        self.middleentry.insert(0, middleTime)

        self.entryEnd = ttk.Entry(frame)
        self.entryEnd.pack(side="left", expand=True, fill="x", padx=5)
        self.entryEnd.insert(0, self.offset_time(middleTime, timeOffset, vector = 1))


class ScrollableFrame(ttk.Frame):
    videoObjects = []
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)


        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def add_element(scrollable_frame, videoName, middleTime, timeOffset):
    myName = str(middleTime).replace(":", "-")
    frame = ttk.Frame(scrollable_frame.scrollable_frame)
    frame.pack(fill="x", padx=10, pady=5)

    videoObject = microVideo(frame, videoName, myName, middleTime, timeOffset )
    print(videoObject.myName)
    scrollable_frame.videoObjects.append(videoObject)




def RunCutter(videoObjects):
    for each in videoObjects.videoObjects:
        try:
            # print(each.entryStart.get())
            each.cut_video()
        except Exception as e:
            print( "ошибочка с объектом для нарезки :: " + str(e))


    for each in range(30):
        print("закончено \n")

def create_gui(title = "Scrollable List with Header"):
    root = tk.Tk()
    root.title("Нарезаем " + title)
    videoName = title


    header_frame = ttk.Frame(root)
    header_frame.pack(fill="x", padx=10, pady=10)

    # self.entry = tkinter.Entry(frame, width=40)

    label = ttk.Label(header_frame, text="время момента")
    label.pack(side="left" )


    timestart = ttk.Entry(header_frame)
    timestart.pack(side="left" )
    timestart.insert(0, "00:02:00")


    label = ttk.Label(header_frame, text="отступ")
    label.pack(side="left" )

    timeoffset = ttk.Entry(header_frame)
    timeoffset.pack(side="left")
    timeoffset.insert(0, "01:30")


    add_button = ttk.Button(header_frame, text="добавить точку", command=lambda: add_element(scrollable_frame,videoName, str(timestart.get()) , str(timeoffset.get()) ))
    add_button.pack(side="left")

    label = ttk.Label(header_frame, text="_____")
    label.pack(side="left" )


    run_button = ttk.Button(header_frame, text="рендер", command=lambda: RunCutter( scrollable_frame ) )
    run_button.pack(side="left")




    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollable_frame = ScrollableFrame(main_frame)
    scrollable_frame.pack(fill="both", expand=True)

    root.mainloop()



def drop_gui():
    def drop(event):
        # Get the dropped file path from the event
        file_path = event.data
        file_path = file_path.replace("}", "").replace("{", "")
        # Update the label with the file path
        root.quit()
        # print(root.state)
        root.quit()
        root.destroy()
        create_gui(title=file_path)

        # label.config(text=f"File dropped: {file_path}")

    # Initialize TkinterDnD
    root = TkinterDnD.Tk()
    root.title("Нарезатор стримов")

    # Create a label to display instructions
    label = tk.Label(root, text="перетащи и брось сюда файл записи", width=50, height=10, bg="lightgrey")
    label.pack(padx=10, pady=10)

    # Register the label as a drop target
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)

    # Start the Tkinter event loop
    root.mainloop()



if __name__ == "__main__":
    drop_gui()