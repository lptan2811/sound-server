from __future__ import print_function
import numpy as np
import librosa as rosa

from keras.optimizers import SGD
np.random.seed(1337)
from keras.utils import np_utils
from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
import utils
import data

'exception_verbosity = high'
nb_classes = data.voca_size
threshold=0.5
#threshold=0.8
hop=10

model= load_model('training/model.h5')

#wave,sr= rosa.load('data/tel/20150227_194718-telcasa-18.wav', mono=True, sr=16000) #resample to 16k
wave,sr= rosa.load('data/test.wav', mono=True, sr=16000) #resample to 16k

#get mfcc
mfcc= rosa.feature.melspectrogram(wave, sr=16000).transpose()
beg=0
end=80
res=np.empty(0)
while end <mfcc.shape[0]:
    grain= mfcc[beg:end].copy()
    grain=np.reshape(grain,grain.shape+(1,))
    blah= model.predict(np.array([grain]))
    #if (np.max(blah[0])>=threshold):
        #res=np.append(res,np.argmax(blah[0]))
    if(np.max(blah[0])>=threshold):
        print(data.byte_to_label(np.argmax(blah[0])))
    beg=beg+hop
    end=beg+80
counts = np.bincount(res.astype(int))

#print (data.byte_to_label(np.argmax(counts)))
