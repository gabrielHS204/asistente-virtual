import speech_recognition as sr
import pyttsx3
import webbrowser
import random


class Assistente:
    def __init__(self, assistente_nome, person):
        self.assistente_nome = assistente_nome
        self.person = person
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.voice_data = ""

    def engine_speak(self, text):
        """Fala usando o pyttsx3"""
        self.engine.say(text)
        self.engine.runAndWait()
        print(f"{self.assistente_nome}: {text}")

    def record_audio(self, ask=""):
        """Escuta a entrada de voz"""
        with sr.Microphone() as source:
            print("ouvindo...")
            self.engine_speak(ask)

            try:
                audio = self.r.listen(source, timeout=10, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                self.engine_speak("Você não falou nada. Tente novamente.")
                return ""

        print("processando...")

        try:
            self.voice_data = self.r.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
            self.engine_speak(f"Desculpe {self.person}, não entendi. Pode repetir?")
            return ""
        except sr.RequestError:
            self.engine_speak("Erro ao conectar com o serviço de reconhecimento.")
            return ""

        print(">>", self.voice_data.lower())
        return self.voice_data.lower()

    def there_exist(self, terms):
        """Verifica se alguma palavra existe na frase"""
        for term in terms:
            if term in self.voice_data:
                return True
        return False

    def render(self, voice_data):
        """Processa os comandos"""
        self.voice_data = voice_data.lower()

        if self.there_exist(['oi', 'olá', 'eai', 'hey']):
            greetings = [
                f"Oi {self.person}, como posso ajudar?",
                "Olá chefe, como posso ajudar?",
                "Oi, o que você quer?",
                "Olá, como você está?",
                f"Olá {self.person}, como posso ajudar?"
            ]
            self.engine_speak(random.choice(greetings))

        elif self.there_exist(['pesquise', 'pesquisar no']) and 'youtube' not in self.voice_data:
            search_term = self.voice_data
            search_term = search_term.replace("pesquisar no google", "")
            search_term = search_term.replace("pesquisar no", "")
            search_term = search_term.replace("pesquisar", "")
            search_term = search_term.strip()

            if search_term == "":
                self.engine_speak("O que você quer que eu pesquise no Google?")
            else:
                url = f'https://www.google.com/search?q={search_term}'
                webbrowser.open(url)
                self.engine_speak(f"Aqui está o que encontrei sobre {search_term} no Google.")

        elif self.there_exist(['youtube', 'pesquisar no youtube']):
            search_term = self.voice_data
            search_term = search_term.replace("pesquisar no youtube", "")
            search_term = search_term.replace("youtube", "")
            search_term = search_term.replace("pesquisar", "")
            search_term = search_term.strip()

            if search_term == "":
                self.engine_speak("O que você quer que eu pesquise no YouTube?")
            else:
                url = f'https://www.youtube.com/results?search_query={search_term}'
                webbrowser.open(url)
                self.engine_speak(f"Aqui está o que encontrei sobre {search_term} no YouTube.")

        elif self.there_exist(['tchau', 'sair', 'fechar', 'desligar', 'desliga']):
            self.engine_speak("Tchau, até mais!")
            exit()


# ==== EXECUÇÃO ====

virtual_assist = Assistente('Luna', 'Gabriel')

while True:
    voice_data = virtual_assist.record_audio("Estou ouvindo...")
    if voice_data == "":
        continue

    virtual_assist.render(voice_data)
