import subprocess

performance = ['sudo', 'sh', '-c', 'echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor']
powersave = ['sudo', 'sh', '-c', 'echo powersave > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor']

subprocess.check_call(performance)

import argparse
import numpy as np
import tensorflow.lite as tflite
import tensorflow as tf
import zlib
import os
import sys

tfModel = "./model.tflite"
dataset_dir = "./test_ds_True"
mfcc = True

interpreter = tflite.Interpreter(model_path=tfModel)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']

if mfcc is True:
    tensor_spec =(tf.TensorSpec([None,49,10,1], dtype=tf.float32), tf.TensorSpec([None], dtype=tf.int64))
else:
    tensor_spec =(tf.TensorSpec([None,32,32,1], dtype=tf.float32), tf.TensorSpec([None], dtype=tf.int64))

test_ds = tf.data.experimental.load(dataset_dir, tensor_spec) 
test_ds= test_ds.unbatch().batch(1)

accuracy=0
count= 0 
for x, y_true in test_ds: 
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    y_pred = interpreter.get_tensor(output_details[0]['index'])
    y_pred = y_pred.squeeze()
    y_pred = np.argmax(y_pred)
    y_true = y_true.numpy().squeeze()
    accuracy += y_pred == y_true
    count += 1 

accuracy/=float(count)
print("Accuracy {}".format(accuracy*100))