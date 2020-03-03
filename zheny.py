import os
import time
import speech_recognition as sr    # spetch recognition modul
from fuzzywuzzy import fuzz        # нечёткое старанение
from fuzzywuzzy import process     # нечёткое старвнение
import pyttsx3         # spetch modul
import datetime        # 

opts = {
    "name_assistant": ('евгений', 'женя', 'женёк', 'жека'),
    "tbr": ('скажи','расскажи','покажи','произнеси'),
    "cmds": {
        "time": ('текущее время','сейчас время','который час','сколько время'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "witcher": ('изобрази ведьмака', 'изобрази геральта')
    }
}


# Function
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

# 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["name_assistant"]):
            # address to Zheny
            cmd = voice

            for x in opts['name_assistant']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # recognize and execute
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

# поиск нечётких команд
def recognize_cmd(cmd):  
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

# преобразовываем команду в действие
def execute_cmd(cmd):
    if cmd == 'time':
        # tell time
        print("hello")
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # start radio
        os.system("D:\\Zheny\\res\\radio_record.m3u")

    elif cmd == 'witcher':
        # Zaraza
        speak("Fuck")

    else:
        print('команда не распознана, повторите!')

# launch
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)

with m as source:
    r.adjust_for_ambient_noise(source) # слушаем фон

speak_engine = pyttsx3.init()

# The voice that the assistant says
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id) # указываем голос которым он будет говорить

speak("Привет")
speak("Я слушаю")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # бесконечный цикл