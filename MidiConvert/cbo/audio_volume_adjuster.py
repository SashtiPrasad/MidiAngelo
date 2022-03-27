import sys
from pydub import AudioSegment

audio_in = "output_audio.wav"
audio_out = "louder_output_audio.wav"
volume = 20
#SMALL VOLUME SECTION
#SOME WE CAN EITHER USE THIS FOR VOLUME OR TO JUST GENERALLY MAKE THE .WAVS LOUDER
song = AudioSegment.from_wav(audio_in)
# add 25 Db to the Wav
# i know the absolute value thing looks dumb but it works for now, for some reason i was having issues adding a negative number
if volume > 0:
    volume_song = song + volume
elif volume < 0:
    volume_song = song - abs(volume)

volume_song.export(audio_out, format="wav")
# since I am unsure how the HTML will be implemented, or what the base audio codecs are, we can use .wavs if needed but .flacs will be much smaller

# if they want to hear it, you'll have to open it from the workspace folder. 
# I assume that we would essentially have the file on the server and then have the webpage point to the audio file