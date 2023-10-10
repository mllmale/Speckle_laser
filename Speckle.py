from tkinter import *
import cv2
from PIL import Image, ImageTk
from moviepy.editor import *


class Camera:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frame_tela()
        self.conf_camera()
        self.botao_gravacao()
        self.label_degree()
        self.qtdf = 1
        self.qtdv = 1
        self.gravando = False
        self.imagens = []
        self.atualiza_camera()
        root.mainloop()

    def tela(self):
        self.root.title("Camera")
        self.root.resizable(True, True)
        self.root.minsize(width=1280, height=720)
        self.root.geometry("1280x720")

    def frame_tela(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.65, rely=0.05, relwidth=0.3, relheight=0.675)
        self.root.configure(background='#1e3743')

        self.frame2 = Frame(self.root)
        self.frame2.place(relx=0.05, rely=0.78, relwidth=0.505, relheight=0.15)
        self.root.configure(background='#1e3743')

    def conf_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.camera_canvas = Canvas(root, width=640, height=480)
        self.camera_canvas.pack()
        self.camera_canvas.place(relx=0.05, rely=0.05)

    def botao_gravacao(self):
        self.btn_capture = Button(root, text="Capturar Foto", command=self.tira_foto)
        self.btn_filma = Button(root, text="Filmar", command=self.iniciar_gravacao)
        self.btn_para = Button(root, text="Parar gravação", command=self.parar_gravacao)
        self.btn_sobrepor = Button(root, text="Sobrepor", command=self.sobrepor)
        self.btn_timelapse = Button(root, text="gif", command=self.criar_timelapse)
        self.btn_capture.place(relx=0.1, rely=0.83)
        self.btn_sobrepor.place(relx=0.38, rely=0.83)
        self.btn_filma.place(relx=0.2, rely=0.83)
        self.btn_para.place(relx=0.28, rely=0.83)
        self.btn_timelapse.place(relx=0.48, rely=0.83)

    def label_degree(self):
        self.lb_laser = Label(text="Angulação do laser")
        self.lb_laser.place(relx=0.68, rely=0.1)
        self.lb_laser_entry = Entry(self.frame1)
        self.lb_laser_entry.place(relx=0.105, rely=0.12, relheight=0.05)
        self.btn_laser = Button(self.frame1, text="Mandar")  # Depois será adicionado o command
        self.btn_laser.place(relx=0.48, rely=0.12)
        self.lb_camera = Label(text="Angulação do camera")
        self.lb_camera.place(relx=0.68, rely=0.18)
        self.lb_camera_entry = Entry(self.frame1)
        self.lb_camera_entry.place(relx=0.105, rely=0.24, relheight=0.05)
        self.btn_camera = Button(self.frame1, text="Mandar")  # Depois será adicionado o command
        self.btn_camera.place(relx=0.48, rely=0.24)
        self.lb_table = Label(text="Posição da mesa")
        self.lb_table.place(relx=0.68, rely=0.26)
        self.lb_table_entry = Entry(self.frame1)
        self.lb_table_entry.place(relx=0.105, rely=0.355, relheight=0.05)
        self.lb_table = Button(self.frame1, text="Mandar")  # Depois será adicionado o command
        self.lb_table.place(relx=0.48, rely=0.355)

    def atualiza_camera(self):
        ret, frame = self.camera.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)

        self.camera_canvas.create_image(0, 0, anchor=NW, image=photo)
        self.camera_canvas.photo = photo

        self.root.after(1, self.atualiza_camera)

    def tira_foto(self):
        ret, frame = self.camera.read()

        if ret:
            file_name = f"captured_photo_{self.qtdf}.jpg"
            cv2.imwrite(file_name, frame)
            print(f"Foto capturada: {file_name}")
            self.qtdf += 1

    def iniciar_gravacao(self):
        if not self.gravando:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            file_name = f"recording{self.qtdv}.mp4"
            self.writer = cv2.VideoWriter(file_name, fourcc, 30.0, (640, 480))
            self.qtdv += 1
            self.gravando = True
            self.write_frame()

    def write_frame(self):
        ret, frame = self.camera.read()
        if ret:
            self.writer.write(frame)
            self.root.after(33, self.write_frame)
        else:
            self.parar_gravacao()

    def parar_gravacao(self):
        if self.gravando:
            self.writer.release()
            self.desacelerar()
            self.gravando = False

    def desacelerar(self):
        file_name = f"recording{self.qtdv - 1}.mp4"
        clip = VideoFileClip(file_name)
        final = clip.fx(vfx.speedx, 0.5)
        final.write_videofile(f"recording{self.qtdv - 1}_slow.mp4", codec='libx264', audio_codec='aac')
        os.remove(file_name)

    def sobrepor(self):
        imagem_sobreposta = cv2.imread('1.bmp')

        for x in range(2, 130):
            imagem_atual = cv2.imread(f'{x}.bmp')
            imagem_sobreposta = cv2.addWeighted(imagem_sobreposta, 0.7, imagem_atual, 0.3, 0)

            cv2.imwrite('imagem_sobreposta.bmp', imagem_sobreposta)

    def criar_timelapse(self):
        num_imagens = 129
        duracao_imagem = 100
        lista_imagens = []

        for x in range(1, num_imagens + 1):
            imagem = Image.open(f'{x}.bmp')
            lista_imagens.append(imagem)

        nome_gif = 'timelapse.gif'
        lista_imagens[0].save(nome_gif, save_all=True, append_images=lista_imagens[1:], loop=1, duration=duracao_imagem)


root = Tk()
app = Camera(root)
