import streamlit as st
import os
import read_dicom
import matplotlib.pyplot as plt
import numpy as np
import cv2
import uuid
import pandas as pd
import plotly.express as px

from config import DEST,\
                DICOM_PATH,\
                MASK_DICOM_PATH,\
                patho_map,\
                patho,\
                dcm
from utils import init_data_viz,\
filter_dicom_images_patient_id,\
filter_dicom_mask_patient_id

st.set_page_config(layout="wide")

list_all_mask_dicom_fp_files,\
list_all_dicom_fp_files,\
list_all_image_fp_files,\
list_all_files,\
list_all_dicom_files,\
list_all_mask_dicom_files,\
list_all_patients = init_data_viz()


# save 1 patch (information from st.widgets)
def save_patch(dicom_id, im):
    """
    saves path to disk with a .jpg extension.
    does not keep original data range
    """
    offset = str(anterior_position) + "_" + str(left_max_window)
    random_id = str(uuid.uuid4())
    plt.imsave(os.path.join(DEST,f"{offset}_{dicom_id}_{random_id}.jpg"),
                im)

# save multiple patches coordinates dans un fichier csv
def save_patches(dicom_id,cust_labels):
    """
    saves patch coordinates (y0,y1,x0,x1) in a csv file with the dicom_id = patient id + slice info
    """
    df = pd.DataFrame(cust_labels).transpose()
    df.to_csv(os.path.join(DEST, f"{dicom_id}.csv"), 
            mode="a", 
            header=False)

# create empty lines
def create_space(n=3):
    """
    creates k empty lines in a streamlit viz
    """
    for k in range(n):
        st.header("")

# transforms dicom info into images ( images + mask and returns the center of the tumour mass(es)
def process_images_masks(file_image_name, file_mask_name):

	
    mask_pixel_array = read_dicom.create_dataset(file_mask_name).pixel_array
    viz_mask_array = mask_pixel_array.astype(np.uint8)

    viz_mask_array_x = np.sum(viz_mask_array, axis=1)
    viz_mask_array_y = np.sum(viz_mask_arr, axis=0)
    x_center_mask = np.mean(np.argwhere(viz_mask_array_x>1))
    y_center_mask = np.mean(np.argwhere(viz_mask_array_y>1))

    if debug :
        print(x_center_mask,y_center_mask)

    viz_mask_array = mask_pixel_array.astype(float)

    pixel_array = read_dicom.create_dataset(file_image_name).pixel_array


    viz_mask_array = cv2.merge([viz_mask_array,
				    np.zeros_like(viz_mask_array),
				    np.zeros_like(viz_mask_array)])*255
    viz_central_array = cv2.merge([pixel_array.astype(np.uint8),
				    pixel_array.astype(np.uint8),
				    pixel_array.astype(np.uint8)])

    return viz_central_array,viz_mask_array,pixel_array, x_center_mask, y_center_mask

	
	
# create layout
far_left_pane,left_pane,right_pane,far_right_pane = st.columns([4,4,2,2])

# sidebar with patient id
dcm_id = st.sidebar.selectbox('Patient ID',
    tuple(list_all_patients))

# sidebar with image path
with st.sidebar:
    dcm = st.selectbox('DICOM Images',
    filter_dicom_images_patient_id(list_all_dicom_files, dcm_id))

    # positions to redefine the windows positions 
    anterior_position = st.slider('offset Y', -150,  150, 0)
    left_max_window = st.slider('offset X', -150, 150, 0)

    if st.checkbox ("Need Help?"):
	    st.text("""This tool allows you to explore the\n
non-seminomatous cancer CT scan images\n
You can create samples by exporting\n
the bounding box position.The labels\n
are later processed to generate a\n
dataset for patch classification\n
""")

# left pane with image
with left_pane:
    st.header("CT-scan abdominal image")
    st.header("")
    # looks for pathologic path first
    # based on the exception, will check if the dicom is in the non pathological path
    try:
        
        f_image_name = os.path.join(DICOM_PATH ,"Patho", dcm)
        assert os.path.exists(f_image_name)
        print(f_image_name)
        print("first try")
        subset_images = filter_dicom_images_patient_id(list_all_dicom_files, dcm_id)
        subset_masks = filter_dicom_mask_patient_id(list_all_mask_dicom_files, dcm_id)
        idx = subset_images.index(dcm)

        f_mask_name = os.path.join(MASK_DICOM_PATH ,"Patho", subset_masks[idx])
 
        patho = True
        
        assert os.path.exists(f_mask_name)

	
	viz_central_arr,viz_mask_arr,pixel_arr, x_res_mask, y_res_mask = process_images_masks(f_image_name,f_mask_name)
	

    # in case the subfolder is not patho:
    except AssertionError as e:
        print(e)
        f_image_name = os.path.join(DICOM_PATH ,"Non patho", dcm)
	
        print(f_image_name)
        assert os.path.exists(f_image_name)

        subset_images = filter_dicom_images_patient_id(list_all_dicom_files, dcm_id)
        subset_masks = filter_dicom_mask_patient_id(list_all_mask_dicom_files, dcm_id)
        idx = subset_images.index(dcm)

        f_mask_name = os.path.join(MASK_DICOM_PATH ,"Non Patho", subset_masks[idx])
        
	viz_central_arr,viz_mask_arr,pixel_arr, x_res_mask, y_res_mask = process_images_masks(f_image_name,f_mask_name)

    # in case there is no pixeldata/pixel_array:
    except Exception as e:
        print(e)
        viz_mask_arr = np.zeros((512,512,3))
        pixel_arr = np.zeros((512,512,3))
        viz_central_arr = np.zeros((512,512,3))
    
    # central image 
    try:
        viz_central_masked_image = cv2.addWeighted(src1=viz_central_arr.astype(np.uint8),
                                                    alpha=0.4,
                                                    src2=viz_mask_arr.astype(np.uint8),
                                                    beta=0.6,
                                                    gamma=1)
        st.image(viz_central_masked_image,
        use_column_width = True,
        caption = f_image_name.split("/")[-1] + " " + patho_map[patho])

    except Exception as e:
        print(e)
        st.image(viz_central_arr,
        use_column_width = True,
        caption = f_image_name.split("/")[-1] + " " + patho_map[patho])
        pass

# right pane with image
with right_pane:

    # use an object detector to precisely detect the spine position
    # else use hardcoded values

    pixel_arr= viz_central_masked_image
    spine_arr_left = pixel_arr[-anterior_position+150:-anterior_position+300, -left_max_window+100:-left_max_window+250]
    spine_arr_b_left = pixel_arr[-anterior_position+200:-anterior_position+350, -left_max_window+100:-left_max_window+250]

    spine_arr_front= pixel_arr[-anterior_position+200:-anterior_position+300, -left_max_window+200:-left_max_window+400]
    spine_arr_far_front = pixel_arr[-anterior_position+100:-anterior_position+200, -left_max_window+200:-left_max_window+400]
    
    spine_arr_right = pixel_arr[anterior_position+150:anterior_position+300, 200+left_max_window:350+left_max_window]
    spine_arr_b_right = pixel_arr[anterior_position+200:anterior_position+350, 200+left_max_window:350+left_max_window]

    #Y0, Y1, X0, X1
    labels = { "left": [-anterior_position+150, -anterior_position+300, -left_max_window+100,-left_max_window+250],
    "right":[anterior_position+15,anterior_position+300, 200+left_max_window,350+left_max_window],
    "bottom_left": [-anterior_position+200,-anterior_position+350, -left_max_window+100,-left_max_window+250],
    "bottom_right":[anterior_position+200,anterior_position+350, 200+left_max_window,350+left_max_window]
    }

    # left quadrants
    viz_spine_arr_left = spine_arr_left.astype(np.uint8)

    # front quadrants
    viz_spine_arr_front = spine_arr_front.astype(np.uint8)
    viz_spine_arr_far_front = spine_arr_far_front.astype(np.uint8)

    # right quadrants
    viz_spine_arr_right = spine_arr_right.astype(np.uint8)
    

    try:
        st.header("")
        st.header("")
        st.image(viz_spine_arr_left,
        use_column_width = True,
        caption = "anterior left")

        st.image(viz_spine_arr_right,
        use_column_width = True,
        caption = "anterior right")

        st.image(viz_spine_arr_front,
        use_column_width = True,
        caption = "front spine")


    except:
        pass

# furthest right pane 
with far_right_pane:
    viz_spine_arr_b_left = spine_arr_b_left.astype(np.uint8)
    viz_spine_arr_b_right = spine_arr_b_right.astype(np.uint8)
    viz_spine_arr_far_front = spine_arr_far_front.astype(np.uint8)

    try:
        create_space(2)
        st.image(viz_spine_arr_b_left,
        use_column_width = True,
        caption = "posterior left")

        st.image(viz_spine_arr_b_right,
        use_column_width = True,
        caption = "posterior right")

        st.image(viz_spine_arr_far_front,
        use_column_width = True,
        caption = "abdominal area")

        image_list= [viz_spine_arr_b_left, viz_spine_arr_b_right]
    except:
        pass

# side bar pane 
with st.sidebar:
    side_left,side_mid,side_right = st.columns(3)
    with side_mid:
        st.button(label='Download patches!', on_click=save_patches(dcm,labels))

# furthest left pane
with far_left_pane:
    create_space(3)
    tumor_intensities = [[el] for el in (viz_mask_arr*pixel_arr).ravel() if el != 0]
    df = pd.DataFrame(tumor_intensities, columns =["Tumour Pixel intensity"])
    
    fig = px.histogram(df, 
                        x="Tumour Pixel intensity", 
                        log_y=True,
                        opacity=0.9,
                        color_discrete_sequence=['indianred'])
    print(tumor_intensities)
    st.plotly_chart(fig,use_container_width=True)
