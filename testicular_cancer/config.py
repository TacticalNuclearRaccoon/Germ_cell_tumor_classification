import os

# list all dicom/images (full_path)

# HOME path 
HOME = os.getenv("TEST_CANCER_HOME", "/Users/assansanogo/Downloads")

# binarized images
IMAGE_PATH = os.path.join(HOME,"testis/*.png")
INPUT_PATH = os.path.join(HOME,"testis")
# original DICOMS               
DICOM_PATH = os.path.join(HOME,"TGNS/DICOM")
MASK_DICOM_PATH = os.path.join(HOME,"/TGNS/contours")
DEST = os.path.join(HOME, "patches")

# mapping (True:pathologic  False:non pathologic)
patho_map = {True: "patho",
        False: "non-patho"}

# initial flag
patho = False

# set dcm to None
dcm = None
