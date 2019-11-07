from PIL import Image, ImageDraw #Подключим необходимые библиотеки.
import random
import io
class kartinka:
    def __init__(self,img):
        self.image = Image.open(io.BytesIO(img))#Image.open(img)
        #self.image = img
        self.draw = ImageDraw.Draw(self.image)  # Создаем инструмент для рисования
        self.width = self.image.size[0]  # Определяем ширину
        self.height = self.image.size[1]  # Определяем высоту
        self.pix = self.image.load()  # Выгружаем значения пикселей

    def image_to_bytes(self):
        b=io.BytesIO()
        self.image.save(b, 'JPEG')
        image_bytes = b.getvalue()
        return image_bytes

    def negative(self):
        for i in range(self.width):
            for j in range(self.height):
                a = self.pix[i, j][0]
                b = self.pix[i, j][1]
                c = self.pix[i, j][2]
                self.draw.point((i, j), (255 - a, 255 - b, 255 - c))

    def shum(self,factor):#добавляем на картинку шум
        for i in range(self.width):
            for j in range(self.height):
                rand = random.randint(-factor, factor)
                a = self.pix[i, j][0] + rand
                b = self.pix[i, j][1] + rand
                c = self.pix[i, j][2] + rand
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                self.draw.point((i, j), (a, b, c))