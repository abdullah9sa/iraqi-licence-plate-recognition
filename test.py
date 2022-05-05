from PIL import Image

def dataURI():
    try:  # Python 3
        from urllib.parse import quote
    except ImportError:  # Python 2
        from urllib import quote
    from base64 import b64encode
    from io import BytesIO

    png_output = BytesIO()
    png_output = Image.open("./p1.jpg")

    # canvas.print_png(png_output)
    data = b64encode(png_output.getvalue()).decode('ascii')
    data_url = 'data:image/jpeg;base64,{}'.format(quote(data))
    return data_url


print(dataURI())
# from PIL import Image, ImageEnhance

# im = Image.open("./static/p1_output.jpg")

# #brightness
# enhancer = ImageEnhance.Brightness(im)
# factor = 1.5 #gives original image
# im_output = enhancer.enhance(factor)
# #Contrast
# enhancer = ImageEnhance.Contrast(im_output)
# factor = 1.3 #gives original image
# im_output = enhancer.enhance(factor)
# #Sharpness
# enhancer = ImageEnhance.Sharpness(im_output)
# factor = 1.5 #gives original image
# im_output = enhancer.enhance(factor)

im_output.show()
# from difflib import SequenceMatcher

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# # {'number': '', 'state': 'حمل', 'city': 'بغداد', 'code': ''}
# # [['?', '٣٦٤٥٧', '0', '3 6 ، 5 1', 'ممل', 'بنداد']]
# print(similar("٠١٢٣٤٥٦٧٨٩","١"))



# words = ["اربيل",
# "الانبار",
# "بابل",
# "بغداد",
# "البصرة",
# "حلبجة",
# "دهوك",
# "القادسية",
# "ديالى",
# "ذي قار",
# "السليمانية",
# "صلاح الدين",
# "كركوك",
# "كربلاء",
# "المثنى",
# "ميسان",
# "النجف",
# "نينوى",
# "واسط",
# "خصوصي",
# "فحص",
# "العراق",
# "اجرة",
# "حمل"]
