import sys
import pyaudio
from scipy.io import wavfile
import wave
import matplotlib.pyplot as plt
import numpy  as np
import tkinter as tk
from alive_progress import alive_bar
# defying default values
defaultrate = 48000 #taken samples/second *(rate / chunk = num of frames taken in one second)
defaultchannels = 1 # amount of channels
Format = pyaudio.paInt24
defaultChunk = 1024 # is number of frames in buffer(memory portion)
Chunk = defaultChunk
channels = defaultchannels
rate = defaultrate
def filterspace(c):
    if c == ' ':
        return False
    return True
def entryfilter(str:str):
    a = filter(filterspace, str)
    filteredlist = list(a)
    return ''.join(filteredlist)
def Buttonrecord():
    try:
            
        filename = fileentry.get()
        time = entryfilter(timeentry.get())
        if 'h' in time:
            time = int(time.replace('h',''))*3600
        elif 'm' in time:
            time = int(time.replace('m',''))*60
        else:
            time = int(time)
        ratestring = entryfilter(rateentry.get())
        Chunkstring = entryfilter(chunkentry.get())
        channelsstring = entryfilter(channelsentry.get())
        if ratestring != '':
            rate = int(ratestring)
        else:
            rate = 48000
        if Chunkstring != '':
            Chunk = int(Chunkstring)
        else:
            Chunk = 1024
        if channelsstring != '':
            channels = int(channelsstring)
        else:
            channels = 1 
        Makerecord(filename=filename, rate=rate, Format=Format,Chunk=Chunk,channels=channels,time=time)  
    except:
        print("unidentified error")
def Buttonanalise(): 
    AnaliseRecord(filename=fileentry.get())   
def AnaliseRecord(filename:str):
    try:
        rate , data = wavfile.read(filename= filename)
        time = data.shape[0]/rate
        x = np.linspace(0,time,data.shape[0])
        plt.plot(x,data)
        plt.show()
    except:
        print('error no filename or file does not exist')
def Makerecord(filename:str ,rate:int, Format:int ,Chunk:int , channels:int, time:float):#defying recording funcction
        device = pyaudio.PyAudio()# defying the device
        framestowrite = []# array wich will contain data to write to a file
        recordstream = device.open(format= Format,rate= rate, channels= channels,input= True, frames_per_buffer= Chunk)# opening stream with device
        recordstream.start_stream()#starting data intake from stream
        try:
            with alive_bar(int(rate*int(time)/Chunk)) as bar:
                print("Recording...")
                for i in range(0,int(rate*int(time)/Chunk)):#data collecting and appending it to a list wich will be written to a file
                    recordedframes = recordstream.read(Chunk)
                    framestowrite.append(recordedframes)
                    bar()
                recordstream.stop_stream()#stopping data flow througth stream
        except:
            print("error no recording time. Recording aborted")
        #opening a file and setting head parameters
        try:
            file = wave.open(filename,'wb')# opening file
            #setting head parameters
            file.setframerate(rate)
            file.setnchannels(channels)
            file.setsampwidth(device.get_sample_size(Format))
            # writing frames to a file
            file.writeframes(b''.join(framestowrite))# b'' is for bite string
            file.close()#closing file
        except:
            print("error no filename. Creating a file aborted")
        #closing stream, releasing device
        recordstream.close()
        device.terminate()
#if program is run from terminal
if len(sys.argv) >= 3:
    filename = sys.argv[1]
    if sys.argv[2].lower() == "-a":# if loop wich gives back freq(time) ploted function
        AnaliseRecord(filename)
    else:
        time = sys.argv[2].lower()
        if 'h' in time:
            time = int(time.replace('h',''))*3600
        elif 'm' in time:
            time = int(time.replace('m','')) * 60
        else:
            time = int(time)
        if len(sys.argv) == 4:
            Chunk = int(sys.argv[3])
        elif len(sys.argv) == 5:
            Chunk = int(sys.argv[3])
            channels = int(sys.argv[4])
        elif len(sys.argv) == 6:
            Chunk = int(sys.argv[3])
            channels = int(sys.argv[4])
            rate = int(sys.argv[5])
        Makerecord(filename=filename, rate=rate, Format=Format,Chunk=Chunk,channels=channels,time=time)
else:   # if opened in app
    # window definition and tweeks 
    window = tk.Tk()
    window.geometry('900x500')
    window.title("app mode")
    #buttons 
    Recordbutton = tk.Button(text="Record",command=Buttonrecord)
    Recordbutton.place(relx= 0.25 , rely=0.1)
    Analisebutton = tk.Button(text="Analise",command=Buttonanalise)
    Analisebutton.place(relx=0.7 , rely=0.1)
    #entries
    addjust = -0.06
    fileentry = tk.Entry()
    filelabel = tk.Label(text="Filename")
    filelabel.place(relx = 1/6 + addjust, rely = 0.25)
    fileentry.place(relx = 1/6 + addjust, rely = 0.3)
    timeentry = tk.Entry()
    timelabel = tk.Label(text="Time")
    timelabel.place(relx = 1/2 + addjust,rely = 0.25)
    timeentry.place(relx = 1/2 + addjust,rely = 0.3)
    rateentry = tk.Entry()
    ratelabel = tk.Label(text="Rate (optional)")
    ratelabel.place(relx = 5/6 + addjust, rely = 0.25)
    rateentry.place(relx = 5/6 + addjust, rely = 0.3)
    chunkentry = tk.Entry()
    chunklabel = tk.Label(text="Chunk (optional)")
    chunklabel.place(relx = 1/2 + addjust,rely = 0.45)
    chunkentry.place(relx = 1/2 + addjust,rely = 0.5)
    channelsentry = tk.Entry()
    channelslabel = tk.Label(text="Channels (optional)")
    channelslabel.place(relx = 5/6 + addjust, rely = 0.45)
    channelsentry.place(relx = 5/6 + addjust, rely = 0.5)
    window.mainloop()