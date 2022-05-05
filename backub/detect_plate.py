import tensorflow as tf
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import cv2 
IMAGE_SIZE = (2, 1) # Output display size as you want
import matplotlib.pyplot as plt
import os
from numpy import asarray
cwd = os.getcwd()
PATH_TO_SAVED_MODEL= cwd + "/model/inference_graph/saved_model"
print('Loading model...', end='')
import io
# Load saved model and build the detection function
detect_fn=tf.saved_model.load(PATH_TO_SAVED_MODEL)
print('Done!')


def Detect_Plate(img):

    #Loading the label_map
    category_index=label_map_util.create_category_index_from_labelmap(cwd+"\model\label_map.pbtxt",use_display_name=True)
    #category_index=label_map_util.create_category_index_from_labelmap([path_to_label_map],use_display_name=True)

    # def load_image_into_numpy_array(path):
    #     return np.array(Image.open(path))
    def load_image_into_numpy_array(path):
        return np.array(path)


    # reader = easyocr.Reader(['ar']) # this needs to run only once to load the model into memory

    # stringy = "(" + str(n+1) + ")"
    # image_path = "D:\\garbg\\ (1).jpg"
    #print('Running inference for {}... '.format(image_path), end='')

    # image_np = load_image_into_numpy_array(image_path)
    image_np = load_image_into_numpy_array(img)
    image_np = asarray(img)

    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=False,
        max_boxes_to_draw=200,
        min_score_thresh=.4, # Adjust this value to set the minimum probability boxes to be classified as True
        agnostic_mode=False)

    #%matplotlib inline
    # plt.figure(figsize=IMAGE_SIZE, dpi=200)
    # plt.axis("off")
    # plt.imshow(image_np_with_detections)
    # plt.show()

    #so detection has happened and you've got output_dict as a
    # result of your inference
    # This is the way I'm getting my coordinates
    boxes = detections['detection_boxes']
    # get all boxes from an array
    max_boxes_to_draw = boxes.shape[0]
    # get scores to get a threshold
    scores = detections['detection_scores']
    # this is set as a default but feel free to adjust it to your needs
    min_score_thresh=.5
    # iterate over all objects found
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        # 
        if scores is None or scores[i] > min_score_thresh:
            # boxes[i] is the box which will be drawn
            class_name = category_index[detections['detection_classes'][i]]['name']
            print ("This box is gonna get used", boxes[i], detections['detection_classes'][i])

    xmin = boxes[0][1]
    xmax = boxes[0][3]
    ymin = boxes[0][0]
    ymax = boxes[0][2]#*812

    imageX = image_np_with_detections.shape[1]
    imageY = image_np_with_detections.shape[0]
    ymin = int(ymin*imageY)
    ymax = int(ymax*imageY)
    xmin = int(xmin*imageX)
    xmax = int(xmax*imageX)

    image_np_with_detections = image_np_with_detections[ymin:ymax,xmin:xmax]

    # cv2.imshow("asd", cv2.resize(image_np_with_detections,(700, 700)))
    # cv2.waitKey(0) 
    # #closing all open windows 
    # cv2.destroyAllWindows() 
    #imgRes = Image.fromarray(image_np_with_detections, 'RGB')
    # array = np.arange(0, 737280, 1, np.uint8)
    # array = np.reshape(image_np_with_detections, (1024, 720))
    def image_to_byte_array(image: Image) -> bytes:
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    data = Image.fromarray(image_np_with_detections, 'RGB')

    # res = image_to_byte_array(data)
    return(data)

    return([ymin,ymax,xmin,xmax])
