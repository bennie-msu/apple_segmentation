# Directory to save logs and trained model

MODEL_DIR = 'weights/'

# Local path to trained weights file
COCO_MODEL_PATH = MODEL_DIR +'model.h5'
print (COCO_MODEL_PATH)

import sys
sys.path.insert(0, "Mask_RCNN/")

from Mask_RCNN import apple_detection_mask_rcnn
class InferenceConfig(apple_detection_mask_rcnn.BalloonConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.7

config = InferenceConfig()
config.display()

from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True, exclude=["mrcnn_bbox"])
class_names = ['bg', ' ']

from construct_via_json import *

import os
import sys
import random
import math
import numpy as np
import skimage.io
import time
import glob

import matplotlib
import matplotlib.pyplot as plt
# for the server without display
plt.switch_backend('agg')
# IMAGE_DIR = '/content/Mask_RCNN/dataset/val'
# file_names = next(os.walk(IMAGE_DIR))[2]
# img = os.path.join(IMAGE_DIR, random.choice(file_names))



# img_dir = 'images/'
# imgs = []
# for i in range(17):
#   imgs.append(img_dir + str(i+1) + '.jpg')
  
# imgs.append(img_dir + '1000.jpg')
# imgs.append(img_dir + '1013.jpg')
# imgs.append(img_dir + '1017.jpg')
if len(sys.argv) != 3 or not os.path.isdir(sys.argv[1]) or not os.path.isdir(sys.argv[2]):
  print('arguments are wrong!')

else:
  input_dir = sys.argv[1]
  output_dir = sys.argv[2]
  imgs = glob.glob(os.path.join(input_dir, '*.jpg'))
  # imgs = ['images2/'+img for img in imgs]

  cost = {}

  via_label_encoder = LabelJsonEncoder('test2')

  for img in imgs:
    image = skimage.io.imread(img)
    start = time.time()
    # Run detection
    size = image.shape
    print(size[0]/2)


    results = model.detect([image], verbose=1)
    r = results[0]

    # print('\nResult:')
    # duration = time.time() - start;
    # print('The detection time is: %.2fs' % (duration))
    # print('The count of apples is ', len(r['class_ids']))

    # cost[img.split('/')[-1]] =  duration

    visualize.save_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                class_names, filename = os.path.join(output_dir, img.split('/')[-1]), colors= [(0.2, 0.2, 0.95)]*100, figsize=(12, 12))
    via_label_encoder.add_label_set(filename=img.split('/')[-1], img_size = 373956, bboxes=r['rois'])
    # print(r['rois'])
    # origial image
    # plt.figure(figsize=(12,12))
    # plt.axis('off')
    # plt.title(img.split('/')[-1]) 
    # plt.imshow(image)
    # plt.show()

    # print('\n\n')
    # print(np.linspace(1, len(imgs), len(imgs)))
    # print(cost.values)

  via_label_encoder.commit()



  # # pre_cost = [20.06, 15.6, 15.75, 15.76, 15.58, 15.49, 15.94, 15.58, 15.55, 15.60, 15.47, 16.01, 16.21, 15.75, 17.11, 15.98, 15.87, 15.78, 15.63, 15.76]
  # plt.figure(figsize=(12,12))
  # x = np.linspace(1, len(imgs), len(imgs))
  # y = np.linspace(0.25, 0.25, len(imgs))
  # plt.plot(x, cost.values(), 'bo-', x, y,'g--')
  # plt.ylabel('time(s)')
  # plt.xlabel('No. ')
  # plt.legend(['GPU Accellerated', 'Expection 0.25s'])
  # plt.show()
  # plt.savefig('fig.jpg')
