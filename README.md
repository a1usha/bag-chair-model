# Bag chair detection model

Machine learning lives here :robot:

I’m going to train an object detector to detect free and occupied bagchairs in an image or video for [sandbags monitor project](https://github.com/a1usha/NSU_project_v2.0). For this purpose, I will use the deep learning technique called [Transfer learning](https://en.wikipedia.org/wiki/Transfer_learning#:~:text=Transfer%20learning%20(TL)%20is%20a,when%20trying%20to%20recognize%20trucks.) with help of [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).

What is Transfer Learning
---
In most cases, training a convolutional neural network is a difficult and time-consuming process that requires a lot of **computing power** and **data**. In modern realities, both components are quite possible to find - [ImageNet](http://www.image-net.org/) (or others) as data library and [Google Colab](https://colab.research.google.com/) (or others) as power. However, the use of cloud computations can cost the user a pretty penny. 

Therefore, in order to speed up the process and save the wallet, people use **transfer learning**: use already trained (mostly called pre-trained) convolution network as the starting point for their own model (use pre-trained weights as the initial weights for own model). 

The whole process can be divided into three large steps (however, this is how any model training works):

- Collect data - This may already be data collected by someone (as ImageNet) or data received manually (this is my case, I have not found large collections of images of bagchairs other than those that can be found in Google Images).

- Annotate the data - In short, it is the process of marking the location of objects and specifying their classes in the data.

- Fine-tune the net - Re-train the weights of the ConvNet using regular [backpropagation](https://en.wikipedia.org/wiki/Backpropagation).


Tensorflow object detection API
---
Not so far ago, Tensorflow developers made available an Object Detection API for simplifying process of fine-tuning of a pre-trained model. API is provided as a set of scripts, which with minor modifications can be used for your own purposes.

Next, I will describe my own experience and approach to using the above methods.

1) I **collected images** and **annotated** them. There are several tools for annotating dataset that can be found on the Internet - I used [MakeSence](https://www.makesense.ai/). It is important to note that there are several annotation formats - COCO, Pascal VOC and YOLO. The code in the future will also depend on the chosen format. I used Pascal VOC, it stores annotation in XML file. Also, you should create label map file (.pbtxt) for future processing.
```
<annotation>
	<folder>images</folder>
	<filename>image0.jpg</filename>
	<path>download_data/downloads/images/image0.jpg</path>
	<source>
		<database>Unspecified</database>
	</source>
	<size>
		<width>522</width>
		<height>481</height>
		<depth>3</depth>
	</size>
	<object>
		<name>occupied_bagchair</name>
		<pose>Unspecified</pose>
		<truncated>Unspecified</truncated>
		<difficult>Unspecified</difficult>
		<bndbox>
			<xmin>4</xmin>
			<ymin>2</ymin>
			<xmax>521</xmax>
			<ymax>479</ymax>
		</bndbox>
	</object>
</annotation>
```

pascal_label_map.pbtxt file
```
item {
  id: 1
  name: 'empty_bagchair'
}

item {
  id: 2
  name: 'occupied_bagchair'
}
```

More info about annotaion formats: *[Image data labeling and annotation](https://towardsdatascience.com/image-data-labelling-and-annotation-everything-you-need-to-know-86ede6c684b1)*

2) **Create TF Records**. I took the [script](https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_pascal_tf_record.py) from the API as a basis and changed it a little (rather, simplified it). It is worth mentioning why this format is needed - TFRecord is Tensorflow's own binary storage format, using it for storage of dataset can have significant impact on performance of import pipeline and for training in future. More info: *[Tensorflow Records? What they are and how to use them](https://medium.com/mostly-ai/tensorflow-records-what-they-are-and-how-to-use-them-c46bc4bbb564)*

```
python create_tfrecords_from_xml.py `
     --image_dir=data\images `
     --annotations_dir=data\annotations `
     --label_map_path=data\label_map\pascal_label_map.pbtxt `
     --output_path=tf_data\
```

3) **Choose and download pre-trained model**. In our main [project](https://github.com/a1usha/NSU_project_v2.0), we are planning to use single-board computer called Raspberry Pi 4 for model inference. Therefore, models adapted to work on mobile devices were considered as a basis for training. MobileNet is a good example of such a model. The creators of this model architecture have achieved great speed by using [depthwise separable convolutions](https://machinethink.net/blog/googles-mobile-net-architecture-on-iphone/). As a result, my choice fell on an model called SSD MobileNet-v2, which is an [improved version](https://machinethink.net/blog/mobilenet-v2/#:~:text=In%20V1%20the%20pointwise%20convolution,the%20number%20of%20channels%20smaller.&text=This%20is%20also%20a%201,goes%20into%20the%20depthwise%20convolution.) of MobileNet-v1. The pre-trained model can be downloaded from [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md).

4) **Fill in the required fields of the configuration file**. Typically, such a file is called *pipeline.config*. It is necessary to specify the path to the train/test *tfrecord* files, number of classes (in my case - 2), path to label map file and path to checkpoints (downloaded model) in it.

5) **Train the model**. I used Google Colab to speed up my training process. It provides user with powerfull GPU for free (as I remember, for ~9 hours). I prepared [this](https://github.com/a1usha/bag-chair-model/blob/main/train.ipynb) notebook for transfer learning using Tensorflow Object Detection API. It is worth noting that even with a powerful graphics accelerator, the learning process can take a fair amount of time.

6) **Export the frozen graph**. This part also included to the training [notebook](https://github.com/a1usha/bag-chair-model/blob/main/train.ipynb).

7) **Convert model to tf lite format** (optional). I prepared this [notebook](https://github.com/a1usha/bag-chair-model/blob/main/export_tflite.ipynb) for model tflite model convertion. You can use [this repository](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi) to run your tflite model on a Raspberry Pi or Android device

8) **Start using your model**. I prepared this [notebook](https://github.com/a1usha/bag-chair-model/blob/main/results.ipynb) with my results.


Results
---
After successfully completing model training (honestly, my free Colab session time has expired :alien:), I tested the model on a few photos:

![case 1](https://github.com/a1usha/bag-chair-model/blob/main/results/tst_1.png)

![case 2](https://github.com/a1usha/bag-chair-model/blob/main/results/tst_2.png)

![case 3](https://github.com/a1usha/bag-chair-model/blob/main/results/tst_3.png)

However, there are small flaws ...  
![case 4](https://github.com/a1usha/bag-chair-model/blob/main/results/tst_4.png)

At the moment I have a couple of ideas on how to improve the quality of the model, they all relate to data preparation.  
<p align="center">
  <img src="https://github.com/a1usha/bag-chair-model/blob/main/results/truth.png" />
</p>

*to be continued...*
