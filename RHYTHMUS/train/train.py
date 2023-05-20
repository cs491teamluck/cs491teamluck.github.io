import numpy
import glob
import pickle
from keras.models import Sequential
from keras.layers import LSTM , Dropout , Dense , Activation , BatchNormalization
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from music21 import note as music21note
from music21 import chord
from music21 import converter as conv
from music21 import instrument as inst

def train():
    # Initializing the necessary variables
    seqLength = 100
    rawNotes = []
    xData = []
    yData = []
    epochNumber = 200
    dropoutRate = 0.3
    modelSize = 512
    batchSize = 128

    # Iterate through the training files to retrieve notes
    for item in glob.glob("trainMusics/*.mid"):
        # Parse the file using converter
        midiFile = conv.parse(item)

        tempNotes = None

        # Try to get only piano notes except take flat notes
        try:
            notesByInst = inst.partitionByInstrument(midiFile)
            # instrumentNotes.parts[0] stores piano notes
            tempNotes = notesByInst.parts[0].recurse() 
        except:
            tempNotes = midiFile.flat.notes

        # Reformat notes and chords
        for element in tempNotes:
            if isinstance(element , chord.Chord):
                tempString = []
                for chordNote in element.normalOrder:
                    tempString.append(str(chordNote))
                rawNotes.append('.'.join(tempString))
            elif isinstance(element , music21note.Note):
                noteVar = str(element.pitch)
                rawNotes.append(noteVar)

    # Backup training notes for later use
    with open('savedNotes/backupNotes', 'wb') as path:
        pickle.dump(rawNotes, path)

    # Sorted set of notes
    notesSet = sorted(set(rawNotes))

    # Number of distinct notes
    numberOfDistinctNotes = len(notesSet)

    # Length of all notes
    notesLength = len(rawNotes)

    # Dictionaries for conversion between numerical nad alphabetical notes
    integerToNote = {}
    for number, note in enumerate(notesSet):
        integerToNote[number] = note

    noteToInteger = {}
    for number, note in enumerate(notesSet):
        noteToInteger[note] = number

    # Extracting input and output sequences for the training
    for i in range(0 , notesLength - seqLength , 1):
        xData.append([noteToInteger[item] for item in rawNotes[i:i + seqLength]])
        yData.append(noteToInteger[rawNotes[i + seqLength]])

    # Reshaping to an acceptable format
    xData = numpy.reshape(xData , (len(xData), seqLength, 1))

    # Normalization of the data
    xData = xData / float(numberOfDistinctNotes)
    yData = np_utils.to_categorical(yData)

    # Data shape variables
    shapeVar1 = xData.shape[1]
    shapeVar2 = xData.shape[2]

    # Model spesifications
    model = Sequential()
    model.add(LSTM(modelSize , recurrent_dropout = dropoutRate , return_sequences = True , input_shape=(shapeVar1 , shapeVar2)))
    model.add(LSTM(modelSize , recurrent_dropout = dropoutRate , return_sequences = True))
    model.add(LSTM(modelSize))
    model.add(BatchNormalization())
    model.add(Dropout(dropoutRate))
    model.add(Dense(modelSize / 2))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(Dropout(dropoutRate))
    model.add(Dense(numberOfDistinctNotes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer = 'rmsprop')

    # Save weights for later use
    checkpoint = ModelCheckpoint("weights.hdf5" , monitor = 'loss' , verbose = 0 , save_best_only = True , mode = 'min')
    callbacksList = [checkpoint]

    # Start the training
    model.fit(xData, yData, epochs = epochNumber, callbacks = callbacksList , batch_size = batchSize)

train()