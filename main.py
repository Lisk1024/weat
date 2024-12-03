from PyQt5 import QtCore
from transformers import BertTokenizer, GPT2LMHeadModel, TextGenerationPipeline
import hashlib
from loginui import *
from interfaceui import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from scrapy import xcfsearch, scrapyxcf
user_db={}
saved_recipe = ''
recipe = ""
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.register)
        self.ui.pushButton_2.clicked.connect(self.go_inter)
        self.show()

    def go_inter(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()

        if username not in user_db:
            self.ui.label_res.setText("User not registered")
        else:
            encrypted_password = encrypt_password(password)
            if user_db[username] == encrypted_password:
                self.ui.label_res.setText(f"hello,user{username}login successfully")
                InterfaceWindow()
                self.close()


            else:
                self.ui.label_res.setText("wrong username or password")

        # 注册函数
    def register(self):
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        if username in user_db:
            self.ui.label_res.setText("user existed")
        else:
            encrypted_password = encrypt_password(password)
            user_db[username] = encrypted_password
            self.ui.label_res.setText(f"hello,user{username} register successfully")


class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_inter()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_scrapy.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_ai.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_contact.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_user.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.Go.clicked.connect(self.scrapy)
        self.ui.Go_2.clicked.connect(self.ai)
        self.ui.saveButton_Scrapy.clicked.connect(self.save)
        self.ui.saveButton_Ai.clicked.connect(self.save)
        self.ui.F5.clicked.connect(self.F5)
        self.show()

    def scrapy(self):
        global recipe
        name = self.ui.input_scrapy.text()
        print(name)
        if not name:
            return None
        web = xcfsearch(name)
        recipe = name+"\n"+scrapyxcf(web)
        self.ui.output_scrapy.setText(scrapyxcf(web))

    def ai(self):
        global recipe
        str_ = self.ui.input_ai.text()
        if not str_:
            return None
        model = GPT2LMHeadModel.from_pretrained(r".\gpt2-chinese-cluecorpussmall")
        tokenizer = BertTokenizer.from_pretrained("uer/gpt2-distil-chinese-cluecorpussmall")
        text_generator = TextGenerationPipeline(model, tokenizer)
        output = text_generator(str_ + "做法 用 料 ：", truncation=True, max_length=100, do_sample=True)
        output = str(output)
        output = output[20:-2]
        recipe = str_+"\n"+output
        self.ui.output_ai.setText(output)

    def save(self):
        global recipe
        global saved_recipe
        saved_recipe = saved_recipe+"\n"+recipe

    def F5(self):
        global saved_recipe
        self.ui.textBrowser.setText(saved_recipe)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())