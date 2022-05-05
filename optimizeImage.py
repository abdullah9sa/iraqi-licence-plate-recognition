from re import X
from pyanime4k import ac
import pyanime4k
import numpy as np
from PIL import Image, ImageEnhance

def Opti(img):
    parameters = ac.Parameters()

    # enable HDN for ACNet
    parameters.HDN = True

    a = ac.AC(
        managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
        type=ac.ProcessorType.OpenCL_ACNet
    )
    #img = Image.open(r"D:\Temp\anime4k\p1.png").convert("RGB")
    img = np.array(img)

    # BGR, RGB and YUV444 is supported
    a.load_image_from_numpy(img, input_type=ac.AC_INPUT_RGB)
    # start processing
    a.process()

    # save image to numpy array
    new_img = a.save_image_to_numpy()
    new_img  = Image.fromarray(new_img)
    new_img = adjustImage(new_img)
    new_img = np.asarray(new_img)

    return new_img


def adjustImage(im):
    #brightness
    enhancer = ImageEnhance.Brightness(im)
    factor = 1.5 #gives original image
    im_output = enhancer.enhance(factor)
    #Contrast
    enhancer = ImageEnhance.Contrast(im_output)
    factor = 1.3 #gives original image
    im_output = enhancer.enhance(factor)
    #Sharpness
    enhancer = ImageEnhance.Sharpness(im_output)
    factor = 1.5 #gives original image
    im_output = enhancer.enhance(factor)

    return im_output




# x = Image.open("./p1.jpg")
# Opti(x)
