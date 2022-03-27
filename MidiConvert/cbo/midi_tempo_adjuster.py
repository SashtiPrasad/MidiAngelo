import sys
import music21
from music21 import *

# this small section of the code handles the TEMPO CHANGE
# we can scale the tempo of the midi using a "factor" float variable
# where anything over 1 is slower (ie 125% speed, fctr =1.25)
# and anything under 1 is faster (75% speed, fctr =0.75)
midi_filename_in = sys.argv[1]
midi_filename_out = sys.argv[2]
fctr = float(sys.argv[3])

# fctr = 0.75 # scale (in this case stretch) the overall tempo by this factor
score = music21.converter.parse(midi_filename_in)
newscore = score.scaleOffsets(fctr).scaleDurations(fctr)
newscore.write('midi',midi_filename_out)