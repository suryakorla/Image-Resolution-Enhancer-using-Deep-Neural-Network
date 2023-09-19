from django.shortcuts import render , redirect 
from django.http import HttpResponse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from requests import Session
from .models import Images
from django.core.files.storage import default_storage
from tensorflow import keras 
from keras.utils import save_img
import PIL
from PIL import Image as im
import numpy as np
from keras.models import load_model
import os
from PIL import Image

#file_path = os.path.join('C:', 'Users', 'John Doe', 'Model', 'model.pth')
#C:\Users\SURYA KIRAN\Desktop\SuperResolution\srcnn.h5
model_path=os.path.join('C:\\','Users','SURYA KIRAN','Desktop','SuperResolution','model3.h5')

new_model = load_model(model_path)


def home(request):
    if request.method == 'POST':
        data = request.POST
        image  = request.FILES['image']
        #drop_down = request.POST.get('dropdown')
        #print(drop_down)
        image_name = default_storage.save(image.name,image)
        image_url = default_storage.path(image_name)
        img = PIL.Image.open(image_url)
        img_arr = np.array(img) 
        test_img = img_arr/255.
        input_to_model = np.array([test_img])
        hr_output = new_model.predict(input_to_model)
        out = hr_output[0]
        #print(out.shape)
        media_path=os.path.join('C:\\','Users','SURYA KIRAN','Desktop','SuperResolution','media','low_res','high_res')
        path = media_path+'\\hr_img_of'+str(image_name)
        save_img(path, out)
        temp = Images.objects.create(
          image_low_res = str(image_name),
          image_high_res = 'high_res/'+'hr_img_of'+str(image_name)
        )
        return redirect('convert-photo')

    context = {}
    return render(request,'homepage/add_photo.html',context)



def convert(request):
  Image_data = Images.objects.last()
  context = {'Image_data':Image_data}
  return render(request,'homepage/convert_photo.html',context)

