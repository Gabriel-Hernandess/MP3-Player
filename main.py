"""
LinkedIn: https://www.linkedin.com/in/gabriel-hernandes-4a3b8b248/
GitHub: https://github.com/Gabriel-Hernandess?tab=repositories

"""

from pygame import mixer
from tkinter import *
from PIL import ImageTk, Image
from urllib.request import urlopen
from tkmacosx import Button
import pygame
import os
import time
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from pytube import YouTube
from moviepy.video.io.VideoFileClip import *
from mutagen.id3 import ID3, APIC
import io
import speech_recognition as sr
import pyttsx3
import tkinter.ttk as ttk

"""
Observacoes: O programa foi feito de forma simples, apenas parar passar o tempo estudando e conhecendo novas ferramentas que as
libs do python e capaz, ele nao e 100%, algumas coisas claramente precisariam de muito tempo para serem feitas, como detalhes, minimizacao de janela, segundo plano, etc... 
"""

# inicializa o motor de síntese de voz
engine = pyttsx3.init()

# inicializa o microfone
r = sr.Recognizer()

# funcao para exibir info na janela de add musica
def info():
    messagebox.showinfo('Info','Cole o link do video do YouTube para baixa-lo em formato mp3 ou, arraste um arquivo ja existente para a pasta "Musics" no diretório do MP3 Player!')

# funcao para abrir txt com comandos de voz ao pressionar o botao de informacao no menu do player
def info_falar_box():
    arq = open("/Users/gabrielhernandes/Documents/MP3 Player/info.txt", 'r') 


# tocar musica selecionada
def play_song():
    global stopped
    stopped = False
    
    musica = listbox.get(ACTIVE)
    
    mp3_title['text'] = musica
    mixer.music.load(musica)
    mixer.music.play()

    # chamar funcao para pegar o tempo da musica
    tempo_musica()
    
    # remover texto para exibir apenas o titulo da musica
    mp3_guide['text'] = ''

    listbox.delete(0 , END)
    show()


global paused
paused = False

# funcoes de pausar e de unpause
def pause():
    global paused

    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True

def unpause():
    mixer.music.unpause()
    global paused 
    paused = False

global stopped
stopped = False

# funcao para parar musica
def quit_player():
    # reseta o slider do tempo
    slider.config(value=0)
    
    # limpar o texto da barra de progresso da musica
    barra.config(text='')
    
    mixer.music.stop()
    listbox.select_clear(ACTIVE)

    mp3_title['text'] = ""

    # adicionar texto para escolher uma musica
    mp3_guide['text'] = 'Escolha uma musica da lista'

    global stopped
    stopped = True

# funcao para avancar musica
def next_song():
    # se tiver pausado, ele da unpause, para nao bugar o slider e o tempo decorrido
    if paused:
        unpause()

    #reseta o slider e o text do tempo decorrido
    slider.config(value=0)
    barra.config(text='')

    # pega o index da musica, e altera para +1, para avancar um arquivo 
    tocando = mp3_title['text']
    index = musics.index(tocando)
    new = index + 1

    if new >= len(listbox.get(0, END)): # se o índice ultrapassar o tamanho da lista, volta para a primeira música
        new = 0

    musica = musics[new]
    mixer.music.load(musica)
    mixer.music.play()
    mp3_title['text'] = musica

    listbox.delete(0 , END)
    show()


# voltar musica
def back_song():
     # se tiver pausado, ele da unpause, para nao bugar o slider e o tempo decorrido
    if paused:
        unpause()

    #reseta o slider e o text do tempo decorrido
    slider.config(value=0)
    barra.config(text='')

    # pega o index da musica, e altera para -1, para voltar um arquivo
    tocando = mp3_title['text']
    index = musics.index(tocando)
    new = index - 1

    if new < 0: # se o índice for negativo, volta para a última música da lista
        new = len(listbox.get(0, END)) - 1
    
    musica = musics[new]
    mixer.music.load(musica)
    mixer.music.play()
    mp3_title['text'] = musica

    listbox.delete(0 , END)
    show()

# pegar o tempo da musica
def tempo_musica():
    # verifica se esta parado, para nao bugar o slider
    if stopped:
        return

    # pega o tempo atual do som
    tempo_atual = pygame.mixer.music.get_pos() / 1000
    
    # converter o formato de tempo
    tempo_convert = time.strftime('%M:%S', time.gmtime(tempo_atual))
    
    # pega o tamanho do som pelo mutagen e por fim o converte em minutos e segundos
    atual_song = mp3_title['text']
    song_mutagen = MP3(atual_song)
    global music_length
    music_length = song_mutagen.info.length
    tempo_convert_length = time.strftime('%M:%S', time.gmtime(music_length))
    
    # avanca 1 para sincronizar o tempo
    tempo_atual += 1

    if int(slider.get()) == int(music_length):
        next_song()

    elif paused == True:
        pass

    elif int(slider.get()) == tempo_atual:
        slider_position = int(music_length)
        slider.config(to=slider_position, value=int(tempo_atual))
    
    else:
        slider_position = int(music_length)
        slider.config(to=slider_position, value=int(slider.get()))
        
        # exibe o tempo na barra
        tempo_convert = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        barra.config(text=f'Decorrido {tempo_convert} de {tempo_convert_length}')

        #avanca a barra com o tempo atual + 1
        prox = int(slider.get()) + 1
        slider.config(value=prox)
    
    barra.after(1000, tempo_musica)


# cria funcao para abrir janela de adicionar musica:
def add_music_window():
    add_window = tk.Toplevel()
    add_window.title('Add musics')
    add_window.geometry('800x800')

    # criar frame de menu
    top_color = Label(add_window, bg='gray13', width=150, height=2).pack(side=TOP)

    # cria funcao para fechar janela
    def quit_add_music():
        add_window.destroy()
        listbox.delete(0, END)
        show()
    
    # adiciona botao para fechar janela, chamando a funcao acima.
    quit_add_music_btn = Button(add_window, text='Quit', highlightbackground='gray13', command=quit_add_music, bg='white', relief=RAISED, overrelief=RIDGE).place(x=10, y=5)
    
    # adiciona botao para informacao
    info_btn = Button(add_window, text='Info', command=info, highlightbackground='gray13', bg='white', highlightcolor='black', relief=RAISED, overrelief=RIDGE).place(x=690, y=5)

    # criar frame para buscar video
    mp3_download = Label(add_window, width=65, height=35, bg='gray15').place(x=100, y=60)

    # cria barra de entrada do link
    video_title_search = Entry(add_window, bg='white', fg='black', width=50)
    video_title_search.place(x=120, y=90)

    # label para informar a insercao do link
    video_title_info = Label(add_window, text='Insira o link do video', fg='white').place(x=310, y=65)

    
    # cria funcao pytube para baixar o video, para depois converte-lo
    def download_mp3():
        url = YouTube(str(video_title_search.get()))
        
        video_mp4 = url.streams.get_highest_resolution().download(filename=url.title, output_path='/Users/gabrielhernandes/Documents/MP3 Player/Musics')

        audio = AudioFileClip(video_mp4)
        audio_filename = url.title+'.mp3'
        audio.write_audiofile(audio_filename)
        
        os.remove(video_mp4)
        messagebox.showinfo('Done!','O download foi realizado! Aguarde alguns segundos e aperte "Quit" para voltar ao menu.')

        listbox.delete(0, END)
        show()
        app.update()

    # exibe o video a ser baixado
    def show_video():
        url = YouTube(str(video_title_search.get()))

        Button(add_window, text='Download', command=download_mp3, bg='white', fg='black').place(x=330, y=465)

        u = urlopen(url.thumbnail_url)
        raw_data = u.read()
        u.close

        video_titulo = Label(add_window, text='Título: '+url.title).place(x=160, y=170)

        video_thumbnail = ImageTk.PhotoImage(data=raw_data)
        video_thumbnail_show = Label(add_window, image = video_thumbnail, width=450, height=250, bd=1,  highlightbackground="black", highlightthickness=2).place(x=160, y=200)
        video_thumbnail_show.pack()


    # botao para pesquisar a musica
    Button(add_window, command=show_video, text='Search', highlightbackground='gray15', bg='white', fg='black', relief=RAISED, overrelief=RIDGE).place(x=585, y=90)

# funcao de remover musica
def remove():
    quit_player()
    musica_delete = ''
    musica_delete = listbox.get(ACTIVE)
    os.remove(f'{musica_delete}')
    listbox.delete(0, END)
    app.after(1000, show)
    app.update()

"""

esta funcao pega a imagem do arquivo mp3 para exibila no programa, porem nao usei, optei por pular por eu usar sistema mac, ou seja, se voce
quiser usar, basta substituir music_icon pela label_imagem abaixo, ou de um rename, para qual preferir.

def Mp3_image():
    tocando = mp3_title['text']
    index = musics.index(tocando)
    audio = ID3(musics[index])

    if "APIC:" in audio:
        imagem_incorporada = audio["APIC:"].data
        imagem_tk = ImageTk.PhotoImage(Image.open(io.BytesIO(imagem_incorporada)))
        label_imagem = Label(app, image=imagem_tk)
        label_imagem.pack()

"""

# cria funcao de slide para o tempo da musica
def slide(x):
    musica = mp3_title['text']
    mixer.music.load(musica)
    mixer.music.play(start=int(slider.get()))


# funcao para reconhecer a fala
def reconhecer_fala():
    r = sr.Recognizer()

    # define o microfone como a fonte de áudio, para saber o mic desejado, abra o arq check_mic_devices.py
    # e troque o '0', pelo index do microfone escolhido
    with sr.Microphone(0) as source:  
        audio = r.listen(source, phrase_time_limit=3)
    
    print("Fale algo: ")

    # tenta reconhecer a fala usando o Google Speech Recognition
    try:
        texto_falado = r.recognize_google(audio, language='pt-BR')

        if texto_falado == "avançar música" or texto_falado == 'Próxima' or texto_falado == "próxima" or texto_falado=='avançar' or texto_falado=='Avançar':            
            next_song()
            
        elif texto_falado == "Fechar programa" or texto_falado == "fechar programa" or texto_falado == "sair":
            quit_player()

            time.sleep(1)
            engine.say("Obrigado por usar o software, volte sempre!")
            engine.runAndWait()

            app.destroy()
        
        elif texto_falado == "voltar música" or texto_falado=='Voltar' or texto_falado=='voltar' or texto_falado=='anterior' or texto_falado=='Anterior':
            back_song()

        elif texto_falado == "pausar música" or texto_falado == "Pausar música" or texto_falado == "pausar" or texto_falado == "Pausar" or texto_falado=='pause' or texto_falado=='Pause':
            pause()

        elif texto_falado == "continuar" or texto_falado == "continue" or texto_falado == "Continuar música" or texto_falado == "continuar música":
            unpause()

        elif texto_falado == "Parar música" or texto_falado == "parar música" or texto_falado == "parar" or texto_falado == "Parar":
            quit_player()

        elif texto_falado=='volume 0' or texto_falado == 'Volume 0':
            pygame.mixer.music.set_volume(0)
            volume_bar.set(0)
        
        elif texto_falado == "volume 1" or texto_falado == "Volume 1":
            pygame.mixer.music.set_volume(10)
            volume_bar.set(10)
        
        elif texto_falado == "volume 2" or texto_falado == "Volume 2":
            pygame.mixer.music.set_volume(20)
            volume_bar.set(20)

        elif texto_falado == "volume 3" or texto_falado == "Volume 3":
            pygame.mixer.music.set_volume(30)
            volume_bar.set(30)

        elif texto_falado == "volume 4" or texto_falado == "Volume 4":
            pygame.mixer.music.set_volume(40)
            volume_bar.set(40)

        elif texto_falado == "volume 5" or texto_falado == "Volume 5":
            pygame.mixer.music.set_volume(50)
            volume_bar.set(50)

        elif texto_falado == "volume 6" or texto_falado == "Volume 6":
            pygame.mixer.music.set_volume(60)
            volume_bar.set(60)

        elif texto_falado == "volume 7" or texto_falado == "Volume 7":
            pygame.mixer.music.set_volume(70)
            volume_bar.set(70)

        elif texto_falado == "volume 8" or texto_falado == "Volume 8":
            pygame.mixer.music.set_volume(80)
            volume_bar.set(10)

        elif texto_falado == "volume 9" or texto_falado == "Volume 9":
            pygame.mixer.music.set_volume(90)
            volume_bar.set(90)

        elif texto_falado == "volume 10" or texto_falado == "Volume 10":
            pygame.mixer.music.set_volume(100)
            volume_bar.set(100)

        elif texto_falado == 'play' or texto_falado == 'tocar' or texto_falado == 'iniciar' or texto_falado == 'começar' or texto_falado=='tocar playlist' or texto_falado=='start':
            play_song()
        
        else:
            engine.say("Nao entendi, fale novamente!")

        
    except sr.RequestError as e:
        print("Não foi possível conectar-se ao serviço de reconhecimento de fala; {0}".format(e))
        messagebox.showinfo('Erro!', 'Nao foi possivel conectar-se ao servico de reconhecimento de voz, verifique se voce esta conectado a internet e tente novamente.')
    except:
        print("Não entendi o que você disse")


# inicializa a janela do Tk
app = Tk()
app.title("Python Music")
app.geometry("1280x800")
app.configure(background="gray15")

# tecla pressionada 'b', e suas funcoes
def press_b(event):
    reconhecer_fala()

app.bind('<b>', press_b)

# adicionar musica
add_music_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-add-song-50.png")
add_music_icon = add_music_icon.resize((40, 40))
add_music_icon = ImageTk.PhotoImage(add_music_icon)
add_music_btn = Button(app, image=add_music_icon, command=add_music_window).place(x=13, y=28)


# remover musica
remove_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-delete-60.png")
remove_icon = remove_icon.resize((40, 40))
remove_icon = ImageTk.PhotoImage(remove_icon)
remove_music_btn = Button(app, command=remove, image=remove_icon, relief=RAISED, overrelief=RIDGE).place(x=13, y=90)


# lista de musicas
listbox = Listbox(app, selectmode=SINGLE, width=50, height=40)
listbox.place(x=110, y=25)


# frame do player :: titulo da musica
mp3_title = Label(app, text="", background="gray15", justify=LEFT, width=70)
mp3_title.place(x=600, y=380)

mp3_guide = Label(app, text="Escolha uma musica da lista", background="gray15")
mp3_guide.place(x=830, y=360)

# Icones dos botoes de manipulacao do player
play_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-play-button-circled-50-2.png")
play_icon = play_icon.resize((50, 50))
play_icon = ImageTk.PhotoImage(play_icon)
play_btn = Button(app, command=play_song, bg="black", image=play_icon, relief=RAISED, overrelief=RIDGE).place(x=740, y=500)

pause_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-pause-button-100-3.png")
pause_icon = pause_icon.resize((50, 50))
pause_icon = ImageTk.PhotoImage(pause_icon)
pause_btn = Button(app, command=pause, image=pause_icon, bg="black", relief=RAISED, overrelief=RIDGE).place(x=830, y=500)

next_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-fast-forward-round-100.png")
next_icon = next_icon.resize((50, 50))
next_icon = ImageTk.PhotoImage(next_icon)
next_btn = Button(app, command=next_song, image=next_icon, relief=RAISED, overrelief=RIDGE, bg="black").place(x=1010, y=500)

back_btn = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-fast-forward-round-100-2.png")
back_btn = back_btn.resize((50, 50))
back_btn = ImageTk.PhotoImage(back_btn)
back_btn = Button(app, command=back_song, image=back_btn, relief=RAISED, bg="black", overrelief=RIDGE).place(x=650, y=500)

quit_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-stop-circled-100.png")
quit_icon = quit_icon.resize((50, 50))
quit_icon = ImageTk.PhotoImage(quit_icon)
quit_btn = Button(app, bg="black", command=quit_player, image=quit_icon).place(x=1100, y=500)

unpause_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-memories-100.png")
unpause_icon = unpause_icon.resize((50, 50))
unpause_icon = ImageTk.PhotoImage(unpause_icon)
unpause_btn = Button(app, command=unpause, bg="black", image=unpause_icon).place(x=920, y=500)

# imagem do player
img_icon = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-music-library-100.png")
img_icon = img_icon.resize((250,200))
img_icon = ImageTk.PhotoImage(img_icon)


music_background_img = Label(app, width=30, height=15, bg="gray35").place(x=780, y=100)
music_icon = Label(app, image=img_icon).place(x=790, y=120)

# barra de volume
def change_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

volume_bar = ttk.Scale(app, from_=0, to=100, orient="horizontal", command=change_volume)
volume_bar.set(50)
volume_bar.configure(length=400)
volume_bar.place(x=720, y=600)
Label(app, text='Volume', bg="gray15").place(x=897, y=574)

# pasta com as musicas
os.chdir(r"/Users/gabrielhernandes/Documents/MP3 Player/Musics")
musics = os.listdir()

# exibir musicas na listbox
def show():
    global musics
    os.chdir(r"/Users/gabrielhernandes/Documents/MP3 Player/Musics")
    musics = os.listdir()
    for music in musics:
        if music.endswith('.mp3'):
            listbox.insert(END, music)
show()

# se a lista houver mais de 80 musicas, ira inserir um scroll na listbox
if len(musics)>80:
    scroll = Scrollbar(app)
    scroll.place(x=528, y=26)

    listbox.config(yscrollcommand=scroll.set)
    scroll.config(command=listbox.yview)

# barra de progresso da musica
barra = Label(app, text='', bg="gray15", width=50)
barra.place(x=690, y=430)

# botoes de info e fala
info_falar = Image.open("/Users/gabrielhernandes/Documents/MP3 Player/icons8-informações-48.png")
info_falar = info_falar.resize((40, 40))
info_falar = ImageTk.PhotoImage(info_falar)
info_falar = Button(app, image=info_falar, command=info_falar_box).place(x=13, y=240)
chamar_fala = Button(app, text="Falar", command=reconhecer_fala).place(x=8, y=200)


#criar slider para tempo da musica
slider = ttk.Scale(app, from_=0, to=100, orient=HORIZONTAL, length=400, value=0, command=slide)
slider.place(x=720, y=450)

# iniciar mixer
mixer.init()

# encerrar tk
app.mainloop()