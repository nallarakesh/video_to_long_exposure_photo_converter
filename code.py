
import cv2
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import *
from PIL import ImageTk,Image
import time
root = Tk()
start, stop = 0,0
def choose():
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("video file","*.mp4"),("all files","*.*")))
    txt = root.filename
    if(txt.endswith('.mp4')):
        canvas.create_text((w - 20) / 2, h / 2, anchor=S, text="Please wait while the video gets processed",font=("Script", 30, "bold"), fill="white")
        global start, stop
        (rAvg, gAvg, bAvg) = (None, None, None)
        total = 0
        global stream
        stream = cv2.VideoCapture(root.filename)
        start = time.time()
        while True:
            (grabbed, frame) = stream.read()
            if not grabbed:
                break
            (B, G, R) = cv2.split(frame.astype("float"))
            if rAvg is None:
                rAvg = R
                bAvg = B
                gAvg = G
            else:
                rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
                gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
                bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)
            total += 1
        avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
        stop = time.time()
        cv2.imshow('Result', avg)
        cv2.waitKey(0)
        ttbtn = ttk.Button(root, text="Statistics")
        ttbtn.place(x=w/15, y=(h/2 + 40), height=30, width=100)
        ttbtn.config(command=calc)
        root.savename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        cv2.imwrite(root.savename, avg)
        stream.release()
        exit()
    elif(len(txt) == 0):
        print(showinfo("No file selected", "please select any video file"))
    else:
        print(showerror("Incorrect file format", "please select only video file"))
def calc():
    total = float(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(stream.get(cv2.CAP_PROP_FPS))
    print(showinfo("statistics","Time taken to convert is "+str(stop - start)+"\n\nTotal No. of frames rendered are "+str(total)+"\n\nfps value of choosen video is "+str(fps)))
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w, h))
w,h = 700,500
x = sw/2 - w/2
y = sh/2 - h/2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.resizable(0, 0)
style = Style()
style.configure('W.TButton', font = ('calibri', 12, 'bold'), foreground = 'red')
canvas=Canvas(root,width=w,height=h)
image=ImageTk.Image.open(r"E:\background.jpg")
image = image.resize((w,h), Image.ANTIALIAS)
PhotoImg = ImageTk.PhotoImage(image)
canvas.create_image(0,0,anchor=NW,image=PhotoImg)
canvas.create_text((w-20)/2,0, anchor = N , text = "Video to Long Exposure Photo converter", font=("Script", 30, "bold"), fill = "white")
canvas.pack()
chbtn = ttk.Button(root, text = "Choose video", style = 'W.TButton')
chbtn.place(x=w/15, y=h/2, height = 30, width = 100)
chbtn.config(command = choose)
root.mainloop()

