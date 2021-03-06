from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import pafy
import os
from os import path
from PyQt5.uic import loadUiType
import urllib.request
import humanize

ui,_=loadUiType('main.ui')
class MainApp(QMainWindow,ui):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()
    
    
    def InitUI(self):       #Conatin All UI Changes in Loading
        self.tabWidget.tabBar().setVisible(False)
        self.Apply_DarkGray_Style()
    def Handle_Buttons(self): #Handle all buttons in app
        self.pushButton_2.clicked.connect(self.Download)
        self.pushButton.clicked.connect(self.Handle_Browse)
        self.pushButton_3.clicked.connect(self.Get_video_data)
        self.pushButton_5.clicked.connect(self.Download_Video)
        self.pushButton_4.clicked.connect(self.Save_Browse)
        self.pushButton_13.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)
        self.pushButton_14.clicked.connect(self.Open_Home)
        self.pushButton_18.clicked.connect(self.Open_Download)
        self.pushButton_17.clicked.connect(self.Open_Youtube)
        self.pushButton_16.clicked.connect(self.Open_Settings)
        self.pushButton_8.clicked.connect(self.Apply_DarkGray_Style)
        self.pushButton_9.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_10.clicked.connect(self.Apply_QDarkBlue_Style)

    
    def Handle_Progress(self,blocknum,blocksize,totalsize): #Calculate Progress
        readed_data=blocknum*blocksize
        print(readed_data)

        if totalsize>0:
            download_percentage=(readed_data*100)/totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
    def Handle_Browse(self):
        save_location=QFileDialog.getSaveFileName(self, caption='Save as',directory='.',filter='All Files(*.*)')
        print(save_location)
        self.lineEdit_2.setText(str(save_location[0]))
    def Download(self):
        download_url=self.lineEdit.text()
        save_location=self.lineEdit_2.text()

        if download_url=="" or save_location=="":
            QMessageBox.warning(self,'Data Error','Provide valid Data')
        else:
            try:
                urllib.request.urlretrieve(download_url,save_location,self.Handle_Progress)
            except Exception:
                QMessageBox.warning(self,'Download Error','URL Not Valid')
                return
        QMessageBox.information(self,'Download Completed','Download Completed')
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def Save_Browse(self):
        save_location = QFileDialog.getSaveFileName(self , caption="Save as" , directory="." , filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))

    def Get_video_data(self):
        video_url=self.lineEdit_3.text()

        if video_url=='':
            QMessageBox.warning(self,'Download Error','URL Not Valid')
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams :
                print(stream.get_filesize())
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype , stream.extension , stream.quality , size)
                self.comboBox.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location , callback=self.Video_Progress)
            QMessageBox.information(self,'Download Completed','Download Completed')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.progressBar_2.setValue(0)

    def Video_Progress(self, total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60 , 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    ################################################
    ######### Youtube Playlist Download

    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()
        if playlist_url == '' or save_location == '' :
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))
        
        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_3.currentIndex()


        QApplication.processEvents()

        for video in playlist_videos :
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()

            current_video_in_download +=1

    def Playlist_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_4.setValue(download_percentage)
            remaining_time = round(time/60 , 2)

            self.label_7.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
        if received==total:
            QMessageBox.information(self,'Download Completed','Download Completed')

    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)

    # UI OPTIONS
    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)

    # THEMES
    def Apply_QDark_Style(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)


    def Apply_DarkGray_Style(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDarkBlue_Style(self):
        style = open('themes/darkblu.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()

