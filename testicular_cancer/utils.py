import os
import glob2
from config import DEST,INPUT_PATH, DICOM_PATH, MASK_DICOM_PATH, patho_map, patho,dcm
import pydicom


def init_data_viz():
    """
    list dicom images, dicom masks & binarized images
    """
    # list all masks_dicom, images_dicom, (custom folder: processed image)
    list_all_mask_dicom_fp_files  = glob2.glob(os.path.join(MASK_DICOM_PATH, "*/*"))
    list_all_dicom_fp_files  = glob2.glob(os.path.join(DICOM_PATH, "*/*"))
    list_all_image_fp_files = glob2.glob(os.path.join(INPUT_PATH, "*.png"))

    # list all dicom/images (rel_path)
    # relative file names
    
    list_all_files = [os.path.basename(fi) for fi in list_all_image_fp_files]
    list_all_dicom_files = [os.path.basename(fi) for fi in list_all_dicom_fp_files]
    list_all_mask_dicom_files = [os.path.basename(fi) for fi in list_all_mask_dicom_fp_files]
    
    # list all patients ID
    list_all_patients = set([fi.split("_")[-1].split("-")[0] for fi in list_all_dicom_files])

    return  list_all_mask_dicom_fp_files,\
            list_all_dicom_fp_files,\
            list_all_image_fp_files,\
            list_all_files,\
            list_all_dicom_files,\
            list_all_mask_dicom_files,\
            list_all_patients  

def filter_dicom_images_patient_id(list_dicom_files, dcm_id):
    """
    returns the files pertaining to a given ID
    works with masks & images 
    """
    # original filenamees (TODO: reorganize the image data )
    res = [fi for fi in list_dicom_files if fi.split("_")[-1].split("-")[0] in [dcm_id] ]
    return sorted(res)

def int_suffix(x):
    """
    extracts the file's suffix & convert it to integer
    """
    # original filenames (TODO: get the patient id from current filename)
    # the int allows to convert the suffix & sort ascendingly
    return int( os.path.basename(x).split(".dcm")[0].split("_")[-1])

def filter_dicom_mask_patient_id(list_dicom_files, dcm_id):
    """
    filter DICOM files by the suffix in ascending order
    """
    # original filenames (TODO: reorganize the mask data )
    res = [fi for fi in list_dicom_files if fi.split("_")[1] in [dcm_id] ]
    # employee ID formatted with "Corresponding id _..."
    return sorted([fi for fi in res if os.path.basename(fi).split("_mask_")[0] == f"Corresponding id _{dcm_id}"] ,key= int_suffix)

def safe_read_dicom(x):
    """
    extract pixelarray from a dcm_path
    """
    dataset = pydicom.dcmread(x, force=True)
    dataset.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    arr = dataset.pixel_array
    return arr
