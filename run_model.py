import tensorflow as tf
import numpy as np
from PIL import Image

class modelRunner:
    
    # Provide with frozen graph path 
    # e.g. 'trained_model/frozen_inference_graph.pb'
    def __init__(self, frozen_graph_path):
        self.detection_graph = tf.Graph()

        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(frozen_graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


    def __load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


    # Method to call deep learning 
    # Specify image path 
    # Returns dictionary with keys:
    #   total - number of detected bagchairs
    #   empty - number of empty bagchairs
    #   occupied - number of occupied bagchairs
    def run_inference(self, image_path):
        with self.detection_graph.as_default():
            with tf.compat.v1.Session(graph=self.detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                
                image = Image.open(image_path)
                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = self.__load_image_into_numpy_array(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                out_dict = self.__filter_output(scores, classes)

                return out_dict


    def __filter_output(self, scores, classes):
        classes = np.squeeze(classes)
        scores = np.squeeze(scores)

        empty_bagchairs = 0
        occupied_bagchairs = 0

        for cl, sc in zip(classes, scores):
            if sc > 0.0:
                if cl == 1.0:
                    empty_bagchairs += 1
                else:
                    occupied_bagchairs += 1
        
        out_dict = { 
            'total': empty_bagchairs + occupied_bagchairs,
            'empty': empty_bagchairs,
            'occupied': occupied_bagchairs
        }

        return out_dict
