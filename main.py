from tkinter import *
import pygame
import os

class MusicPlayer:
    def __init__(self,root):
        self.current_track = ""  # текущий трек
        self.STATUS = 0  # 0 - ОСТАНОВКА; 1 - ПАУЗА; 2 - ПРОИГРЫВАНИЕ
        self.root = root
        self.root.title("Музыкальный плеер")  # заголовок окна
        self.root.geometry("1000x200")  # размеры окон
        pygame.init()  # инициализация pygame
        pygame.mixer.init()  # инициализация миксера
        self.track = StringVar()  # объявление переменной с треком
        self.status = StringVar()  # объявление переменной со статусом

        # Создание рамки для трека и статуса
        self.trackframe = LabelFrame(self.root,text="Трек",font=("times new roman",15,"bold"),bg="Navyblue",fg="white",bd=5,relief=GROOVE)
        self.trackframe.place(x=0,y=0,width=600,height=100)
        # Подставляем название трека
        songtrack = Label(self.trackframe,textvariable=self.track,width=20,font=("times new roman",24,"bold"),bg="White",fg="Black").grid(row=0,column=0,padx=10,pady=5)
        # Подставляем статус, но сперва фон такой же, чтобы не видно было
        self.trackstatus = Label(self.trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="Navyblue",fg="gold").grid(row=0,column=1,padx=10,pady=5)

        # Создание рамки с кнопками
        buttonframe = LabelFrame(self.root,text="Панель управления",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        buttonframe.place(x=0,y=100,width=600,height=100)
        playbtn = Button(buttonframe,text="▶",command=self.playsong,width=8,height=1,font=("times new roman",22,"bold"),fg="navyblue",bg="DarkSeaGreen1").grid(row=0,column=0,padx=8,pady=5)
        playbtn = Button(buttonframe,text="⏸️",command=self.pausesong,width=8,height=1,font=("times new roman",22,"bold"),fg="navyblue",bg="honeydew").grid(row=0,column=1,padx=8,pady=5)
        playbtn = Button(buttonframe,text="⏹️",command=self.stopsong,width=8,height=1,font=("times new roman",22,"bold"),fg="navyblue",bg="pink").grid(row=0,column=3,padx=8,pady=5)

        # Создание рамки с плейлистом
        songsframe = LabelFrame(self.root,text="Плейлист",font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        songsframe.place(x=600,y=0,width=400,height=200)
        # Создание скролбара
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        # Подставление списка треков
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="seashell2", selectforeground="navyblue" ,selectmode=SINGLE,font=("times new roman",12,"bold"),bg="silver",fg="dodgerBlue3",bd=5,relief=GROOVE)
        # Подставляем скролбар
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # ПАПКА С ТРЕКАМИ!
        os.chdir("music")
        # Фиксируем все песни
        songtracks = os.listdir()
        # Подставляем треки в плейлист
        for track in songtracks:
            self.playlist.insert(END,track)

    
    def playsong(self):
        # tесли треки отличаются или статус 0 или 1
        # p.s. то есть: если мы не пытаемся запустить тот же самый трек или же в случае stop/pause
        if self.current_track != self.playlist.get(ACTIVE) or self.STATUS in (0, 1):
            self.current_track = self.playlist.get(ACTIVE)  # сохраняем текущую песню  (формат: "Ауф.mp3")
            self.track.set(self.current_track)  # # Отображение название выбранной песни
            # Отображение статуса
            self.status.set("ИГРАЕТ")
            self.trackstatus = Label(self.trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="DarkSeaGreen1",fg="grey20").grid(row=0,column=1,padx=10,pady=5)

            if self.STATUS == 1:  # если пауза, то unpause
                self.STATUS = 2  # статус проигрывания
                pygame.mixer.music.unpause()

            else:  # если остановлено, то запуск песни
                # p.s. почему else? еще может быть ситуация когда ты слушая один трек хочешь запустить другой, то есть статус 2
                self.STATUS = 2  # статус проигрывания
                # Загрузить выбранную музыку
                pygame.mixer.music.load(self.playlist.get(ACTIVE))
                # Запутить выбранную музыку
                pygame.mixer.music.play()



    def stopsong(self):
        # Отображение статуса
        self.status.set("СТОП")
        self.trackstatus = Label(self.trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="pink",fg="grey20").grid(row=0,column=1,padx=10,pady=5)

        self.STATUS = 0  # статус остановки
        pygame.mixer.music.stop()  # остановка песни

    
    def pausesong(self):
        if self.STATUS == 2:  # можно запаузить только если проигрывается
            # p.s. чтобы не было бага, когда ты запаузил остановленный трек
            # Отрисовка статуса
            self.status.set("ПАУЗА")
            self.trackstatus = Label(self.trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="honeydew",fg="grey20").grid(row=0,column=1,padx=10,pady=5)

            self.STATUS = 1  # статус паузы
            pygame.mixer.music.pause()  # паузим трек
        

root = Tk()
MusicPlayer(root)
root.mainloop()

