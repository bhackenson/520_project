import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import confusion_matrix
import seaborn as sns
from music21 import *
import pandas as pd
import matplotlib.pyplot as plt
import re

def plot_hist(hist, output='hist.png'):
    plt.plot(hist.history['loss'], label='Training Loss')
    plt.plot(hist.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.savefig(output)

def print_accuracy(y_pred, y_test):
    accuracy = np.mean(np.all(y_pred == y_test, axis=1))
    print(f"accuracy: {accuracy:.2%}")

def plot_conf_matrix(y_pred, y_test):
    conf_matrix = confusion_matrix(y_pred, y_test)
    sns.heatmap(conf_matrix, annot=True, cmap="Blues")
    plt.title('Chord Prediction Confusion Matrix')
    plt.xlabel('Pred')
    plt.ylabel('Actual')
    plt.savefig('confusion_matrix.png')

def get_roman_numerals():
    # C major (no vii-dim)
    I = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]) # Cmaj
    ii = np.array([0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]) # Dmin
    iii = np.array([0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]) # Emin
    IV = np.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]) #Fmaj
    V = np.array([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]) #Gmaj
    vi = np.array([1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]) #Amin
    # C minor (no ii-dim)
    i = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]) # Cmin
    III = np.array([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]) # Ebmaj
    iv = np.array([1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]) # Fmin
    v = np.array([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]) # Gmin
    VI = np.array([1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]) # Abmaj
    VII = np.array([0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]) # Bbmaj
    return {
        # major
        "I": I,
        "ii": ii,
        "iii": iii,
        "IV": IV,
        "V": V,
        "vi": vi,

        # minor
        "i": i,
        "III": III,
        "iv": iv,
        "v": v,
        "VI": VI,
        "VII": VII
    }

def build_model(m):
    if (m != 'major' and m != 'minor'):
        raise Exception("input string m is not equal to 'major' or 'minor'.")
    df = pd.read_csv("server\dataset.csv") # pop chord progressions from https://github.com/ology/Data-Dataset-ChordProgressions/blob/master/share/Chord-Progressions.csv?plain=1
    matrix = df.values
    progressions = []
    for entry in matrix:
        if (entry[1] == m):
            p = re.split('[-]', entry[4])
            progressions.append([get_roman_numerals()[i] for i in p])

    prog_train, prog_test = np.split(progressions, [54], axis=0)

    X = []
    y = []
    X_t = []
    y_t = []

    for prog in prog_train:
        X.append(prog[:3])  # First 3 chords as input
        y.append(prog[1:])  # Last 3 chords as target
    X = np.array(X)
    y = np.array(y)

    print("X shape:", X.shape)  # Expected: (num_sequences, 3, 12)
    print("y shape:", y.shape)  # Expected: (num_sequences, 3, 12)

    for prog in prog_test:
        X_t.append(prog[:3])  # First 3 chords as input
        y_t.append(prog[1:])  # Last 3 chords as target
    X_t = np.array(X_t)
    y_t = np.array(y_t)

    print("X_t shape:", X_t.shape)
    print("y_t shape:", y_t.shape)

    # Define the model
    model = Sequential()
    model.add(LSTM(128, input_shape=(3, 12), return_sequences=True))
    model.add(Dense(12, activation='sigmoid'))
    # model.add(Dropout(0.2))

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam')
    history = model.fit(X, y, epochs=150, validation_data=(X_t, y_t), batch_size=32)

    return model, m, history, X, y, X_t, y_t

def apply_threshold(predictions, threshold=0.5):
    return (predictions > threshold).astype(int)

"""Evaluation"""
# History
# plot_hist(history)

# Accuracy
model, tone, history, X_train, y_train, X_test, y_test = build_model('major')
X_test_chord = X_test[:,:2,:]
y_test_chord = y_test[:,2,:]
y_pred = [apply_threshold(model.predict(np.array([c]))[0])[0] for c in X_test_chord]
# print_accuracy(y_pred, y_test_chord)

# Confusion Matrix
v = list(get_roman_numerals().values())
classes_pred = []
classes_test = []
for pred in y_pred:
    pred_idx = next((index for index, arr in enumerate(v) if np.array_equal(arr, pred)), 0)
    classes_pred.append(pred_idx)
for tst in y_test_chord:
    test_idx = next((index for index, arr in enumerate(v) if np.array_equal(arr, tst)), 0)
    classes_test.append(test_idx)
# plot_conf_matrix(classes_pred, classes_test)