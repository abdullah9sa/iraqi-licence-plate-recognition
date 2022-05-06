import easyocr
from googletrans import Translator
import json
from difflib import SequenceMatcher
import optimizeImage
reader = easyocr.Reader(['ar'])
from PIL import Image


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


words = ["اربيل",
         "الانبار",
         "بابل",
         "بغداد",
         "البصرة",
         "حلبجة",
         "دهوك",
         "القادسية",
         "ديالى",
         "ذي قار",
         "السليمانية",
         "صلاح الدين",
         "كركوك",
         "كربلاء",
         "المثنى",
         "ميسان",
         "النجف",
         "نينوى",
         "واسط",
         "خصوصي",
         "فحص",
         "العراق",
         "اجرة",
         "حمل",
         "مؤقت"]


def AssignWord(wrd):
    bestMatch = ""
    prevPrec = 0.0
    for preDefinedWord in words:
        precision = similar(wrd, preDefinedWord)

        if((precision > prevPrec) and (precision > 0.2)):
            bestMatch = preDefinedWord
            prevPrec = precision

    return bestMatch


def ReadLic(img , isOptimize):

    if(isOptimize):
        img = optimizeImage.Opti(img)

    thisdict = {
        "number": "",
        "state": "",
        "city": "",
    }

    allData = reader.readtext(img)
    # print(reader.readtext(img))

    punk = []
    for det in allData:

        punk.append(det[1])
        # print(det[1])

        if (similar("٠١٢٣٤٥٦٧٨٩" ,det[1] ) > 0.0):
            thisdict["number"] = det[1]
        else:
            if(thisdict["state"] == ""):
                thisdict["state"] = AssignWord(str(det[1]))
            elif (thisdict["city"] == ""):
                thisdict["city"] = AssignWord(str(det[1]))

                
            #ar = ar

    # print(thisdict)

    return thisdict
