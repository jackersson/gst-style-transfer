export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/gst-python/plugin:$PWD/gst_filter
python3 run.py
# echo $GST_PLUGIN_PATH
# GST_DEBUG=python:4 gst-launch-1.0 fakesrc num-buffers=10 ! gstblurfilter ! fakesink