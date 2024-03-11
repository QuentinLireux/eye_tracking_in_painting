import os
import pyttsx3




def read_painting_description(text):
    subdir_path = os.path.join("oeuvres")

    file_path = os.path.join(subdir_path, f"{text}.txt")

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            
            engine = pyttsx3.init()
            ##engine.say(text_content) Faire parler l'audio
            engine.save_to_file(text_content, f'oeuvres/{text}.mp3')
            engine.runAndWait()
    else:
        print(f"Le fichier {text}.txt n'existe pas dans le répertoire {subdir_path}")



read_painting_description("SAINT_JEROME_A_L_ETUDE")