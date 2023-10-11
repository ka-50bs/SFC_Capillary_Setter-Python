import numpy as np
import cv2

import random

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import TheilSenRegressor
from sklearn.linear_model import RANSACRegressor

class CapCam(object):
    def __init__(self):
        
        self.img = None
        self.frame = None
        self.cap_edges = [0, 0]
        self.cap_angle = 0
        self.cap_center = 0
        self.beam_center = 0
        self.beam_angle = 0
        self.center = []

        self.up = []
        self.down = []
        self.m2p = 0
        self.p2m = 0
        self.regr = RANSACRegressor(random_state=0, stop_probability=0.90)
        #self.regr = LinearRegression()
        self.d_pos = []
        self.d_ang = []
        self.up_edge = []
        self.down_edge = []
        self.cap = None

    def init_cam(self, id_cam, exp):
        '''
        Метод инициализации объекта захвата в виде камеры
        :param id_cam: Параметр, ID камеры захвата
        :param exp: Параметр, уровень экспозиции для камеры
        '''
        if self.cap != None:
            self.cap.release()
        cap = cv2.VideoCapture(id_cam, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_EXPOSURE, exp)
        self.cap = cap
        return self
    
    def down_scale(self, img, factor = 6, channel ='r'):
        '''
        Метод обработки кадра для обработки. Производит выделение определенного канала изображения и децимацию разрешения 
        :param img: Масиив, Кадр для обработки
        :param factor: Параметр, уровень дечимации разрешения
        :param channel: Параметр, выбор канала изображения 
        :return: Возвращает обработанное изображение 
        '''
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if channel == 'r':
            img = img[::factor, ::factor, 0]
        elif channel == 'g':
            img = img[::factor, ::factor, 1]
        elif channel == 'b':
            img = img[::factor, ::factor, 2]
        elif channel == 'gray':
           img = cv2.cvtColor(img[::factor, ::factor,:], cv2.COLOR_RGB2GRAY)
        elif channel == 'native':
           img = img[::factor, ::factor,:]
        return img

    def init_video(self, name):
        '''
        Метод инициализации объекта захвата в виде видеофайла
        :param name: Параметр, полный путь до загружаемого видео
        '''
        self.cap = cv2.VideoCapture(name)
        return self

    def get_frame(self):
        '''
        Метод получения изображения (фрейма) из обьекта захвата (камера, видео и т.д.)
        '''
        ret, frame = self.cap.read()
        if (ret):
            self.frame = frame
        return self

    def get_img(self, fname):
        '''
        Метод получения изображения (фрейма) из файла изображения
        :param fname: Параметр, полный путь до загружаемого изображения
        '''
        self.frame = cv2.imread(fname)
        return self
    
    def max_conv(self, img, win = [1, 20]):
        '''
        Метод обработки кадра для обработки. Производит оконное преобразование, выделяющее в окне максимум 
        :param img: Масиив, кадр для обработки
        :param win: Список, размер окна для преобразования 
        :return: Возвращает обработанное изображение 
        '''
        _img = np.copy(img)
        img_size = np.shape(_img)
        for i in range(win[0], img_size[0] - win[0]):
            for j in range(win[1], img_size[1] - win[1]):
                _img[i,j] = np.max(img[i-win[0]:i+win[0]+1,j-win[1]:j+win[1]+1])
        return _img

    def edge_detect(self, img, win = 20, treshlod = 1.6, inverse = False):
        '''
        Метод нахождения параметров границ капилляра (вернхей и нижней).
        :param img: Масиив, кадр для обработки
        :param win: Список, размер окна для преобразования 
        :return: Возвращает обработанное изображение 
        '''
        img_size = np.shape(img)
        
        x = np.array(range(img_size[1]))
        x = np.reshape(x, (-1,1))

        up_edge = np.zeros(img_size[1])
        down_edge = np.zeros(img_size[1])
        
        if inverse == False:
            for i in range(img_size[1]):
                treshold_up = treshlod * np.std(img[:win,i]) + np.mean(img[:win,i])
                treshold_down = treshlod * np.std(img[:win,i]) + np.mean(img[-win:,i])

                up = 0
                down = 0

                for j in range(img_size[0]):
                    if img[j,i] > treshold_up:
                        up = j
                        break
                up_edge[i] = up

                for j in range(img_size[0]):
                    if img[img_size[0]-j-1,i] > treshold_down:
                        down = img_size[0]-j-1
                        break
                down_edge[i] = down
        else:
            for i in range(img_size[1]):
                treshold_up = treshlod * np.std(img[:win,i]) - np.mean(img[:win,i])
                treshold_down = treshlod * np.std(img[:win,i]) - np.mean(img[-win:,i])

                up = 0
                down = 0

                for j in range(img_size[0]):
                    if img[j,i] < treshold_up:
                        up = j
                        break
                up_edge[i] = up

                for j in range(img_size[0]):
                    if img[img_size[0]-j-1,i] < treshold_down:
                        down = img_size[0]-j-1
                        break
                down_edge[i] = down

        self.up = up_edge
        self.down = down_edge

        self.regr.fit(x, up_edge)
        # k_up = self.regr.coef_[0]
        # b_up = self.regr.intercept_
        k_up = self.regr.estimator_.coef_[0]
        b_up = self.regr.estimator_.intercept_

        self.regr.fit(x, down_edge)
        #k_down = self.regr.coef_[0]
        #b_down = self.regr.intercept_
        k_down = self.regr.estimator_.coef_[0]
        b_down = self.regr.estimator_.intercept_

        # self.cap_edges = np.array([b_down, b_up])
        # self.cap_center = (b_down + b_up) / 2
        # self.cap_angle = np.arctan((k_down + k_up) / 2)

        # self.m2p = (b_down - b_up) / 254
        # self.p2m = 1 / self.m2p
        return np.arctan((k_down + k_up) / 2), [b_down, b_up] 

    def beam_detect(self, img):
        img = cv2.blur(img, [9,9])
        img_size = np.shape(img)
        max_array = np.zeros(img_size[1])

        for i in range(img_size[1]):

            max_array[i] = np.argmax(img[:,i])

        y = max_array
        x = np.array(range(img_size[1]))
        x = np.reshape(x, (-1,1))

        self.regr.fit(x, y)

        # self.beam_angle = self.regr.coef_[0]
        # self.beam_center = self.regr.intercept_
        self.beam_angle = self.regr.estimator_.coef_[0]
        self.beam_center = self.regr.estimator_.intercept_
        x = np.array(range(img_size[1]))
        self.beam = self.beam_center + self.beam_angle * x
        self.beam_angle = np.arctan(self.beam_angle)
        self.beam_part = y


    def cap_init(self, N = 10, factor = 1, channel='gray', inverse = False, treshold = 3):
        edges_list = []
        angles_list = []
        
        for i in range(N):
            self.get_frame()
            img = self.frame
            cap_img = self.down_scale(img=img, factor=factor, channel=channel)
            res = self.edge_detect(img=cap_img, win=40, treshlod=treshold, inverse=inverse)
            edges_list.append(res[1])
            angles_list.append(res[0])
        
        edges_list = np.array(edges_list)
        angles_list = np.array(angles_list)

        self.cap_edges = np.mean(edges_list, axis=0)
        self.cap_angle = np.mean(angles_list, axis=0)
        self.cap_center = (self.cap_edges[0]  + self.cap_edges[1]) / 2

        self.m2p = (self.cap_edges[1] - self.cap_edges[0]) / 254
        self.p2m = 1 / self.m2p

        img_size = np.shape(cap_img)
        x = np.array(range(img_size[1]))

        self.up_edge = self.cap_edges[1] + np.tan(self.cap_angle) * x
        self.down_edge = self.cap_edges[0] + np.tan(self.cap_angle) * x
        self.center = self.cap_center + np.tan(self.cap_angle) * x
        

    def beam_init(self,  img, factor = 1, channel='r'):
        img = cv2.blur(img, [21,21])
        beam_img = self.down_scale(img=img, factor=factor, channel=channel)
        self.beam_detect(img=beam_img)
        self.d_ang.append(np.rad2deg(self.cap_angle - self.beam_angle))
        self.d_pos.append((self.cap_center - self.beam_center) * self.p2m) 

    

