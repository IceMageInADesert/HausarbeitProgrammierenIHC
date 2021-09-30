import deepl
from libretranslatepy import LibreTranslateAPI
from googletrans import Translator
from nltk.translate.bleu_score import sentence_bleu
import time
import glob
import os
import re


def BleuScoreCalculatorIntro():
    Referenzreinmachen=True
    while Referenzreinmachen==True:
        print("Bitte geben Sie Ihre Referenz-Übersetzung in den Referenzordner. Wenn sie fertig sind, drücken Sie Enter.")
        input()
        referenz=[os.path.basename(x) for x in glob.glob("Referenzen/*.txt")]
        if len(referenz) > 1:
            Referenzlisteerstellen(referenz)
        elif len(referenz)==1:
            datei=glob.glob("Referenzen/*.txt")
            for titel in datei:
                with open(titel, "r", encoding="utf8") as f:
                    rf=f.read()
                    rx=re.compile("\W+")
                    ref=rx.sub(" ", rf).strip()
                    refdone=ref.split()
                    BleuScoreKandidatwahl(refdone)
        else:
            print("Sie haben keine Referenz-Übersetzung im Ordner")
        
        
def Referenzlisteerstellen(referenz):
    nochmal=True
    while nochmal==True:
        referenzlist=[]
        print("Es wurden mehrere Referenzdateien gefunden. Welche möchten Sie verwenden? \n Bitte geben Sie nur eine Datei pro Eingabeaufforderung an. \n Wenn Sie die Auswahl beenden möchten, drücken Sie einfach Eingabe")
        listefüllen=True
        nochmal=False
        while listefüllen==True:
            print(referenz)
            referenzeingabe=input()
            if referenzeingabe in referenz:
                with open("Referenzen/"+ referenzeingabe, "r", encoding="utf8") as f:
                    rf=f.read()
                    if rf not in referenzlist:
                        referenzlist.append(rf)
                        print(referenzlist)
                    elif rf in referenzlist:
                        print("Diese Datei verwenden Sie bereits")
            elif referenzeingabe=="":
                print("Möchten Sie aufhören? Y/N")
                chontinue=False 
                while chontinue==False:
                    abbrechenpre=input()
                    abbrechen=abbrechenpre.lower()
                    if abbrechen=="y" or abbrechen=="ja" or abbrechen=="yes" or abbrechen=="j":
                        listefüllen=False
                        print("Möchten Sie diese Liste behalten oder neu anfangen?")
                        listewegmach2=input()
                        listewegmach=listewegmach2.lower()
                        if listewegmach=="behalten":
                            chontinue=True
                            print("Verstanden")
                            BleuScoreCleanup(referenzlist)
                        elif listewegmach=="neu" or listewegmach=="neu anfangen":
                            chontinue=True
                            nochmal=True
                            listefüllen=False
                        else:
                            print("Bitte geben Sie \"behalten\" oder \"neu\" an.")
                    elif abbrechen=="n" or abbrechen=="nein" or abbrechen=="no":
                        print("Alles klar")
                        chontinue=True
                    else:
                        print("Bitte geben Sie \"Ja\" oder \"Nein\" an.")
                else:
                    print("Bitte geben Sie Namen der Übersetzungen an, die Sie verwenden möchte.")

def BleuScoreCleanup(referenzlist):
    referenzlistclean=[]
    rx=re.compile("\W+")
    for i in referenzlist:
        res=rx.sub(" ", i).strip()
        referenzlistclean.append(res)
    BleuScoreSplit(referenzlistclean)
    
def BleuScoreSplit(referenzlist):
    referenzlistsplit=[]
    for i in referenzlist:
        ineu=i.split()
        referenzlistsplit.append(ineu)
    print(referenzlistsplit)
    BleuScoreKandidatwahl(referenzlistsplit)
    
def BleuScoreKandidatwahl(referenz):
    Maschinenwahl=True
    print("Bitte geben Sie an, welche Übersetzung Sie durch die Referenz überprüfen lassen wollen.")
    print("Eine Übersetzung von Google, DeepL oder LibreTranslate?")
    while Maschinenwahl==True:
        MTchoice2=input()
        MTchoice=MTchoice2.lower()
        if MTchoice=="google" or MTchoice=="g":
            MTchoice="Google"
            BleuScoreCalculator(MTchoice, referenz)
            
        elif MTchoice=="deepl" or MTchoice=="deep":
            MTchoice="DeepL"
            BleuScoreCalculator(MTchoice, referenz)
            
        elif MTchoice=="libretranslate" or MTchoice=="lt" or MTchoice=="libre":
            MTchoice="LibreTranslate"
            BleuScoreCalculator(MTchoice, referenz)
            
        else:
            print("Bitte wählen Sie entweder \"Google\" oder \"DeepL\" oder \"LibreTranslate\".")
    
    
def BleuScoreCalculator(MTchoice, referenz):
    rx=re.compile("\W+")
    ordnerÜ=[os.path.basename(x) for x in glob.glob("Übersetzungen/"+MTchoice+"/*.txt")]
    if len(ordnerÜ) > 1:
        print("Bitte wählen Sie eine Übersetzung aus.\n"+ordnerÜ)
        Üwahl=True
        while Üwahl == True:
            print(ordnerÜ)
            kandidatÜ=input()
            if kandidatÜ in ordnerÜ:
                print("Möchten Sie \""+kandidatÜ+"\" für den BLEU-Score verwenden? Y/N")
                Choice1=input()
                Choice=Choice1.lower()
                if Choice=="y" or Choice=="yes" or Choice=="ja" or Choice=="j":
                    print("Alles klar.")
                    with open("Übersetzungen/"+MTchoice+"/"+kandidatÜ, "r", encoding="utf8") as f:
                        rf=f.read()
                        ref=rx.sub(" ", rf).strip()
                        kandidat=ref.split()
                        print("Bleu-Score: "+str(sentence_bleu([referenz], kandidat)))
                        input("Drücken Sie Eingabe, um zum Hauptmenü zurückzugelangen")
                        main()
                elif Choice=="n" or Choice=="nein" or Choice=="no":
                    print("Bitte wählen Sie eine Übersetzung aus.")
            else:
                print("Bitte geben Sie eine Übersetzung aus dem Ordner an.\n"+ordnerÜ)
    elif len(ordnerÜ) < 1:
        print("Sie haben keine Übersetzung in diesem Ordner.")
        time.sleep(1)
        BleuScoreKandidatwahl(referenz)
            
    elif len(ordnerÜ)==1:
        datei=glob.glob("Übersetzungen/"+MTchoice+"/*.txt")
        for titel in datei:
            with open(titel, "r", encoding="utf8") as f:
                rf=f.read()
                ref=rx.sub(" ", rf).strip()
                kandidat=ref.split()
                print("Bleu-Score: "+ str(sentence_bleu([referenz], kandidat)))
                input("Drücken Sie Eingabe, um zum Hauptmenü zurückzugelangen")
                main()


def Übersetzenlassen():
    Sprachenliste={"Englisch": "en", "Arabisch": "ar", "Chinesisch": "zh", "Niederländisch": "nl", "Finnisch": "fi", "Französisch": "fr", "Deutsch": "de", "Hindi": "hi", "Ungarisch": "hu", "Indonesisch": "id", "Gälisch": "ga", "Italienisch": "it", "Japanisch": "ja", "Koreanisch": "ko", "Polnisch": "pl", "Portugiesisch": "pt", "Russisch": "ru", "Spanisch": "es", "Schwedisch": "sv", "Türkisch": "tr", "Ukrainisch": "uk", "Vietnamesisch": "vi"}
    print("Bitte geben Sie den Text ein, den Sie übersetzen lassen möchten:")
    Textauswahl=False
    while Textauswahl==False:
        AT=input()#AT=Ausgangstext
        print("Möchten Sie diesen Text übersetzen?")
        Choice2=input()
        Choice=Choice2.lower()
        if Choice=="y" or Choice=="yes" or Choice=="ja" or Choice=="j":
            print("Welches Tool möchten Sie benutzen? DeepL, Google Translate oder LibreTranslate? \n")
            Toolwahltoggle=False
            while Toolwahltoggle == False:
                Toolwahl=input()
                Toolwahl=Toolwahl.lower()
                if Toolwahl=="google" or Toolwahl=="gt":
                    Toolwahl="Google"
                    Translatorallgemein(AT, Sprachenliste, Toolwahl)
            
                elif Toolwahl=="deepl" or Toolwahl=="deep":
                    Toolwahl="DeepL"
                    Translatorallgemein(AT, Sprachenliste, Toolwahl)
                
                elif Toolwahl=="libretranslate" or Toolwahl=="lt":
                    Toolwahl="LibreTranslate"
                    Translatorallgemein(AT, Sprachenliste, Toolwahl)
            
                else:
                    print("Bitte geben Sie eine der Tools an.")
        elif Choice=="n" or Choice=="nein" or Choice=="no":
            print("Bitte geben Sie den Text ein, den Sie übersetzen lassen möchten:")

def Translatorallgemein(AT, Sprachenliste, Toolwahl):
    dl=deepl.Translator("916661")
    lt=LibreTranslateAPI("https://translate.astian.org/")
    gt=Translator()
    print("In welcher Sprache ist der Ausgangstext verfasst?")
    Sprachangabe=False
    while Sprachangabe==False:
        ATSprache3=input()
        ATSprache2=ATSprache3.lower()
        ATSprache=ATSprache2.capitalize()
        if ATSprache in Sprachenliste.keys(): 
            print("Und in welche Sprache möchten Sie es übersetzen lassen?")
            Sprachangabe=True
            Sprachauswahl=False
            while Sprachauswahl == False:
                ZTSprache3=input()
                ZTSprache2=ZTSprache3.lower()
                ZTSprache=ZTSprache2.capitalize()
                if ZTSprache in Sprachenliste.keys():
                    Sprachauswahl = True
                    if Toolwahl=="Google":
                        ÜGoogle=gt.translate(AT, src=Sprachenliste[str(ATSprache)], dest=Sprachenliste[str(ZTSprache)])
                        test=str(ÜGoogle)
                        test2=test.replace("Translated(src="+Sprachenliste[ATSprache]+", dest="+Sprachenliste[ZTSprache]+", text=", "")
                        test3=test2.replace(", pronunciation="+AT+", extra_data=\"{'translat...\")", "")
                        print("Möchten Sie die Übersetzung abspeichern? Y/N")
                        Choice=input()
                        if Choice=="y" or Choice=="yes" or Choice=="ja" or Choice=="j":
                            filename=input("Geben Sie der Datei einen Namen:\n")
                            with open("Übersetzungen/Google/"+filename+".txt", "w", encoding="utf8") as a:
                                a.write(test3)
                        elif Choice=="n" or Choice=="nein" or Choice=="no":
                            input("Drücken Sie Eingabe, um zum Hauptmenü zurückzugelangen")
                            main()
                    elif Toolwahl=="LibreTranslate":
                        print(Sprachenliste[ZTSprache])
                        ÜLibre=lt.translate(AT, Sprachenliste[ATSprache], Sprachenliste[ZTSprache])
                        print(ÜLibre)
                        print("Möchten Sie die Übersetzung abspeichern? Y/N")
                        Choice=input()
                        if Choice=="y" or Choice=="yes" or Choice=="ja" or Choice=="j":
                            filename=input("Geben Sie der Datei einen Namen:\n")
                            with open("Übersetzungen/LibreTranslate/"+filename+".txt", "w", encoding="utf8") as a:
                                a.write(ÜLibre)
                        elif Choice=="n" or Choice=="nein" or Choice=="no":
                            input("Drücken Sie Eingabe, um zum Hauptmenü zurückzugelangen")
                            main()
                    elif Toolwahl=="DeepL":
                        ÜDeep=dl.translate_text(AT, target_lang=Sprachenliste[ZTSprache])
                        print(ÜDeep)
                        print("Möchten Sie die Übersetzung abspeichern? Y/N")
                        Choice=input()
                        if Choice=="y" or Choice=="yes" or Choice=="ja" or Choice=="j":
                            filename=input("Geben Sie der Datei einen Namen:\n")
                            with open("Übersetzungen/DeepL/"+filename+".txt", "w", encoding="utf8") as a:
                                a.write(ÜDeep)
                        elif Choice=="n" or Choice=="nein" or Choice=="no":
                            input("Drücken Sie Eingabe, um zum Hauptmenü zurückzugelangen")
                            main()
                    
                elif ZTSprache not in Sprachenliste.keys():
                    print("Bitte wählen Sie eine Sprache aus dieser Liste: \n", Sprachenliste.keys())
        else:
            print("Bitte wählen Sie eine Sprache aus dieser Liste: \n", Sprachenliste.keys())


def main():
    print("Herzlich Willkommen zum Online-Übersetzerprogramm. Wollen Sie den \"BLEU-Score\" für einen Übersetzer berechnen oder wollen\nSie etwas simultan \"übersetzen lassen\"?")
    time.sleep(2)
    Umw = False
    while Umw == False:
        Untermenüwahl=input()
        Untermenüwahl=Untermenüwahl.lower()
        if Untermenüwahl=="bleu-score" or Untermenüwahl=="bleu":
            BleuScoreCalculatorIntro()
        elif Untermenüwahl=="übersetzen lassen" or Untermenüwahl=="übersetzen" or Untermenüwahl=="ü":
            Übersetzenlassen()
        else:
            print("Bitte geben Sie entweder \"BLEU-Score\" oder \"Übersetzen\" als Befehl ein")
            
    
main()