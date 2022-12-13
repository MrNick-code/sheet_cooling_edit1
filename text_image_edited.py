import numpy as np
from PIL import Image, ImageDraw, ImageFont

class InitialCondition:

    def __init__(self):
        pass

    def gera_caracteres(self, text='COOL', nx1=101, ny1=101, fontsize=24):

        backcolor = 0
        textcolor = 1

        font = ImageFont.truetype("FreeSerif_edited.ttf", fontsize, encoding="unic")
        img = Image.new('L', (nx1, ny1), color=backcolor)

        d = ImageDraw.Draw(img)
        d.text((10, 150), text, fill=textcolor, font=font)

        return np.array(img)[::-1, :]

    def gera_forma(self, forma='anel circular', nx=101, ny=101, dx=0.01, dy=0.01, Tmax=800, T0=np.zeros([101,101])):
        
        if forma == "anel circular":
            for i in range(nx):
                for j in range(ny):
                    if ( ( (i*dx-0.5)**2+(j*dy-0.5)**2 <= 0.1)
                        & ((i*dx-0.5)**2+(j*dy-0.5)**2 >= .05) ):
                        T0[i,j] = Tmax
            pass
        elif forma == "anel elíptico":
            for i in range(nx):
                for j in range(ny):
                    if ( ( ((i*dx-0.5)/1.2)**2+((j*dy-0.5)/1.5)**2 <= 0.1)
                        & (((i*dx-0.5)/1.2)**2+((j*dy-0.5)/1.5)**2 >= .05) ):
                        T0[i,j] = Tmax
            pass
        elif forma == "circulo":
            for i in range(nx):
                for j in range(ny):
                    if ((i*dx-0.5)**2 + (j*dx-0.5)**2 <= 0.1):
                        T0[i, j] = Tmax
            pass
        elif forma =="furo circular":
            for i in range(nx):
                for j in range(ny):
                    if ((i*dx-0.5)**2 + (j*dy-0.5)**2 >= .05):
                        T0[i, j] = Tmax
            pass
        else:
            print('Error')
            pass

        return T0
