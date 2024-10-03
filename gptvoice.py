import openai
from openai import OpenAI
import json, os
from dotenv import load_dotenv
load_dotenv()

import speech_recognition as sr
import struct
import pyaudio
import pvporcupine
from threading import Thread
PORCUPINE_KEY = os.getenv("PORCUPINE_API_KEY")
import config

def tts(texto, nome_arquivo="output.mp3", modelo="tts-1", voz="alloy"):

  client = openai.OpenAI()

  response = client.audio.speech.create(
      model=modelo,
      voice=voz,
      input=texto,
  )

  response.stream_to_file(nome_arquivo)
  speak()

#----begin of speaking code------#
import time
from pygame import mixer

def playaudio(filename):
    #os.system('ffplay -nodisp -autoexit -loglevel quiet '+filename)  # Play 
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.5)

def speak():

    response=("output.mp3")
    playaudio(response) #changed from ffmpeg to pygame play audio mp3;

    #os.system('ffmpeg -loglevel quiet -i /tmp/response.wav -af "asetrate=44100*0.5,atempo=1.8" /tmp/response_mod.wav')
    #os.system('ffplay -nodisp -autoexit -loglevel quiet '+response_mod)  # Play 
    #os.remove(response_mod)
    #os.remove(response)

#wake and listen----------------------
#--not used in this program
def listen():
    # Initialize speech recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recog = False
    text = ""
    while(True):
        try: 
            with sr.Microphone() as source:
       
                print("System: Listening...:")
                audio = recognizer.listen(source,timeout=2)
                print("System: Recognizing...")
                text = recognizer.recognize_google(audio, language=config.language)
                recog = True
                print("System: heard...")
                return text
        
        except sr.WaitTimeoutError:
            print("System: Timeout, no speak recognized")
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
        except sr.RequestError as e:
            print("System: No result in recognizing; {0}".format(e))
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
        except sr.UnknownValueError:
            print("System: Sorry, I didn't understand that")
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
    return text


#listen()

#--not used in this program
class WakeWord:
    def __init__(self):
        self.wakeup = False
    def start_wake_thread(self):
        self.thread = Thread(target=self.wake)
        self.thread.daemon = True
        self.thread.start()
    def wake(self):    
        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(access_key=PORCUPINE_KEY,keywords=["jarvis", "blueberry"])
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                            rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=porcupine.frame_length)
            while True:
                self.wakeup =False
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("System: Hotword Detected")
                    self.wakeup = True
                    return self.wakeup
        finally:
            if porcupine is not None:  #todo stop thread ?
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()
wake_word_instance = WakeWord()


