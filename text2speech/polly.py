#this is the code for the GUI for the S2T Converter
import tkinter as tk
import boto3 #python SDK for AWS
import os
import sys
from tempfile import gettempdir
from contextlib import closing

root=tk.Tk()
root.geometry("400x240")
root.title("T2S Converter - Using Amazon Polly")
textExample=tk.Text(root,height=10)
textExample.pack()
def getText():
        aws_mag_con=boto3.session.Session(profile_name='jacomo-profile') #creating programmatically an AWS Session Management
        client=aws_mag_con.client(service_name='polly',region_name='eu-west-1')
        result=textExample.get("1.0","end") #input should be read from line 1 
        print(result)
        response=client.synthesize_speech(VoiceId='Joanna',OutputFormat='mp3',Text=result,Engine='neural')
        print(response)
        if "AudioStream" in response:
                with closing(response['AudioStream']) as stream:
                        output=os.path.join(gettempdir(),"speech.mp3")
                        try:
                            with open(output,"wb") as file:
                                file.write(stream.read())
                        except IOError as error:
                              print(error)
                              sys.exit(-1)
        else:
              print("Could not find the stream!")   
              sys.exit(-1)  
        if sys.platform=='win32':
                os.startfile(output)                       
btnRead=tk.Button(root,height=1,width=10,text="Read",command=getText)
btnRead.pack()

root.mainloop() #keep the window open and persistant until I close it
