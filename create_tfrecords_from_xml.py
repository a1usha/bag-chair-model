# This is a modified example of using 
# https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_pascal_tf_record.py
# The structure should be like PASCAL VOC format dataset
#   +Dataset
#   +Annotations
#   +JPEGImages
# python create_tfrecords_from_xml.py   --image_dir=dataset/JPEGImages 
#                                       --annotations_dir=dataset/Annotations 
#                                       --label_map_path=object-detection.pbtxt 
#                                       --output_path=data.record

import hashlib
import io
import logging
import os
import random
import logging

from lxml import etree
import PIL.Image
import tensorflow.compat.v1 as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util


flags = tf.app.flags
flags.DEFINE_string('image_dir', '', 'Path to image directory.')
flags.DEFINE_string('annotations_dir', '', 'Path to annotations directory.')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('label_map_path', 'data/pascal_label_map.pbtxt',
                    'Path to label map proto')
FLAGS = flags.FLAGS


def dict_to_tf_example(data, image_dir, label_map_dict):
    """Convert XML derived dict to tf.Example proto.

    Notice that this function normalizes the bounding
    box coordinates provided by the raw data.

    Arguments:
        data: dict holding XML fields for a single image (obtained by
          running dataset_util.recursive_parse_xml_to_dict)
        image_dir: Path to image directory.
        label_map_dict: A map from string label names to integers ids.

    Returns:
        example: The converted tf.Example.
    """

    full_path = os.path.join(image_dir, data['filename'])

    with tf.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()

    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)
    
    key = hashlib.sha256(encoded_jpg).hexdigest()

    width = int(data['size']['width'])
    height = int(data['size']['height'])

    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []

    try:
        for obj in data['object']:
            xmin.append(float(obj['bndbox']['xmin']) / width)
            ymin.append(float(obj['bndbox']['ymin']) / height)
            xmax.append(float(obj['bndbox']['xmax']) / width)
            ymax.append(float(obj['bndbox']['ymax']) / height)
            classes_text.append(obj['name'].encode('utf8'))
            classes.append(label_map_dict[obj['name']])
    except KeyError:
        print(data['filename'] + ' without objects!')

    difficult_obj = [0]*len(classes)

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(data['filename'].encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(data['filename'].encode('utf8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
        'image/object/difficult': dataset_util.int64_list_feature(difficult_obj)
    }))

    return example


def generate_tf_record(filename, label_map_dict, annotations_dir, image_dir, examples_list):
    writer = tf.python_io.TFRecordWriter(filename)

    for idx, example in enumerate(examples_list):
        if example.endswith('.xml'):
    
            if idx % 10 == 0:
                logging.info('On image %d of %d', idx, len(examples_list))

            path = os.path.join(annotations_dir, example)
            with tf.gfile.GFile(path, 'r') as fid:
                xml_str = fid.read()
            xml = etree.fromstring(xml_str)
            data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

            tf_example = dict_to_tf_example(data, image_dir, label_map_dict)

            writer.write(tf_example.SerializeToString())

    writer.close()


def main(_):

    random.seed(11)
    
    label_map_dict = label_map_util.get_label_map_dict(FLAGS.label_map_path)

    image_dir = FLAGS.image_dir
    annotations_dir = FLAGS.annotations_dir
    logging.info('Reading from dataset: ' + annotations_dir)
    examples_list = os.listdir(annotations_dir)

    # Divide data to train and test parts
    random.shuffle(examples_list)
    total_examples_len = len(examples_list)
    train_examples_len = int(total_examples_len * 0.95)
    
    train_examples = examples_list[:train_examples_len]
    test_examples = examples_list[train_examples_len:]

    logging.info('Train size: %d, test size: %d', len(train_examples), len(test_examples))

    
    train_output_path = os.path.join(FLAGS.output_path, 'bagchair_train.record')
    val_output_path = os.path.join(FLAGS.output_path, 'bagchair_test.record')
    
    generate_tf_record(train_output_path, label_map_dict, annotations_dir,
                   image_dir, train_examples)
    generate_tf_record(val_output_path, label_map_dict, annotations_dir,
                   image_dir, test_examples)


if __name__ == '__main__':
    tf.app.run()