from __future__ import print_function

import librosa as rosa
import numpy as np

from keras.models import load_model
import tensorflow as tf

from Predict import data
from server.models import Sound,Users
model = load_model('./Predict/training/model.h5')
graph = tf.get_default_graph()

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def loading_sound_model(path):
    return load_model(path)


def predict_sound(time_start, wave, sr, user_id):
    """Predict possible labels in the inputed sound wave and sample rate."""
    # nb_classes = data.voca_size
    threshold = 0.5
    hop = 10
    global model
    """
    get_model = run_once(loading_sound_model)('./Predict/training/model.h5')

    if get_model:
        model = get_model
    if not model:
        print("Model is not loaded")
        return []

    """
    """Load default files."""
    if not wave:
        return {}
        wave, sr = rosa.load('./Predict/data/embe.wav', mono=True, sr=16000)  # resample to 16k
        user_id = 1
        time_start = "2017-12-21 8:10:1"
    """TEST"""
    #wave = np.load('Predict/data/test.npy', allow_pickle=False)
    #sr = 16000
    if (type(wave) is list):
        wave = np.array(wave)
    # get mfcc
    mfcc = rosa.feature.melspectrogram(wave, sr=16000).transpose()
    beg = 0
    end = 80
    labels = {}
    while end < mfcc.shape[0]:
        grain = mfcc[beg:end].copy()
        grain = np.reshape(grain, grain.shape+(1,))
        global graph
        with graph.as_default():
            blah = model.predict(np.array([grain]))
        if(np.max(blah[0]) >= threshold):
            label = str(data.byte_to_label(np.argmax(blah[0])))
        else:
            label = 'unknown'
        if label in labels:
             labels[label] = labels[label] + 1
        else:
            labels[label] = 1
        beg = beg+hop
        end = beg+80
    #print(labels)
    # Save sound to DATABASES
    user = Users.objects.get(id=user_id)
    Sound.objects.create(
        wave=wave.tolist(),
        time_start=time_start,
        sr=sr,
        label=labels,
        user_id=user,
        )
    return labels
