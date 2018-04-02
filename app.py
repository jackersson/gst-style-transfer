
import logging
import traceback

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

from gst-style-transfer.gstpipeline import GstPipeline

GObject.threads_init()
Gst.init(None)

logging.info("Gstreamer initialized successfully.")


class StyleTransferPipeline(GstPipeline):

    def __init__(self, src):
        style_transfer_plugin_name = 'gststyletransfer'

        command = 'filesrc location={} ! '.format(src)
        command += 'decodebin ! '
        command += 'videoconvert ! '
        command += 'gststyletransfer name={}! '.format(style_transfer_plugin_name)
        command += 'videoconvert ! '
        command += 'gtksink '

        super(StyleTransferPipeline, self).__init__(command)

        # Get element from pipeline by name
        # https://lazka.github.io/pgi-docs/Gst-1.0/classes/Bin.html#Gst.Bin.get_by_name
        ret, element = pipeline.get_element(style_transfer_plugin_name)
        if not ret:
            raise ValueError("Invalid type")

        # Tensorflow Model
        self._model = StyleTransferModel()

        # Pass tensorflow Model to Plugin
        element.set_model(self._model)

    def stop(self):
        # Stop tensorflow model first
        self._model.release()

        # Stop Pipeline
        super(StyleTransferPipeline, self).stop()


class App(object):

    def __init__(self, config):       
        self._active = False
        self._loop = GObject.MainLoop()

        self._pipeline = StyleTransferPipeline(src='video.mpg')
        # Connect to pipeline messages (Catch EOS, STOP)
        self._pipeline.bus().connect("message", self._on_message, None)

    def __del__(self):
        self.stop()

    def _on_message(self, bus, message, loop):
        mtype = message.type

        """
            Gstreamer Message Types and how to parse
            https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
        """
        if mtype == Gst.MessageType.EOS:
            # Call Stop 
            self.stop()
            
        elif mtype == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logging.error("{0}: {1}".format(err, debug))     
            # Call Stop 
            self.stop()                  

        elif mtype == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            logging.warning("{0}: {1}".format(err, debug))             
            
        return True   
    
    def start(self):
        if self._active:
            return
            
        self._active = True

        try:
            self._pipeline.start()
            self._loop.run()
        except:
            traceback.print_exc()
            self.stop()
        
    def stop(self):
        if not self._active:
            return 

        # First stop pipeline
        self._pipeline.stop()

        # Then stop loop
        self._loop.quit()
        self._active = False 