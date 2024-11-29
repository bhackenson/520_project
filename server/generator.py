import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from music21 import *
import pandas as pd
import matplotlib.pyplot as plt
import re
import random

def plot_hist(hist, output='hist.png'):
    plt.plot(hist.history['loss'], label='Training Loss')
    plt.plot(hist.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.savefig(output)

def chord_to_vector(chord):
    note_to_index = {
        'C': 0, 'B#': 0,
        'C#': 1, 'D-': 1,
        'D': 2,
        'D#': 3, 'E-': 3,
        'E': 4, 'F-': 4,
        'F': 5, 'E#': 5,
        'F#': 6, 'G-': 6,
        'G': 7,
        'G#': 8, 'A-': 8,
        'A': 9,
        'A#': 10, 'B-': 10,
        'B': 11, 'C-': 11
    }
    pitch_arr = []
    ret = [0 for _ in range(12)]
    for p in chord.pitches:
        if str(p)[1:2] not in "1234567890":
            pitch_arr.append(str(p)[0:2])
        else:
            pitch_arr.append(str(p)[0:1])
    for pitch in pitch_arr:
        ret[note_to_index[pitch]] = 1

    return ret

def pitch_to_vector(pitch):
    note_to_index = {
        'C': 0, 'B#': 0,
        'C#': 1, 'D-': 1,
        'D': 2,
        'D#': 3, 'E-': 3,
        'E': 4, 'F-': 4,
        'F': 5, 'E#': 5,
        'F#': 6, 'G-': 6,
        'G': 7,
        'G#': 8, 'A-': 8,
        'A': 9,
        'A#': 10, 'B-': 10,
        'B': 11, 'C-': 11
    }
    pitch_arr = []
    ret = [0 for _ in range(12)]
    if str(pitch)[1:2] not in "1234567890":
        pitch_arr.append(str(pitch)[0:2])
    else:
        pitch_arr.append(str(pitch)[0:1])
    for p in pitch_arr:
        ret[note_to_index[p]] = 1

    return ret

def vector_to_chord(vector):
    pitch_classes = []

    for i, val in enumerate(vector):
        if val == 1:
            pitch_classes.append(i)

    c = chord.Chord([note.Note(pitch) for pitch in pitch_classes])
    return c

# original key is C major or C minor
def transpose_chord(original_chord, m, target_key_name):
    if (m != 'major' and m != 'minor'):
        raise Exception("input string m is not equal to 'major' or 'minor'.")
    # key names (strings): 'CM' = C major; 'Cm' = C minor; 'F#M' = F# major; 'B-m' = Bb minor; etc
    original_key = key.Key('CM') if m == 'major' else key.Key('Cm')
    target_key = key.Key(target_key_name)

    transposition_interval = interval.Interval(original_key.tonic, target_key.tonic)
    transposed_chord = original_chord.transpose(transposition_interval)
    
    return transposed_chord

def show_roman_numeral(chord, key_sig):
    return roman.romanNumeralFromChord(chord, key.Key(key_sig))
    
def chord_to_melody(chord):
    melody = [p for p in chord.pitches]
    if ((len(chord.pitches)) < 4):
        extra_notes = [p.transpose(12) for p in chord.pitches[:(4-(len(chord.pitches)))]] # pad melody so each chord has a 4-note melody (arpeggio)
        melody += extra_notes
    return melody

def show_melody_notes(chord):
    melody = [p for p in chord.pitchNames]
    if ((len(chord.pitches)) < 4):
        extra_notes = [j.name for j in [p.transpose(12) for p in chord.pitches[:(4-(len(chord.pitches)))]]] # pad melody so each chord has a 4-note melody (arpeggio)
        melody += extra_notes
    return melody

def show_chord_name(chord):
    flat_symbol = '\u266D'
    sharp_symbol = '\u266F'
    return {"chord": f'{str(chord.root().name).replace("-", flat_symbol).replace("#", sharp_symbol)} {chord.commonName}', "notes": [str(chord.root().name).replace("-", "b") + '3'] + [str(p).replace("-", "b") + '4' for p in chord.pitches]}

def create_midi_file(chords, melody, key_sig, time_sig='4/4', m_tempo=120, path="output.mid"):
    score = stream.Score()
    part = stream.Part()
    mel = stream.Part()
    score.append(mel)
    score.append(part)

    for m in melody:
        if time_sig == '3/4':
            for i in range(len(m)-1):
                n = note.Note(m[i])
                n.duration = duration.Duration('quarter')
                mel.append(n)
        elif time_sig == '4/4':
            for p in m:
                n = note.Note(p)
                n.duration = duration.Duration('eighth')
                mel.append(n)
        elif time_sig == '6/8':
            for i in range(len(m)-1):
                n = note.Note(m[i])
                n.duration = duration.Duration('eighth')
                mel.append(n)
    
    for c in chords:
        root_note = c.root()
        # root_note.octave -= 1 # bass note
        c.add(root_note)
        c.transpose(-12, inPlace=True)
        if time_sig == '3/4':
            c.duration.quarterLength = 3
        elif time_sig == '4/4':
            c.duration = duration.Duration('half')
        elif time_sig == '6/8':
            c.duration.quarterLength = 1.5
        part.append(c)
        """
        rn = roman.romanNumeralFromChord(c, key.Key(key_sig))
        rn.duration = c.duration
        part.append(rn)
        """

    part.timeSignature = meter.TimeSignature(time_sig)

    ks = key.KeySignature(key.Key(key_sig).sharps)
    part.insert(0, ks)

    new_tempo = tempo.MetronomeMark(number=m_tempo)
    part.insert(0, new_tempo)

    mf = midi.translate.music21ObjectToMidiFile(score)
    mf.open(path, 'wb')
    mf.write()
    mf.close()
    return

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
    df = pd.read_csv("dataset.csv") # pop chord progressions from https://github.com/ology/Data-Dataset-ChordProgressions/blob/master/share/Chord-Progressions.csv?plain=1
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
        X.append(prog[:3])  # First 7 chords as input
        y.append(prog[1:])  # Last 7 chords as target
    X = np.array(X)
    y = np.array(y)

    print("X shape:", X.shape)  # Expected: (num_sequences, 3, 12)
    print("y shape:", y.shape)  # Expected: (num_sequences, 3, 12)

    for prog in prog_test:
        X_t.append(prog[:3])  # First 3 chords as input
        y_t.append(prog[1:])  # Last 3 chords as target
    X_t = np.array(X_t)
    y_t = np.array(y_t)

    # Define the model
    model = Sequential()
    model.add(LSTM(128, input_shape=(3, 12), return_sequences=True))
    model.add(Dense(12, activation='sigmoid'))
    # model.add(Dropout(0.2))

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam')
    history = model.fit(X, y, epochs=150, validation_data=(X_t, y_t), batch_size=32)

    return model, m, history

def apply_threshold(predictions, threshold=0.5):
    return (predictions > threshold).astype(int)

# Generating a new chord progression
def generate_chord_progression(model, seed_chord, length):
    chord_progression = [seed_chord]
    current_chord = seed_chord
    chord_strings = [vector_to_chord(seed_chord[0])]

    for _ in range(length - 1):
        next_chord = model.predict(np.array([current_chord]))[0]
        next_chord = apply_threshold(next_chord, threshold=0.45)

        # limit to 4 notes in a chord
        ones_count = 0
        for i in range(len(next_chord)):
            if next_chord[0][i] == 1 and ones_count < 4:
                ones_count += 1
            else:
                next_chord[0][i] = 0

        chord_progression.append(next_chord)
        chord_strings.append(vector_to_chord(next_chord[0]))
        current_chord = next_chord

    return np.array(chord_progression), chord_strings

# randomize seed chord
def randomize_seed(m):
    if (m == 'major'):
        major_numerals = list(get_roman_numerals().items())[:6]
        seed_chord = random.choice(major_numerals)
        return np.array([seed_chord[1]])
    elif (m == 'minor'):
        minor_numerals = list(get_roman_numerals().items())[6:]
        seed_chord = random.choice(minor_numerals)
        return np.array([seed_chord[1]])
    else:
        raise Exception("input string m is not equal to 'major' or 'minor'.")

# generate progression, plot history, create MIDI file
# model, tone, history = build_model('minor')
# new_progression, chord_strings = generate_chord_progression(model, randomize_seed(tone), 4)
# flattened_list = [item for sublist in new_progression for item in sublist]
# print(flattened_list)
# print(chord_strings)
# plot_hist(history)
# print([transpose_chord(c, tone, 'B-m') for c in chord_strings])
# print([[pitch_to_vector(p) for p in chord_to_mel(t)] for t in [transpose_chord(c, tone, 'B-m') for c in chord_strings]])
# print([show_melody_notes(t) for t in [transpose_chord(c, tone, "Am") for c in chord_strings]])
# transposed_chords = [transpose_chord(c, tone, 'Dm') for c in chord_strings]
# transposed_melody = [chord_to_melody(t) for t in transposed_chords]
# create_midi_file(chords=transposed_chords,melody=transposed_melody,key_sig='Dm',time_sig='6/8',m_tempo=120)