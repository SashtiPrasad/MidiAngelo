FROM python:3.7

RUN python3 -m pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y fluidsynth

COPY ./requirements.txt /workspace/

RUN python3 -m pip install -r /workspace/requirements.txt

CMD ["python3", "midiConverter_full.py", "midiAngeloConversions.py", "midi_tempo_adjuster.py", "audio_volume_adjuster.py", "midi_to_audio_conversion.py", "canvas2image.py", "canvas2midi.py", "image2midi.py"]