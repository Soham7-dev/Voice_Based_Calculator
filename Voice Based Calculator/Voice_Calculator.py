from tkinter import *
from PIL import Image, ImageTk #pip install pillow
import os
import  pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import time
import re
from math import *

def speak( audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice = engine.setProperty('voice', voices[1].id)
    rate = engine.setProperty('rate', 160)
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(e)


def myCommand():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio_data = r.listen(source, timeout= 5.0)
            query = r.recognize_google(audio_data, language= 'en-in')
            return query
    except sr.UnknownValueError:
        return "Can't recognize your speech..."
    except sr.RequestError:
        return "No internet connection !"
    except TimeoutError:
        return "Taking too much time :("


def Calculator():

    '''Returns a value rounded up to a specific number of decimal places'''

    def round_decimals_up(number: float, decimals: int = 2):

        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return ceil(number)

        factor = 10 ** decimals
        return ceil(number * factor) / factor

    '''Counting the number places after decimal'''

    def num_after_point(x):
        s = str(x)
        if not '.' in s:
            return 0

        return len(s) - s.index('.') - 1

    '''Taking the raw Query'''

    query = myCommand()
    query = query.lower()
    print(query)

    '''Words that might be present in the Query'''

    add = ['+', 'add', 'sum', 'addition', 'plus']
    dif = ['-', 'difference', 'subtract', 'minus']
    mul = ['into', 'multiply', 'multiplication', 'times', 'x']
    div = ['divided', 'by', '/', 'divide', 'division']
    square_and_square_root = ['square']
    cube_and_cube_root = ['cube']
    power = ['power']
    factorial_value = ['factorial']
    sin_value = ['sin', 'sign']
    cos_value = ['cos']
    tan_value = ['tan']
    logarithm = ['log', 'logarithm']

    '''Sorting out the Query'''

    try:
        for i in query.split(' '):
            if i in add:
                query = query.replace('and', '+')
                query = query.replace('with', '+')
                query = query.replace('plus', '+')
                print(query)
                query = re.sub('[a-z]', '', query)
                print(query)

            elif i in dif:
                query = query.replace('and', '-')
                print(query)
                query = re.sub('[a-z]', '', query)
                print(query)

            elif i in mul:
                query = query.replace('into', '*')
                query = query.replace('and', '*')
                query = query.replace('with', '*')
                query = query.replace('x', '*')
                print(query)
                query = re.sub('[a-z]', '', query)
                print(query)

            elif i in div:
                query = query.replace('divided by', '/')
                query = query.replace('divided /', '/')
                query = query.replace('divided', '/')
                query = query.replace('division', '/')
                query = query.replace('by', '/')
                print(query)
                query = re.sub('[a-z]', '', query)
                print(query)

            elif i in sin_value:
                query = re.sub('[a-z]', '', query)
                query = 'sin(radians(' + query + '))'
                print(query)

            elif i in cos_value:
                query = re.sub('[a-z]', '', query)
                query = 'cos(radians(' + query + '))'
                print(query)

            elif i in tan_value:
                query = re.sub('[a-z]', '', query)
                query = 'tan(radians(' + query + '))'
                print(query)

            elif i in power:
                query = query.replace('power', '**')
                query = re.sub('[a-z]', '', query)
                print(query)

            elif i in factorial_value:
                query = re.sub('[a-z]', '', query)
                query = 'factorial(' + query + ')'
                print(query)

            elif i in square_and_square_root:
                if 'root' in query:
                    query = re.sub('[a-z]', '', query)
                    query = query.replace(' ', '')
                    query = 'sqrt(' + query + ')'
                    print(query)
                else:
                    query = re.sub('[a-z]', '', query)
                    query = query.replace(' ', '')
                    query += '**2'
                    print(query)

            elif i in cube_and_cube_root:
                if 'root' in query:
                    query = re.sub('[a-z]', '', query)
                    query = query.replace(' ', '')
                    query = query + '**(1/3)'
                    print(query)
                else:
                    query = re.sub('[a-z]', '', query)
                    query = query.replace(' ', '')
                    query += '**3'
                    print(query)

            elif i in logarithm:
                query = re.sub('[a-z]', '', query)
                query = query.replace(' ', '')
                query = 'log10(' + query + ')'
                print(query)

        q = eval(query)
        if 'radians' in query:
            query = query.replace('radians', '')
            query = query.replace('(', '', 1)
            query = query.replace(')', '', 1)
        print(q)
        d = num_after_point(q)
        if d > 3:
            speak('The answer is approximately ' + str(round_decimals_up(q)))
        elif d > 0:
            speak('That makes ' + str(q))
        else:
            speak('That makes ' + (str(q)))
        return query + ' = ' + str(q)

    except:
        speak("That's not a valid query")
        return query

class UI:
    def __init__(self):

        '''MASTER'''

        self.root = Tk()
        self.title = self.root.title('OM3GA')
        self.geo = self.root.geometry('400x500')
        self.maxsize = self.root.maxsize(width= 400, height= 500)
        self.minsize = self.root.minsize(width= 400, height= 500)

        '''DEFAULT BACKGROUND COLOR IS LIGHT'''

        self.root.configure(bg = '#d5d3f0')

        '''MESSAGE'''

        self.speech_to_text = StringVar()
        self.message = Message(self.root, textvariable=self.speech_to_text, bg='#d5d3f0', width=200, font=('Book Antiqua', 20))
        self.message.place(x = 105, y = 145)

        '''CLICKED'''

        def clicked_light_button():
            self.root.configure(bg = '#d5d3f0')
            self.message['bg'] = '#d5d3f0'
            self.message['fg'] = 'black'
            self.button_tap_to_speak['relief'] = SOLID

        def clicked_dark_button():
            self.root.configure(bg = '#1d1c2b')
            self.message['bg'] = '#1d1c2b'
            self.message['fg'] = '#e4ebe5'
            self.button_tap_to_speak['relief'] = RIDGE

        def clicked_tap_to_speak():
            self.speech_to_text.set('L i s t e n i n g...')
            self.message.after(1000, lambda: self.speech_to_text.set(Calculator()))

        '''HOVER'''

        def on_enter_light(e):
            self.button_light['bg'] = '#fff700'

        def on_leave_light(l):
            self.button_light['bg'] = 'white'

        def on_enter_dark(e):
            self.button_dark['bg'] = '#00f2ff'

        def on_leave_dark(l):
            self.button_dark['bg'] = 'white'

        def on_enter_tap_to_speak(e):
            self.button_tap_to_speak['bg'] = '#b0def7'
            self.button_tap_to_speak['fg'] = '#0f04d9'

        def on_leave_tap_to_speak(l):
            self.button_tap_to_speak['fg'] = 'black'
            self.button_tap_to_speak['bg'] = '#ebeae4'

        '''BUTTON FOR CHANGING THEME'''

        img_light = PhotoImage(file = 'light_after_clicking.png')
        self.button_light = Button(self.root, image = img_light, command = clicked_light_button, bd = 1, relief = SOLID)
        self.button_light.pack()

        img_dark = PhotoImage(file = 'black_after_cursor.png')
        self.button_dark = Button(self.root, command = clicked_dark_button, image = img_dark, bd = 1, relief = SOLID)
        self.button_dark.pack()

        self.button_light.bind('<Enter>', on_enter_light)
        self.button_light.bind('<Leave>', on_leave_light)

        self.button_dark.bind('<Enter>', on_enter_dark)
        self.button_dark.bind('<Leave>', on_leave_dark)

        '''TAP TO SPEAK BUTTON'''

        tap_to_speak_text = StringVar()
        tap_to_speak_text.set("Tap to Speak")
        img = PhotoImage(file = 'mic2.png')
        mic_icon = img.subsample(7, 7)
        self.button_tap_to_speak = Button(self.root, image = mic_icon, compound = 'left',command = clicked_tap_to_speak, textvariable = tap_to_speak_text, font = ('Comic Sans MS Bold', 11), bd = 3, relief = SOLID, bg = '#ebeae4', fg = 'black', padx = 17, pady = 8)
        self.button_tap_to_speak.place(x = 113, y = 250)

        self.button_tap_to_speak.bind('<Enter>', on_enter_tap_to_speak)
        self.button_tap_to_speak.bind('<Leave>', on_leave_tap_to_speak)

        '''MAIN LOOP'''

        self.root.mainloop()

if __name__ == '__main__':

    omega = UI()
