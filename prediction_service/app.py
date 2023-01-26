import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import keras
"""
# RRU Classifier Project
"""
model = tf.keras.models.load_model(r"model.h5")
# artifacts\training\model.h5
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:

    image = Image.open(uploaded_file)
    img = image.resize((300,300))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0) # [batch_size, row, col, channel]
    result = model.predict(img_array) # [[0.99, 0.01], [0.99, 0.01]]
    # y_classes = keras.np_utils.probas_to_classes(result)
    # y_pred=model.predict(np.expand_dims(img_array,axis=0))
    argmax_index = np.argmax(result, axis=1) # [0, 0]
    print(result)
    #print(f'print {y_pred}')
    print(argmax_index)
    print(argmax_index[0])
    if argmax_index[0] == 0:
        st.image(image, caption="predicted: RRU_ON_THE_GROUND")
    else:
        st.image(image, caption='predicted: RRU_ON_THE_TOP')