import numpy as np
from random import getrandbits
import librosa
import data
# data path
_training_path='training/preprocess/'
_maximum_splits= 50000
_frames_per_split= 80
_hop=10;
_coeff= 20
_coeff_spectro=128
def load():
    #load mfccs into 3d matrix: samples* frames* features
    #load labels into 1d array
    with open(_training_path+'train.csv') as f:
        lis= [line.split(',') for line in f]
    train_X=np.empty((_maximum_splits,_frames_per_split,_coeff))
    train_Y= np.empty(_maximum_splits)
    mat_count=0
    for line in lis:
        if (line[0]=='\n'):
            continue;
        fmfcc= np.load(_training_path+'mfcc/'+ line[0]+'.npy', allow_pickle=False)
        fmfcc= augment_mfcc(fmfcc).transpose()
        label= int(line[1])
        beg=0
        end=beg+_frames_per_split
        while (end<=fmfcc.shape[0]):
            mfcc_part= fmfcc[beg:end].copy()
            train_X[mat_count]=mfcc_part
            train_Y[mat_count]=label
            mat_count+=1
            beg+= _hop
            end+= _hop
    return train_X[:mat_count].copy(), train_Y[:mat_count].copy()

##########################################################################
############SPECTRO
def load_spectro():
    #load mfccs into 3d matrix: samples* frames* features
    #load labels into 1d array
    with open(_training_path+'train_spectro.csv') as f:
        lis= [line.split(',') for line in f]
    train_X=np.empty((_maximum_splits,_frames_per_split,_coeff_spectro))
    train_Y= np.empty(_maximum_splits)
    mat_count=0
    for line in lis:
        if (line[0]=='\n'):
            continue;
        fmfcc= np.load(_training_path+'spectro/'+ line[0]+'.npy', allow_pickle=False).transpose()
        #fmfcc= augment_mfcc(fmfcc).transpose()
        label= int(line[1])
        beg=0
        end=beg+_frames_per_split
        while (end<=fmfcc.shape[0]):
            mfcc_part= fmfcc[beg:end].copy()
            train_X[mat_count]=mfcc_part
            train_Y[mat_count]=label
            mat_count+=1
            beg+= _hop
            end+= _hop
    return train_X[:mat_count].copy(), train_Y[:mat_count].copy()


def augment_mfcc(mfcc):

    # random frequency shift ( == speed perturbation effect on MFCC )
    r = np.random.randint(-2, 2)

    # shifting mfcc
    mfcc = np.roll(mfcc, r, axis=0)

    # zero padding
    if r > 0:
        mfcc[:r, :] = 0
    elif r < 0:
        mfcc[r:, :] = 0

    return mfcc

def random_onoff():                # randomly turns on or off
    return bool(getrandbits(1))

def augment_data(y, sr, n_augment = 1, allow_speedandpitch = True, allow_pitch = True,
    allow_speed = True, allow_dyn = True, allow_noise = True, allow_timeshift = True, wlabel='', tab=""):

    mods = [y]                  # always returns the original as element zero
    length = y.shape[0]
    if (wlabel=='cryingBaby'):
        print('baby label!!')

    for i in range(n_augment):
        print(tab+"augment_data: ",i+1,"of",n_augment)
        y_mod = y.copy()
        count_changes = 0

        # change speed and pitch together
        if (allow_speedandpitch) and random_onoff() and wlabel!='cryingBaby':
            length_change = np.random.uniform(low=0.9,high=1.1)
            speed_fac = 1.0  / length_change
            print(tab+"    resample length_change = ",length_change)
            tmp = np.interp(np.arange(0,len(y),speed_fac),np.arange(0,len(y)),y)
            #tmp = resample(y,int(length*lengt_fac))    # signal.resample is too slow
            minlen = min( y.shape[0], tmp.shape[0])     # keep same length as original;
            y_mod *= 0                                    # pad with zeros
            y_mod[0:minlen] = tmp[0:minlen]
            count_changes += 1

        # change pitch (w/o speed)
        if (allow_pitch) and random_onoff() and wlabel!='cryingBaby':
            bins_per_octave = 24        # pitch increments are quarter-steps
            pitch_pm = 4                                # +/- this many quarter steps
            pitch_change =  pitch_pm * 2*(np.random.uniform()-0.5)
            print(tab+"    pitch_change = ",pitch_change)
            y_mod = librosa.effects.pitch_shift(y, sr, n_steps=pitch_change, bins_per_octave=bins_per_octave)
            count_changes += 1

        # change speed (w/o pitch),
        if (allow_speed) and random_onoff():
            speed_change = np.random.uniform(low=0.9,high=1.1)
            print(tab+"    speed_change = ",speed_change)
            tmp = librosa.effects.time_stretch(y_mod, speed_change)
            minlen = min( y.shape[0], tmp.shape[0])        # keep same length as original;
            y_mod *= 0                                    # pad with zeros
            y_mod[0:minlen] = tmp[0:minlen]
            count_changes += 1

        # change dynamic range
        if (allow_dyn) and random_onoff():
            dyn_change = np.random.uniform(low=0.5,high=1.1)  # change amplitude
            print(tab+"    dyn_change = ",dyn_change)
            y_mod = y_mod * dyn_change
            count_changes += 1

        # add noise
        if (allow_noise) and random_onoff():
            noise_amp = 0.005*np.random.uniform()*np.amax(y)
            if random_onoff():
                print(tab+"    gaussian noise_amp = ",noise_amp)
                y_mod +=  noise_amp * np.random.normal(size=length)
            else:
                print(tab+"    uniform noise_amp = ",noise_amp)
                y_mod +=  noise_amp * np.random.normal(size=length)
            count_changes += 1

        # shift in time forwards or backwards
        if (allow_timeshift) and random_onoff():
            timeshift_fac = 0.2 *2*(np.random.uniform()-0.5)  # up to 20% of length
            print(tab+"    timeshift_fac = ",timeshift_fac)
            start = int(length * timeshift_fac)
            if (start > 0):
                y_mod = np.pad(y_mod,(start,0),mode='constant')[0:y_mod.shape[0]]
            else:
                y_mod = np.pad(y_mod,(0,-start),mode='constant')[0:y_mod.shape[0]]
            count_changes += 1
        #final check for duplication
        if (np.array_equal(y, y_mod)):
            return augment_data(y,sr, wlabel=wlabel)
        return y_mod


def generate_one_hot(y, lnum):
    #y= input array, lnum= number of labels
    Y= np.zeros((y.size, lnum))
    for i in range(y.size):
        Y[i][int(y[i])]=1.0
    return Y
def truncate_silence(y, fsize=5096, hop=1/4):
    beg=0
    end=beg+fsize
    out= np.zeros(y.size)
    presil=False
    outcursor=0
    while (end<y.size):
        grain=y[beg:end]*np.hanning(fsize)
        if (np.max(grain)<0.05):
            if (presil==False): #attach silence
                outcursor+=fsize*2
                presil=True;
        else:
            out[outcursor:outcursor+fsize]+=grain
            outcursor+=hop*fsize;
            presil=False;
        beg=beg+hop*fsize
        end=beg+fsize
    return out
def STFT(y, frame_size=512, window=None, hop=1/4):
    #generate window
    if (window==None):
        window= np.hanning(frame_size)
    #calculate fft
    beg=0
    end= beg+frame_size
    fftmat= np.empty((_maximum_splits, frame_size//2+1))
    fcount=0
    while (end<= y.size):
        grain= y[beg:end]* window
        rfft= np.fft.rfft(grain)
        fftmat[fcount]=rfft
        fcount+=1
        beg+=frame_size*hop
        end+=frame_size*hop
    return fftmat[:fcount]
def invert_STFT(fftmat, frame_size=512):
    #generate default window
    window=np.hanning(frame_size)
    for i in range(fftmat.size):
        grain= np.fft.irfft(fftmat[i])

        #re-regenerate window
        if (grain.size!= window.size):
            window= np.hanning(grain.size)
            frame_size= grain.size
