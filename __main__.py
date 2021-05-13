import random

import speech_recognition as sr
import PySimpleGUI as sg
import pronouncing


if __name__ == "__main__":
    r = sr.Recognizer()

    layout = [[sg.Text("Please record a your desired word within 2 seconds!")],
              [sg.Text('Number of Rhymes to be outputted (default is 5)')],
              [sg.Input(key='-NUM-')],
              [sg.Button('Record'),
               sg.Button('Quit')],
              [sg.Text(size=(40,1), key='-IN WORD-')],
              [sg.Text(size=(40,1), key='-RHYMES_PRE-')],
              [sg.Text(size=(40,1), key='-RHYMES-')]]

    window = sg.Window('Welcome to Rhyme-er', layout, size=(400, 300))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == 'Record':
            num_rhymes = int(values['-NUM-'] or 5)
            with sr.Microphone() as source:
                audio = r.listen(source, phrase_time_limit=2)

            try:
                word = r.recognize_google(audio)
                window['-IN WORD-'].update(f"You said \"{word}\"")
                all_rhymes = pronouncing.rhymes(word)
                window['-RHYMES_PRE-'].update(f"{num_rhymes} possible rhymes are: ")
                window['-RHYMES-'].update(", ".join(random.sample(all_rhymes, num_rhymes)))
            except (LookupError, sr.UnknownValueError) as e:
                window['-RHYMES-'].update("Uh oh, your word was not recognized. Please try again!")
