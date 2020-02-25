from pydub import AudioSegment
import speech_recognition as sr


def extractTextFromAudio(file):
        text = ''
        wavFile = file
        if file[-3:] in ['mp3', 'MP3']:
                sound = AudioSegment.from_mp3(file)
                wavFile = file[:-3]+'wav'
                sound.export(wavFile, format="wav")
        r = sr.Recognizer()
        with sr.AudioFile(wavFile) as source:
                audio = r.record(source)
                text = r.recognize_google(audio)
        return text