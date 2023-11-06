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
def AnaliseRecord():
        rate , data = wavfile.read(filename= filename)
        time = data.shape[0]/rate
        x = np.linspace(0,time,data.shape[0])
        plt.plot(x,data)
        plt.show()
def Makerecord():#defying recording funcction
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
        AnaliseRecord()
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
        Makerecord()
else:   # if opened in app 
    window = tk.Tk()
    #window.size()
    Recordbutton = tk.Button(text="Record",command=Makerecord)
    Analisebutton = tk.Button(text="Analise",command=AnaliseRecord)
    window.title("app mode")
    Recordbutton.pack()
    Analisebutton.pack()
    window.mainloop()