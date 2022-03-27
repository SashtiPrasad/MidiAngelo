import os
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import midiAngeloConversions
from . import midi_to_audio_conversion
from django.conf import settings
import base64
import glob
from django.test import Client

from .midiAngeloConversions import checkDataStringValidity, generateRandomDatastring, canvas2image


#libraries for password hashing
import uuid
import hashlib
 

#Render the landing page
def home(request):
	return render(request, 'index.html')

#Render the admin testing page
def test(request):
	return render(request, "test.html")

#Convert an image in the request
@csrf_exempt
def image(request):
	data = json.loads(request.body)
	if not data:
		return HttpResponseBadRequest("There was no data provided to handle then request.")

	midi_string = '' # image string to make into midi
	if 'img_string' in data and isinstance(data['img_string'],str):
		midi_string = str(data['img_string'])
	else:
		return HttpResponseBadRequest("No Image was provided or it was in an improper format.")

	sounds = getSoundFontsList(data["soundfonts"]) #soundfont to use for conversion
	if len(sounds)==0:
		return HttpResponseBadRequest("No Sounds were provided or they could not be formatted by the server.")

	db_boost = 0
	if 'db_boost' in data and isinstance(data['db_boost'], int):
		db_boost = int(data['db_boost'])

	midi_file_success = midiAngeloConversions.canvas2midi('output_midi', midi_string)
	if not midi_file_success:
		response = HttpResponseBadRequest("The Image failed be converted to MIDI")
	
	try:
		midi_to_audio_conversion.overlayWavs(sounds, "output_midi.midi", 'output_audio.wav', db_boost)
	except:
		RuntimeError
		return HttpResponseBadRequest("Failed to create the song from selected sounds.")

	try:
		fname = settings.BASE_DIR/"output_audio.wav"
	except:
		RuntimeError
		return HttpResponseBadRequest("The finalized audio file could not be found .")

	with open(fname,"rb") as f: audio_encoded = base64.b64encode(f.read())
	#convert audio file to JSON
	response = HttpResponse(audio_encoded, content_type='application/json')

	return response

#Render the login page
def login(request):
	return render(request, 'login.html')

#Render the drawing canvas page
def canvas(request):
	return render(request, 'midiCanvas.html')

#Render the user signup page
def signup(request):
	return render(request, 'login.html')	

#Input: an HttpRequest
#Return: a list of soundfonts by their file location
def getSoundFonts(request):

	soundfont_names = []
	soundfont_names = glob.glob("/app/cbo/soundfonts/*.sf2")
	for s in range(len(soundfont_names)):
		soundfont_names[s] = soundfont_names[s][20:-4]
	return HttpResponse(json.dumps(soundfont_names), content_type='application/json')

#Input: a list of strings with no file extensions
#Return: a list of strings that relate to the filepaths
def getSoundFontsList(soundfonts):
	formatted_soundfonts = []
	for i in range(len(soundfonts)):
		formatted_soundfonts.append("/app/cbo/soundfonts/"+soundfonts[i]+".sf2")
	
	return formatted_soundfonts

#Run all of our tests and return a report
@csrf_exempt
def runTestingSuite(request):
	tester = Client()
	test_results = {
		'pass':['Server Health: Strong', 'The testing suite has been reached.'], 
		'fail':[]
	}
	# Test 1
	if midi_to_audio_conversion.createWav(settings.BASE_DIR/'cbo/filein.mid', settings.BASE_DIR/'cbo/soundfonts/Early Ens.sf2', 'melody_loud.wav', 20) == 0:
		test_results['pass'].append("Test 1: decibel conversion output - positive value pass")
	else:
		test_results['fail'].append("Test 1: Error decibel conversion output - not turning up volume")

	# Test 2
	if midi_to_audio_conversion.createWav(settings.BASE_DIR/'cbo/filein.mid', settings.BASE_DIR/'cbo/soundfonts/Early Ens.sf2', 'melody_quiet.wav', -20) == 0:
		test_results['pass'].append("Test 2: decibel conversion output - negative value pass")
	else:
		test_results['fail'].append("Test 2: Error decibel conversion output - not turning down volume")

	# Test 3
	if midi_to_audio_conversion.createWav(settings.BASE_DIR/'cbo/filein.mid', settings.BASE_DIR/'cbo/soundfonts/Early Ens.sf2', 'melody_normal.wav') == 0:
		test_results['pass'].append("Test 3: basic conversion - no decibel alteration pass")
	else:
		test_results['fail'].append("Test 3: Error in basic conversion - no decibel alteration")

	# TEST SECTION 2: OVERLAYWAV
	sound_list = [settings.BASE_DIR/'cbo/soundfonts/Early Ens.sf2', settings.BASE_DIR/'cbo/soundfonts/Piano.sf2',
				  settings.BASE_DIR/'cbo/soundfonts/Sax Section.sf2', settings.BASE_DIR/'cbo/soundfonts/Celesta.sf2']

	# Test 4
	if midi_to_audio_conversion.overlayWavs(sound_list, settings.BASE_DIR/'cbo/filein.mid', 'combo_normal.wav') == 0:
		test_results['pass'].append("Test 4: basic conversion - overlayWav works - no added Db")
	else:
		test_results['fail'].append(
			"Test 4: Error in basic conversion - overlayWav does not work - no added db - perhaps file path error?")

	# Test 5
	if midi_to_audio_conversion.overlayWavs(sound_list, settings.BASE_DIR/'cbo/filein.mid', 'combo_loud.wav',20) == 0:
		test_results['pass'].append("Test 5: basic conversion - overlayWav works - higher Db")
	else:
		test_results['fail'].append(
			"Test 5: Error in basic conversion - overlayWav does not work - higher db - perhaps file path error?")

	# Test 6
	if midi_to_audio_conversion.overlayWavs(sound_list, settings.BASE_DIR/'cbo/filein.mid', 'combo_quiet.wav',-20) == 0:
		test_results['pass'].append("Test 6: basic conversion - overlayWav works - lowered Db")
	else:
		test_results['fail'].append(
			"Test 6: Error in basic conversion - overlayWav does not work - lowered db - perhaps file path error?")

	#Test getSoundFonts(tester):	

	# Testing reliability of data string unpacker
	numOfTests = 100
	for testNum in range(1, numOfTests + 1):
		result = checkDataStringValidity(generateRandomDatastring())
		if result == True:
			test_results['pass'].append(
				"Random Datastring Generation " + str(testNum) + "/" + str(numOfTests) + " passed")
		else:
			test_results['fail'].append(
				"Random Datastring Generation " + str(testNum) + "/" + str(numOfTests) + " Reason:" + result)

	# Testing Random generation of Images from randomly generated
	numofRandTests = 100
	show = False
	for testNum in range(1, numofRandTests + 1):
		try:
			randomDataString = generateRandomDatastring()
			canvas2image(("test#" + str(testNum)), randomDataString, 1, show)
			os.remove("test#" + str(testNum) + "x1.PNG")
		except RuntimeError:
			test_results['fail'].append(
				"Random Image Generation " + str(testNum) + "/" + str(numofRandTests) + " had a RuntimeError")
			raise
		test_results['pass'].append("Random Image Generation " + str(testNum) + "/" + str(numofRandTests) + " passed")

	

	return HttpResponse(json.dumps(test_results), content_type='application/json')

@csrf_exempt
def validateUser(request):
	
	data = json.loads(request.body)
	password = data['password']
	username = data['username']


	#load the database
	f = open(settings.BASE_DIR/'cbo/database.json', 'r')
	db = json.loads(f.read())
	f.close()

	result = {
		'code':200,
		'message':'Successful Login'
	}

	#check for valid username
	if not isinstance(username, str) or len(username) > 20:
		result['code'] = 500
		result['message'] = "The username is not valid"
		return HttpResponse(json.dumps(result), content_type='application/json')
	#check if the username exists
	if username not in db['users'].keys():
		result['code'] = 500
		result['message'] = "The user does not exist"
		return HttpResponse(json.dumps(result), content_type='application/json')

	user = db['users'][username]

	if check_password(user['password'], password):

		result['payload'] = user
		result['payload'].pop("password")
		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result['code'] = 500
		result['message'] = "Incorrect Password"
		return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt	
def createUser(request):
	data = json.loads(request.body)
	password = data['password']
	username = data['username']
	email = data['email']

	#load the database as a readable file
	f = open(settings.BASE_DIR/'cbo/database.json', 'r')
	db = json.load(f)
	f.close()

	result = {
		'code':200,
		'message':'Account Created'
	}

	if not isinstance(username, str) or len(username) > 20:
		result['code'] = 500
		result['message'] = "The username is not valid"
		return HttpResponse(json.dumps(result), content_type='application/json')
	#check if the username exists
	if username in db['users'].keys():
		result['code'] = 500
		result['message'] = "The user already exists"
		return HttpResponse(json.dumps(result), content_type='application/json')

	hashed_password = hash_password(str(password))
	db['users'][username] = {'username':username, 'password':hashed_password, 'email':email}

	#open database as a writeable file
	f = open(settings.BASE_DIR/'cbo/database.json', 'w')
	json.dump(db, f)

	return HttpResponse(json.dumps(result), content_type='application/json')

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
 
	