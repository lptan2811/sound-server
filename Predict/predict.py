from __future__ import print_function

import librosa as rosa
import numpy as np

from keras.models import load_model

from Predict import data


def predict_sound(wave, sr):
    """Predict possible labels in the inputed sound wave and sample rate."""
    # nb_classes = data.voca_size
    threshold = 0.5
    hop = 10
    model = load_model('Predict/training/model.h5')
    """Load default files."""
    wave, sr = rosa.load('Predict/data/test.wav', mono=True, sr=16000)  # resample to 16k
    """TEST"""
    # wave = np.load('Predict/data/test.npy', allow_pickle=False)
    # sr = 16000

    # get mfcc
    mfcc = rosa.feature.melspectrogram(wave, sr=16000).transpose()
    beg = 0
    end = 80
    labels = {}
    while end < mfcc.shape[0]:
        grain = mfcc[beg:end].copy()
        grain = np.reshape(grain, grain.shape+(1,))
        blah = model.predict(np.array([grain]))
        if(np.max(blah[0]) >= threshold):
            label = data.byte_to_label(np.argmax(blah[0]))
            if label in labels:
                labels[label] = labels[label] + 1
            else:
                labels[label] = 1
        beg = beg+hop
        end = beg+80
    print(labels)
    return labels
