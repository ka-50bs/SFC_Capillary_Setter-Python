import numpy as np
import cv2

class CapCam(object):
    def __init__(self):
        self.cap = None
        self.shif_arr = []
        self.frame = None
        self.edges = None
        self.center = 0
        self.beam = 0
        self.k = 0.1
        self.qtile = 0.5
        self.cap_mask = None
        self.beam_mask = None

        self.edge_up = []
        self.edge_down = []

    def init_cam(self, id_cam, exp):
        '''
        Метод инициализации объекта захвата в виде камеры
        :param id_cam: Параметр, ID камеры захвата
        :param exp: Параметр, уровень экспозиции для камеры
        '''
        cap = cv2.VideoCapture(id_cam, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_EXPOSURE, exp)
        self.cap = cap
        return self

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

        self.frame = self.frame[::3,::3,:]
        return self

    def get_img(self, fname):
        '''
        Метод получения изображения (фрейма) из файла изображения
        :param fname: Параметр, полный путь до загружаемого изображения
        '''
        self.frame = cv2.imread(fname)
        self.frame = self.frame[::3,::3,:]
        return self

    def capillar_finder(self, inverse=False):
        '''
        Препроцессинг изображения связанный с нахождением границ капилляра на фотографии снятой на вебкамере.
        Препроцессинг состоит из следующих этапов:
            - Выбор G-канала из изображения в системе BGR
            - Применение гамма коррекции изображения
            - Применение фильтра Blur с большим окном интегрирования [6000, 1]
            - Перевод изображения в GrayScale для удобства работы с методами нахождения контура
            - Применение пороговой бинаризации изображения, порог задается аргументом treshold
            - При необходимости используется инвертирование бинаризованного изображения
            - В бинаризованном изображении находится маска контуров посредством алгоритма Canny
            - Для маски контуров находится сам список контуров
            - Для каждого контура находится среднее значение по координате y, появляется список координат каждой границы
            - Каждая граница отрисовывается во кадре
            - Массив кооординат границ сортируется по возрастанию.
            - Если существует массив границ больше 2 элементов, в этом массиве выбираются первый и последний элемент.
              Это и есть границы капилляра.
            - Координата центра капилляра вычисляется путем нахождения среднего между границами капилляра при соблюдении
              условий предыдущего пунктаю. В противном случае, значение координаты центра не меняется
            - Всё
        :param inverse: Булевый параметр, управляет инверсией изображения после бинаризации
        :return: исходное изображение с камеры с дополнительной разметкой контуров красным цветом
        '''
        def gamma(im, val):
            return np.array((im ** val) * 255 / np.amax(im ** val), dtype=np.uint8)

        img = np.copy(self.frame)
        img_size = np.shape(img)

        img[:, :, [0, 2]] = img[:, :, [0, 2]] * 0
        img = gamma(img, 0.6)


        img = cv2.blur(img, (6000, 1))
        self.green = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        treshold = np.quantile(np.mean(img, axis=1), self.qtile)
        ret, img = cv2.threshold(img, treshold, 255, 0)
        self.cap_mask = img

        if inverse == True:
            img = cv2.bitwise_not(img)

        img1 = np.copy(self.frame)
        edges = cv2.Canny(img, 100, 200)

        cont, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        edges = []

        for i in range(len(cont)):
            point = np.mean(cont[i], axis=0, dtype=np.int32)[0][1]
            edges.append(point)
            #img1 = cv2.line(img1, (0, point), (img_size[1], point), (0, 255, 255), 1)

        if len(edges) >= 2:
            edges.sort()
            self.edges = edges
            self.edge_up.append(edges[0])
            self.edge_down.append(edges[-1])

            self.up = int(np.mean(self.edge_up))
            self.down = int(np.mean(self.edge_down))

            self.k = 254 / (self.up - self.down)
            self.center = int((self.up + self.down) / 2)

        else:
            self.up = int(0)
            self.down = int(img_size[0])

        img1 = cv2.line(img1, (0, self.up), (img_size[1], self.up), (0, 255, 255), 1)
        img1 = cv2.line(img1, (0, self.down), (img_size[1], self.down), (0, 255, 255), 1)

        # if len(edges) > 2:
        #     self.k = 254 / (edges[-1] - edges[0])
        #     self.center = int((self.edges[-1] + self.edges[0]) / 2)
        img1 = self.beam_finder(img1)
        return img1

    def beam_finder(self, img_map):
        '''
        Препроцессинг изображения связанный с нахождением центра  на фотографии снятой на вебкамере.
        Препроцессинг состоит из следующих этапов:
            - Выбор R-канала из изображения в системе BGR
            - Применение фильтра Blur с большим окном интегрирования [6000, 1]
            - Перевод изображения в GrayScale для удобства работы
            - Производится интегрирование кадра по оси x, геренируется линия интенсивности вдоль оси y
            - Применение пороговой бинаризации изображения, порог задается аргументом treshold, он высчитывается как
              квантильное значение 0.95 + 3 std
            - Если максимум превышает treshold, то индекс максимума - позиция луча-струи


        :param img_map: Кадр
        '''
        img = np.copy(self.frame)
        img_size = np.shape(img)
        img[:, :, [0, 1]] = img[:, :, [0, 1]] * 0
        img = cv2.blur(img, (6000, 1))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.beam_mask = img

        line = np.mean(img, axis=1, dtype=np.int32)
        treshold = np.quantile(line, 0.95) + 3 * np.std(line)

        if np.amax(line) > treshold:
            self.beam = np.argmax(line)
            img_map = cv2.line(img_map, (0, self.beam), (img_size[1], self.beam), (50, 255, 50), 1)
        img_map = cv2.line(img_map, (0, self.center), (img_size[1], self.center), (250, 255, 250), 1)
        return img_map

    def main_func(self, inverse=False, qtile=0.5):
        img = self.capillar_finder(inverse=inverse)
        img = self.beam_finder(img)
        self.shif_arr.append(self.center - self.beam)
        self.qtile = qtile
        return img

