class Bitmap:
    def __init__(self,filename):
        self.filename = filename
        print(f'Loading image from {filename}')

    def draw(self):
        print(f'Drawing image {self.filename}')

def draw_image(image):
    print('About to draw image')
    image.draw()
    print('Done drawing image')

class LazyBitmap:
    def __init__(self,filename):
        self.filename = filename
        self._bitmap = None
    def draw(self):
        if not self._bitmap:
            self._bitmap = Bitmap(self.filename)
        self._bitmap.draw()



#bmp = Bitmap('facepalm.jpg')
# draw_image(bmp)

bmp = LazyBitmap('facepalm.jpg')
bmp.draw()
bmp.draw()
bmp.draw()