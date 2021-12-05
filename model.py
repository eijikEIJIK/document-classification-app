import tensorflow as tf
import numpy as np
import shutil
import glob

def get_category(x):
  if len(x)!=4:
    return 0
  max_index = np.argmax(x)
  cat_list=["building","document","food","person"]

  return cat_list[max_index]

def get_document_img():
    pred_dir='upload'
    img_li=[]
    files = glob.glob("upload/*")
    for i,img_name in enumerate(files):
        im = tf.io.read_file(img_name)
        im = tf.image.decode_jpeg(im, channels=3)
        #画像のリサイズ
        im=tf.image.resize(im, [128, 128])/255
        img_li.append(im)
    img_li=np.array(img_li)

    save_model_path = 'model2.h5'
    new_model=tf.keras.models.load_model(save_model_path)
    results=new_model.predict(img_li)
    for i in range(len(results)):
        img_name=files[i]
        print(img_name)
        print(get_category(results[i]))
        if get_category(results[i])=="document":
            shutil.move(img_name, 'output/document/')
        else:
            shutil.move(img_name, 'output/others/')


