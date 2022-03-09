import pydicom

def create_dataset(file_path):
    '''
    function which creates dataset with LittleEndian format (necessary for truncated DICOM files)
    '''

    im_dataset = pydicom.dcmread(file_path, force=True)
    im_dataset.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    return im_dataset
