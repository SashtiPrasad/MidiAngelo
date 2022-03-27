from itertools import groupby
from unittest import skip

import pygame
from PIL import Image
from midiutil import MIDIFile
import random as rand
import os

# helper functions for conversions

def lerp(min, max, note):
  return int(min + note * (max - min))


def convert_rgb_to_note(r, g, b):
  return lerp(21, 108, int((r+g+b)/6.0)/255.0)


def add_note(song, track, pitch, time, duration):
  song.addNote(track, 0, pitch, time, duration, 100)


def create_midi(tempo, data):
  song = MIDIFile(1)
  song.addTempo(0, 0, tempo)

  grouped = [(note, sum(1 for i in g)) for note, g in groupby(data)]
  time = 0
  for note, duration in grouped:
    add_note(song, 0, note, time, duration)
    time += duration
  return song


def play_midi(music_file):
  clock = pygame.time.Clock()
  try:
    pygame.mixer.music.load(music_file)
    print("Music file %s loaded. Press Ctrl + C to stop playback." % music_file)
  except Exception as e:
    print("Error loading file: %s - %s" % (music_file, e))
    return
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30)


def get_song_data(filename):
  try:
    im = Image.open(filename).convert('RGB')
  except Exception as e:
    print("Error loading image: %s" % e)
    raise SystemExit
  print("Img %s loaded." % filename)
  w, h = im.size
  return [convert_rgb_to_note(*im.getpixel((x, y))) for y in range(h) for x in range(w)]


def convert(img_file, midi_file, play):
  pygame.init()
  data = get_song_data(img_file)
  song = create_midi(240, data)

  with open(midi_file, 'wb') as f:
    song.writeFile(f)

  if play:
    try:
      play_midi(midi_file)
    except KeyboardInterrupt:
      pygame.mixer.music.fadeout(1000)
      pygame.mixer.music.stop()
      raise SystemExit
  return True

"""
unpacks data string into an array/grid of pixel values, returns a NxM nested list
"""
def unpackDataString(str):
    str = str.replace("\n","\\n")
    str = str.split("\\n")
    del str[-1]
    result = []
    for row in str:
        row = row.replace("(","")
        row = row.replace(")","")
        row = row.split(" ")
        del row[-1]
        newrow = []
        for pixel in row:
            pixel = pixel.split(",")
            for i in range(0, len(pixel)):
              pixel[i] = int(pixel[i])
            newrow.append(pixel)
        result.append(newrow)
    return result

def checkDataStringValidity(dataString):
    dataStringResult = unpackDataString(dataString)

    N = len(dataStringResult)
    M = len(dataStringResult[0])

    # checks if the pixel array's values are the right data type and are within the correct interval
    rowSum = 0
    for row in dataStringResult:
        rowsPixelSum = 0
        for pixel in row:
            for pixelValue in pixel:
                if not(pixelValue>= 0 and pixelValue<= 255):
                    return "Contains pixel Values outside of range [0,255]"
            rowsPixelSum += 1
        rowSum += 1

    if (rowSum != N) or (rowsPixelSum != M):
        return "Data string Provided yeilded improper diamentions"

    return True


def generateRandomDatastring():
    N = rand.randint(2,128)
    M = rand.randint(2,128)
    result = ""

    for i in range(N):

        for j in range(M):
            r = rand.randint(0,255)
            g = rand.randint(0,255)
            b = rand.randint(0, 255)
            result += "(" + str(r) + "," + str(g) + "," + str(b) + ")"
            if j!= M-1:
                result+= " "
        result += "\n"

    return(result)


# End of Helper Functions, The last three are funtions you would wnat to call upon

"""
Converts a nested list of pixel RGB values into an image
@:param outputFileName -> name of the image file that will be exported. it will be saved in the woring directoru 
@:param P -> A NxM nested list of pixel values 
    example: [[[r,g,b],[r,g,b]],[r,g,b],[r,g,b]] would represent a 2x2 image
@param scale -> the magnification factor of the generated image. its main purpose
    is for exporting images for the user to look at
@param show -> false by default. displays the image after generation, not recomended outside of testing
"""
def canvas2image(outputFileName, dataString, scale, show=False):

    P = unpackDataString(dataString)
    N = len(P)
    M = len(P[0])

    img = Image.new('RGB', (N, M), color=0)
    pixels = img.load()

    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            newPix = P[i][j]
            pixels[i, j] = (newPix[0], newPix[1], newPix[2])

    intscale = (int)(scale)

    img = img.resize((img.size[0]*intscale,img.size[1]*intscale),Image.NEAREST)

    if show == True:
        img.show()

    img.save(outputFileName + "x"+(str)(scale)+".PNG")
    img.close()


"""
Converts a image into a midi file
@:param inputFileName -> name/path of the image file to be converted
@:param outputFileName -> the name of the midi file being generated. it will be saved in the working directory
@:param playback -> false by default. Played the midi file after conversion. not recomended outside of testing
"""
def image2midi(inputFileName,outputFileName,playback=False):
    convert(inputFileName,outputFileName,playback)


""" 
Converts a nested list of pixel RGB values into a midi file
@:param outputFileName -> the name of the midi file being generated. it will be saved in the working directory
@:param dataString -> a string containg the exported data from  canvas
@param show -> false by default. displays the image after generation, not recomended outside of testing
@:param playback -> false by default. Played the midi file after conversion. not recomended outside of testing
"""
def canvas2midi(outputFileName, dataString, show=False, playback=False):
    canvas2image(outputFileName +"-canvas2midiTEMP", dataString, 1, show)
    return convert(outputFileName+"-canvas2midiTEMPx1.PNG",outputFileName+".midi",playback)

"""
Test Driver for this file for the generation of images from canvas.
Since the generation of .midi from image is done with an external 
library I used I decided not to test it
These tests can also be found in views.py under the testsuite function
"""
def runTestSuite():
    test_results = {
        'pass': ['Server Health: Strong', 'The testing suite has been reached.'],
        'fail': []
    }

    # Testing reliability of data string unpacker
    numOfTests = 100
    for testNum in range(1,numOfTests+1):
        result = checkDataStringValidity(generateRandomDatastring())
        if result == True:
            test_results['pass'].append("Random Datastring Generation " + str(testNum) + "/" + str(numOfTests) + " passed")
        else:
            test_results['fail'].append("Random Datastring Generation " + str(testNum) + "/" + str(numOfTests) + " Reason:"+result)

    # Testing Random generation of Images from randomly generated
    numofRandTests = 100
    show = False
    for testNum in range(1,numofRandTests+1):
        try:
            randomDataString = generateRandomDatastring()
            canvas2image(("test#"+str(testNum)),randomDataString,1,show)
            os.remove("test#"+str(testNum)+"x1.PNG")
        except RuntimeError:
            test_results['fail'].append("Random Image Generation " + str(testNum) + "/" + str(numofRandTests) + " had a RuntimeError")
            raise
        test_results['pass'].append("Random Image Generation "+str(testNum)+"/"+str(numofRandTests)+" passed")

