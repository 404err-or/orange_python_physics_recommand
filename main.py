from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import pytesseract
from orangecontrib.text.vectorization.sbert import SBERT
from orangecontrib.text import Corpus
from Orange.util import dummy_callback
import pickle, cv2, os, random

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = pickle.load(open('model.pkcls', 'rb'))
sbert = SBERT()
corpus = Corpus.from_file("test.csv")

status_code = 0 # program status
'''
0 => no state
1 => Camera running
2 => Camera saving and OCR
3 => reading and OCR of file image
4 => Entering text
5 => Fixing image OCR
6 => predicting model
7 => Recommend problem
'''

predict_code = {
    '1.0': '1-1 part',
    '2.0': '1-2 part',
    '3.0': '1-3 part',
    '4.0': '2-1 part',
    '5.0': '2-2 part',
    '6.0': '3-1 part',
    '7.0': '3-2 part'
}


path = 'img_data/'
dir_list = os.listdir(path)

recommand_data = {i: os.listdir(path+i) for i in dir_list}

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def predict(text):
    # The test.csv file must contain at least 3 to be able to predict.
     # => sbert encoding by putting 3 in advance and adding them to the list.
    data = sbert(texts=corpus.documents + [text], callback=dummy_callback)
    return model(data[-1]) + 1

class App():
    def __init__(self):
        self.root = Tk()
        self.root.title('물리 문제 추천')
        self.root.geometry('400x500+100+100')
        self.root.resizable(False, False)
        self.explain_text = '''설명서'''
        explain_label = Label(self.root, text=self.explain_text, width=100, height=50, bitmap='info', relief='solid', compound='top')
        explain_label.pack()
        self.camera_button_text = '카메라 켜기'
        self.camera_status_button = Button(self.root, width=20, text=self.camera_button_text, overrelief='solid', command=self.camera_button_def)
        self.camera_status_button.pack()
        self.image_button = Button(self.root, width=20, text='이미지 업로드', overrelief='solid', command=self.image_button_def)
        self.image_button.pack()
        self.self_button = Button(self.root, width=20, text='문제 텍스트 직접 입력', overrelief='solid', command=self.self_button_def)
        self.self_button.pack()
        self.root.mainloop()

    def camera_button_def(self):
        global status_code
        print('camera_button_def', status_code)
        if status_code == 1: # 카메라 OFF 이벤트
            status_code = 0
            self.camera_status_button['text'] = '카메라 켜기'
        elif status_code == 0: # 카메라 ON 이벤트
            status_code = 1
            self.camera_status_button['text'] = '카메라 끄기'
            self.camera_root_def()
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def image_button_def(self):
        global status_code
        print('image_button_def',status_code)
        if status_code == 0:
            status_code = 3
            f_types = [('Image Files', '*.jpg, *.png')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            if filename == '':
                status_code = 0
                messagebox.showerror(title='error', message='파일을 선택하지 않았습니다. 처음으로 돌아갑니다.')
            else:
                text = pytesseract.image_to_string(Image.open(filename), lang="kor+eng")
                status_code = 5
                print(text)
                self.edit_text(text)
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def self_button_def(self):
        global status_code
        print('self_button_def', status_code)
        if status_code == 0:
            status_code = 4
            self.edit_text()
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def camera_root_def(self):
        global status_code
        print('camera_root_def', status_code)
        if status_code == 1:
            self.camera_root = Toplevel(self.root)
            self.camera_root.title('문제 찍기')
            self.camera_root.grid()
            self.camera_label = Label(self.camera_root, text='인식하고자 하는 문제를 찍어주세요', relief='solid', compound='top')
            self.camera_label.grid()
            self.image = Label(self.camera_root)
            self.image.grid()
            self.camera_status_button = Button(self.camera_root, text='사진찍기', overrelief='solid', command=self.save)
            self.camera_status_button.grid()

            self.camera_root.protocol("WM_DELETE_WINDOW", lambda: self.on_exit(self.camera_root))
            
            self.video_stream()
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def video_stream(self):
        global status_code
        if status_code == 0:
            self.camera_root.destroy()
            self.camera_root.update()
            self.camera_status_button['text'] = '카메라 켜기'
        elif status_code == 1:
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image.imgtk = imgtk
            self.image.configure(image=imgtk)
            self.image.after(1, self.video_stream)
        elif status_code == 2:
            _, frame = cap.read()
            cv2.imwrite("filename.jpg", frame)
            text = pytesseract.image_to_string(Image.open("filename.jpg"), lang="kor+eng")
            print(text)
            self.camera_root.destroy()
            self.camera_root.update()
            self.camera_status_button['text'] = '카메라 켜기'
            status_code = 5
            self.edit_text(text)
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def save(self):
        global status_code
        print('save', status_code)
        status_code = 2

    def edit_text(self, text: str = None):
        global status_code
        print('edit_text', status_code)
        if status_code == 5 or status_code == 4:
            self.text_root = Toplevel(self.root)
            self.text_root.title('텍스트 수정')
            self.text_root.grid()
            self.input_text = Text(self.text_root, width=70)
            if status_code == 5:
                if text is None or text.strip() == '':
                    messagebox.showerror(title='error', message='텍스트를 인식하지 못했습니다.\n처음으로 돌아갑니다.')
                    status_code = 0
                    self.text_root.destroy()
                    self.text_root.update()
                    return ''
                self.input_text.insert(END, text.strip().replace('\n', ' '))
                self.camera_label = Label(self.text_root, text='이미지 인식 중 오류가 있을 수 있습니다.\n정확도를 높이기 위해 이상한 문장 등을 수정해주세요.\n또한, 문제만 남기고 나머지(보기, 선다형, 문제 번호 등)는 지워주세요. 감사합니다.', relief='solid', compound='top')
                self.text_button = Button(self.text_root, text='수정 완료', overrelief='solid', command=self.predict_gui)
            else:
                self.camera_label = Label(self.text_root, text='문제의 텍스트를 입력해주세요.', relief='solid', compound='top')
                self.text_button = Button(self.text_root, text='입력 완료', overrelief='solid', command=self.predict_gui)
            self.camera_label.grid()
            self.input_text.grid()
            self.text_button.grid()
            self.input_text.focus()
            self.text_root.protocol("WM_DELETE_WINDOW", lambda: self.on_exit(self.text_root))
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def predict_gui(self):
        global status_code
        print('predict_gui', status_code)
        if status_code == 5 or status_code == 4:
            status_code = 6
            text = self.input_text.get("1.0",END)
            self.text_root.destroy()
            self.text_root.update()
            result = predict(text)
            print(predict_code[str(result)])
            messagebox.showinfo(title='Predict Success', message=predict_code[str(result)])
            status_code = 7
            self.recommand(str(result))
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def recommand(self, value: str):
        global status_code
        print('recommand', status_code)
        if status_code == 7:
            self.recommand_list = []
            self.recommand_label_list = []
            random_value = random.sample(recommand_data[value], 5)
            for i in random_value:
                print(f'{path}{value}/{i}')
                self.recommand_list.append(Toplevel(self.root))
                self.recommand_list[-1].title(f'{predict_code[value]} - {i}')
                self.recommand_list[-1].grid()
                self.recommand_label_list.append(Label(self.recommand_list[-1]))
                image = ImageTk.PhotoImage(Image.open(f'{path}{value}/{i}'))
                self.recommand_label_list[-1].imgtk = image
                self.recommand_label_list[-1].configure(image=image)
                self.recommand_label_list[-1].grid()                
            status_code = 0
        else:
            messagebox.showwarning(title='Warning', message='다른 작업을 마치고 시도해주세요')

    def on_exit(self, root_content):
        global status_code
        print('on_exit', status_code)
        root_content.destroy()
        root_content.update()
        status_code = 0

cv2.destroyAllWindows()

app = App()



