from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.list import OneLineIconListItem, MDList
import json
from difflib import get_close_matches
from PyDictionary import PyDictionary
from kivymd.app import MDApp
from translate import Translator
from kivy.core.window import Window
from kivymd.uix.list import TwoLineListItem
from grammar import *
import pyttsx3
import webbrowser
import datetime
import speech_recognition as sr
import os
import wikipedia
import webbrowser
dictionary = PyDictionary()

Window.size=(310,500)

engine = pyttsx3.init('sapi5', debug=True)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)




class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()



class TestNavigationDrawer(MDApp):
    namee = ObjectProperty()
    def build(self):
        kv= Builder.load_file("screenmd.kv")

        return kv

    def speak(self,audio):
        engine.say(audio)
        engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        self.root.ids.top.text = "listening...."
        self.speak('we are listening')

        with sr.Microphone() as source:
            r.energy_threshold = 10000
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')
            self.root.ids.namee.text = query

        except sr.UnknownValueError:
            self.root.ids.top.text = 'Sorry sir! I didn\'t get that! Try typing the word!'
            self.speak('Sorry sir! I didn\'t get that! Try typing the word!')



    def submit(self):
        self.root.ids.top.text = "Please enter a word to find its meaning"
        word = self.root.ids.namee.text
        ans = dictionary.meaning(word)
        data = json.load(open("data.json"))
        c = word.lower()
        d = word.upper()
        e = word.capitalize()
        if ans:
            x = ans.keys()
            y =[]
            for i in x:
                y.append(i)
            z = ans[y[0]][:2]
            w = ",".join(z)
            self.output = "{}: {}".format(y[0],w)
            self.root.ids.mean.text = self.output
        elif c in data:
            self.root.ids.mean.text = str(data[c][0])
        elif d in data:
            self.root.ids.mean.text = str(data[c][0])
        elif e in data:
            self.root.ids.mean.text = str(data[c][0])
        elif len(get_close_matches(word,data.keys())) > 0 :
            self.speak("did you mean %s" % get_close_matches(word, data.keys())[0])
            self.root.ids.top.text  = str("did you mean %s" % get_close_matches(word, data.keys())[0])
        else:
            self.root.ids.top.text = "We Didnt Get you Sir "
            self.speak("We didnt get you sir")
            self.root.ids.mean.text = ""


        '''
        data = json.load(open("data.json"))
        c = word.lower()
        d = word.upper()
        e = word.capitalize()
        if c in data:
            self.root.ids.mean.text = str(data[c][0])
        elif d in data:
            self.root.ids.mean.text = str(data[c][0])
        elif e in data:
            self.root.ids.mean.text = str(data[c][0])
        elif len(get_close_matches(word,data.keys())) > 0 :
            self.speak("did you mean %s" % get_close_matches(word, data.keys())[0])
            self.root.ids.top.text  = str("did you mean %s" % get_close_matches(word, data.keys())[0])
        '''
        '''
        else:
            self.root.ids.top.text = "We Didnt Get you Sir "
            self.speak("We didnt get you sir")
            self.root.ids.mean.text = ""
        '''



    def add(self):
        if len(self.root.ids.mean.text) == 0:
            self.root.ids.top.text = "Pls select a word first"
        else:

            with open("a.txt",'a') as x:
                x.write("{}:{}\n".format(self.root.ids.namee.text,self.output))
            self.root.ids.top.text = "Word added successfully"

    def pronounse(self):
        print(self.output,type(self.output))
        self.speak("meaning of {} is  {}".format(self.root.ids.namee.text,self.output[1:]))



    def anto(self):

        dictionary = PyDictionary(self.root.ids.antosyno.text)
        word = str(self.root.ids.antosyno.text)
        synonym = list(dictionary.getAntonyms())
        d = synonym[0][word][:4]
        e = ",".join(d)

        self.root.ids.antosynom.text = e
        self.speak(e)

    def syno(self):

        dictionary = PyDictionary(self.root.ids.antosyno.text)
        word = str(self.root.ids.antosyno.text)
        synonym = list(dictionary.getSynonyms())
        d = synonym[0][word][:4]
        e = ",".join(d)
        self.root.ids.antosynom.text = e
        self.speak(e)

    def spain(self):
        sentence = str(self.root.ids.translate.text)
        translator = Translator(to_lang= "spanish") # to spanish language
        text = translator.translate(sentence)
        self.root.ids.trans.text = text
        self.speak(text)


    def french(self):
        sentence = str(self.root.ids.translate.text)
        translator = Translator(to_lang= "french") # to spanish language
        text = translator.translate(sentence)
        self.root.ids.trans.text = text
        self.speak(text)


    def german(self):
        sentence = str(self.root.ids.translate.text)
        translator = Translator(to_lang= "german") # to spanish language
        text = translator.translate(sentence)
        self.root.ids.trans.text = text
        self.speak(text)

    def japan(self):
        sentence = str(self.root.ids.translate.text)
        translator = Translator(to_lang= "japanese") # to spanish language
        text = translator.translate(sentence)
        self.root.ids.trans.text = text
        self.speak(text)

    def favourites(self):

        c = []
        d = []
        c.append(self.root.ids.namee.text)
        d.append(self.output)

        for i in range(len(c)):
            item = TwoLineListItem(text='{}'.format(c[i]),secondary_text = "{}".format(d[i]))
            self.root.ids.container.add_widget(item)
        self.speak("word added successfully")


    def check_grammar(self):
        sentence = self.root.ids.gramm.text
        checked  = main(sentence)
        if sentence == checked:
            self.root.ids.let.text = "Correct Sentense!!!"
            self.speak(root.ids.let.text)
        else:
            self.root.ids.let.text = checked
            self.speak(self.root.ids.let.text)

    def greet_me(self):
        current = int(datetime.datetime.now().hour)
        if current>= 0 and current<12:
            self.speak('Good Morning')
        elif current >= 12 and current < 18 :
            self.speak('good Afternoon')
        elif current >=18 and current < 20:
            self.speak('good evening')
        else:
            self.speak('good nighht')



    def lets_chat(self):
        def listen_below():
            r = sr.Recognizer()
            self.root.ids.top.text = "listening...."
            self.speak('we are listening')

            with sr.Microphone() as source:
                r.energy_threshold = 10000
                audio = r.listen(source)

            try:
                query = r.recognize_google(audio, language='en-in')
                print('User: ' + query + '\n')
                return query


            except sr.UnknownValueError:
                self.root.ids.top.text = 'Sorry sir! I didn\'t get that! Try typing the word!'
                self.speak('Sorry sir! I didn\'t get that! Try typing the word!')
                s = input()
                return s
        query = listen_below()


        if "meaning" in query:
            c = query[-1]
            dictionary = PyDictionary(c)
            ans = dictionary.meaning(c)
            if ans:

                x = ans.keys()
                y =[]
                for i in x:
                    y.append(i)
                z = ans[y[0]][:2]
                w = ",".join(z)

                hey = "{}: {}".format(y[0],w)
                self.speak(hey)
            else:
                self.speak("We didnt got you sir")

        elif "synonym" in query:
            c = query[-1]
            dictionary = PyDictionary(c)
            synonym = list(dictionary.getSynonyms())
            d = synonym[0][c][:4]
            e = ",".join(d)
            self.root.ids.antosynom.text = e
            self.speak(e)

        elif "antononym"  in query:
            c = query[-1]
            dictionary = PyDictionary(query[-1])
            synonym = list(dictionary.getAntonyms())
            d = synonym[0][c][:4]
            e = ",".join(d)
            self.speak(e)

        elif "about " in query:
            self.speak("This A dictionary application which is a listing of words in one or more specific languages, often arranged alphabetically (or by radical and stroke for ideographic languages), which may include information on definitions, usage, etymologies, pronunciations, translation")

        elif "features" in query:
            self.speak("This Dictionary application consists of listed features such as pronunciation of an entered word,Translations of word or sentence  into four languages that is Spanish,French,German,japenese,antononyms and synonyms of an word , there is also spelling checker as well as grammar checker into this application which corrects a sentence  and there is also an AI bot named pam which helps in assisting the user")

        elif "english" in query:
            self.speak("English may not be the most spoken language in the world, but it is the official language of 53 countries and spoken by around 400 million people across the globe. Being able to speak English is not just about being able to communicate with native English speakers, it is the most common second language in the world. If you want to speak to someone from another country then the chances are that you will both be speaking English to do this.")

        elif "created" in query:
            self.speak("this application is created in using KivyMD is a collection of Material Design compliant widgets for use with Kivy, a framework for cross-platform, touch-enabled graphical applications. The project's goal is to approximate Google's Material Design spec as close as possible without sacrificing ease of use or application performance")


        elif "gmail" in query:
            self.speak('okay')
            webbrowser.open('www.gmail.com')

        elif 'open hackerrank' in query:
            self.speak('okay')
            webbrowser.open('https://www.hackerrank.com')

        elif 'open interviewbit' in query:
            self.speak('okay')
            webbrowser.open('https://www.interviewbit.com/profile')

        elif 'open leetcode' in query:
            self.speak('okay')
            webbrowser.open('https://leetcode.com')

        elif 'open chrome' in query:
            self.speak('okay')
            webbrowser.open('www.google.com')


        elif 'open github' in query:
            self.speak('okay')
            webbrowser.open('https://github.com')
        else:

            query = query
            self.speak('Searching...')
            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak('Got it.')
                self.speak('WIKIPEDIA says - ')
                self.speak(results)
            except:
                webbrowser.open('www.google.com')




    def intro(self):
        self.greet_me()
        self.speak(' Hello  my name is pam.   i   am   your   digital   assistant')
        self.speak(' how may i help you sir')









TestNavigationDrawer().run()
