# list all dicom/images (full_path)
IMAGE_PATH = "/Users/assansanogo/Downloads/testis/*.png"
INPUT_PATH = "/Users/assansanogo/Downloads/testis"

DICOM_PATH = "/Users/assansanogo/Downloads/TGNS/DICOM"
MASK_DICOM_PATH = "/Users/assansanogo/Downloads/TGNS/contours"
DEST = "/Users/assansanogo/Downloads/patches"

# mapping (True:pathologic  False:non pathologic)
patho_map = {True: "patho",
        False: "non-patho"}
patho = False

dcm = None