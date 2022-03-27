import sys
import midiAngeloConversions

n = len(sys.argv)
if n != 3 :
    print("INVALID INPUT: Three inputs required,", n-1,"provided.\n REQUIRED PARAMITERS: inputFileName PixelArray")
    exit(1)

midiAngeloConversions.image2midi(sys.argv[1],sys.argv[2])