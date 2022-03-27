import os
import re
from midi2audio import FluidSynth
from pydub import AudioSegment

from numpy import number

"""
createWav takes:
a string name representing the soundbank being used for the conversion.
a string name representing the name of the midi file we wish to use with the soundbank.
a string name representing the name of the outputted .wav file we would like to save the conversion as.
an integer (other than zero). Positive integers will make the .wav louder, while negative integers will make the .wav quieter.

creates 1 .wav file from the midi file inputted using the inputted soundbanks voice
"""

def createWav(midi_in_name, soundfont_name, wav_output_name, db_boost=0):
    test_flag = -1
    if db_boost != 0:   # raise or lower volume
        temp_wav_name = "temp_" + str(wav_output_name)
        FluidSynth(str(soundfont_name)).midi_to_audio(midi_in_name, temp_wav_name)

        volume = int(db_boost)
        song = AudioSegment.from_wav(temp_wav_name)
        if volume > 0:
            volume_song = song + volume
            volume_song.export(str(wav_output_name), format="wav")
            test_flag = 0
        elif volume < 0:
            volume_song = song - abs(volume)
            volume_song.export(str(wav_output_name), format="wav")
            test_flag = 0
        os.remove(temp_wav_name)
    else:   #no alteration in volume
        FluidSynth(str(soundfont_name)).midi_to_audio(midi_in_name, wav_output_name)
        test_flag = 0
    return test_flag

"""
find_deleteable()
deletes all intermediary files created during the overlayWav merging of .wav files
"""
def find_deleteable():
    flag = False
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if re.search("sound.+", f):
            os.remove(f)
            flag = True
    return flag

"""
createWav takes:
a list of strings where each item is a name representing the soundbank being used for the conversion.
a string name representing the name of the midi file we wish to use with the soundbank.
a string name representing the name of the outputted .wav file we would like to save the conversion as.
an integer (other than zero). Positive integers will make the .wav louder, while negative integers will make the .wav quieter.

creates 1 .wav file from the midi file inputted using the inputted soundbanks voice
"""

def overlayWavs(soundfont_list, midi_in_name, wav_output_name, db_boost=0):
    test_flag = 0
    number_of_overlays = len(soundfont_list)
    sounds = []
    createWav(midi_in_name, soundfont_list[0], "sound0.wav", db_boost)
    sound_base = AudioSegment.from_wav("sound0.wav")
    for i in range(1, number_of_overlays):
        createWav(midi_in_name, soundfont_list[i], "sound" + str(i) + ".wav", db_boost)
        sound_added = AudioSegment.from_wav("sound" + str(i) + ".wav")
        sounds.append(sound_added)
    # rename the file into the parameter passed in
    for sound in sounds:
        # sound_base = sound_base.overlay(sound, gain_during_overlay=int(db_boost))
        sound_base = sound_base.overlay(sound)
    # temp_wav_name = "tempcombo_" + str(wav_output_name)
    sound_base.export(wav_output_name, format="wav")

    if find_deleteable() != True:
        print("find deleteables did not delete anything!")
        test_flag = -1
    return test_flag

