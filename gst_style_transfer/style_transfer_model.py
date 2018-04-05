"""
    Dan implementation
    Model name: _____
"""

import cv2
import os
import copy
import numpy as np
import tensorflow as tf

def parse_graph(model_path):

    model_path = os.path.abspath(model_path)
    assert os.path.isfile(model_path), "Invalid filename {}".format(model_path)        
        
    with tf.gfile.GFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def


class StyleTransferModel(object):

    DEFAULT_CONFIG = {
        'model': 'filename',
        'gpu': False
    }

    def __init__(self, **config):

        """ 
        self.config = copy.copy(self.DEFAULT_CONFIG)
        for key in self.config:
            if key in config:
                self.config[key] = config[key]

        # Only check for extra config keys in top-level class
        # assert not config, 'Unrecognized configs: %s' % config

        graph_def = parse_graph(self.config['model'])
        config, device = create_config(self.config['gpu'])

        device = '/device:CPU:0'
        if on_gpu:
            device = '/device:GPU:0' 
            config = tf.ConfigProto(log_device_placement=log_device_placement)
            config.gpu_options.allow_growth = True
        else:
            config = tf.ConfigProto(log_device_placement=log_device_placement,
                                    device_count={'GPU': 0})

        with tf.device(device):
            graph = tf.Graph()            
            with graph.as_default():
                tf.import_graph_def(graph_def, name="")
                return graph

        self._session = tf.Session(graph=graph, config=config)

        self._input = graph.get_tensor_by_name('import/input_image:0')
        self._output = graph.get_tensor_by_name('import/prediction:0') 

        self._width = self.config['width']
        self._height = self.config['height']
        self._threshold = self.config['threshold']
        """

    def process(self, image):

        if not isinstance(image, np.ndarray):
            raise ValueError('Invalid data. {} != {}'.format(type(image), 'np.ndarray'))
        print("Process image")
        return image

    def release(self):
        try:
            if self._session is not None:
                self._session.close()
                self._session = None
        except Exception as e:
            pass

    def __del__(self):
        self.release()