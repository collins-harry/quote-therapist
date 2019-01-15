##############################################################################
#                                                                            #
# EXAMPLE FILE FOR TEAM 05 AT THE AIME HACKATHON                             #
#                                                                            #
##############################################################################

# Please list additional requirements in your requirement.txt file
from flask import Flask, request, Response,Blueprint
import os
import json
import time
import pyaudio
import sys
import pyaudio
import pocketsphinx as ps
from pocketsphinx import get_model_path
import wave
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import io

# Do not rename this:
team05 = Blueprint('team05', __name__)
						
# Write your API routes here:
# (Please use the /api/team05/ prefix for your routes)
script_dir = os.path.dirname(os.path.realpath(__file__))

@team05.route('/api/team05/route01', methods=['POST', 'GET'])
def team05route01():

    """ How to save uploaded photo and read binary contents in variable img: """
    if 'photo' in request.files:
        photo = request.files['photo']
        photo.save(os.path.dirname(os.path.realpath(__file__)) + '/' + 'current_image.png')
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + 'current_image.png', 'rb') as f:
            img = f.read()
			
    try:	
        response = {'status': 'ok', 'message': 'AARDAPPELAARDAPPELAARDAPPELAARDAPPELAARDAPPELAARDAPPEL'}	
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
    except:
        response = {'status': 'failure', 'message': 'Something went wrong'}
        return Response(response=json.dumps(response), status=200, mimetype="application/json")

@team05.route('/api/team05/janschut', methods=['POST', 'GET'])
def janschut():
    print("recording")
    record_audio(6)
    print("finished recording!")
    keywords = []
    usr_ins = stt_google(keywords)
    try:
        response = {'status': 'ok', 'message': '{}'.format(usr_ins)}
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
    except:
        response = {'status': 'failure', 'message': 'Something went wrong'}
        return Response(response=json.dumps(response), status=200, mimetype="application/json")


# modeldir = get_model_path();
# # Create a decoder with certain model
# config = ps.Decoder.default_config()
# config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
# config.set_string('-lm', os.path.join(modeldir, 'en-us.lm.bin'))
# config.set_string('-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
# stream.start_stream()
# # Process audio chunk by chunk. On keyword detected perform action and restart search
# decoder = ps.Decoder(config)
# decoder.set_kws('keyphrase', "keys.kws")
# decoder.set_search('keyphrase')
# decoder.start_utt()

# find_words = ['yes', 'no']

# PORT = 5555

# # route http posts to this method
# @app.route('/api/listen', methods=['POST'])
# def listen():
#     print("Listening...")
#     if "timeout" in request.form:
#         t = time.time() + int(request.form["timeout"]);
#     else:
#         t = time.time() + 10;
    
#     last_word = "";
#     while True:
#         buf = stream.read(1024)
#         if buf:
#             decoder.process_raw(buf, False, False)
#         else:
#             break
#         if decoder.hyp() is not None:
#             print(decoder.hyp().hypstr);
#             for word in find_words:
#                 if word in decoder.hyp().hypstr:
#                     last_word = word
#                     #print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
#                     #print("Detected keyword, restarting search")
#                     decoder.end_utt()
#                     decoder.start_utt()                 
#                     response = {'status': 1, "word": last_word, "time": time.time()}
#                     return Response(response=json.dumps(response), status=200, mimetype="application/json")
        
#         if last_word != "":
#             break;      
        
#         if time.time() > t:
#             response = {'status': 0, 'error': 'timeout', 'timeout': request.form["timeout"], "time": time.time()}
#             return Response(response=json.dumps(response), status=200, mimetype="application/json")
#             break;
        
                    
# def is_port_in_use(port):
#     import socket
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         return s.connect_ex(('localhost', port)) == 0


# if is_port_in_use(PORT):
#     print("Error: port 5555 in use");
#     sys.exit()
# else:
#     # start flask app
#     app.run(host="0.0.0.0", port=PORT)

def record_audio(duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = script_dir + "\\resources\\recording.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    t_start = time.time()
    frames = []
    print("start recording")
    while time.time() - t_start < duration:
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording") 

    stream.stop_stream()
    stream.close() 
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME

def stt_google(keywords):
    # Imports the Google Cloud client library

    #from google.cloud import storage

    start_time = time.time()
    client = speech.SpeechClient()

    # The name of the audio file to transcribe

    file_name = script_dir + "\\resources\\recording.wav"

    #print (file_name)

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code='en-US',
        speech_contexts= [speech.types.SpeechContext(phrases=keywords)],
        )

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    #print (response)

    transcript = ""
    if response:
        for result in response.results:
            transcript = result.alternatives[0].transcript
        #print('Transcript: {}'.format(result.alternatives[0].transcript))

    #print("--- %s seconds ---" % (time.time() - start_time))
    
    return transcript
