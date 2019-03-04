import librosa
import IPython.display as ipd
import math
import numpy


def get_beat_data(raw_music, sr):

    ipd.Audio(raw_music, rate=sr)
    tempo, beat_times = librosa.beat.beat_track(raw_music, sr=sr, start_bpm=60, units='time')
    return tempo, beat_times.tolist()

def calc_speed_intervals(length):
    speed_interval = math.floor(length/7*100) / 100
    speed_changes = []
    time = 0
    new_time = 1

    while time < length:
        new_time = time + speed_interval
        if new_time < length:
            speed_changes.append(new_time)
        time = new_time
    
    return speed_changes

def get_bpm_intervals(bpm, length):
    beat_interval = ((60/bpm) * 100 / 100) / 2
    beats = length/beat_interval
    beat_times = [0]
    time = 0
    new_time = 1

    while time < length:
        new_time = time + beat_interval
        if new_time < length:
            beat_times.append(new_time)
        time = new_time
    
    return beat_times

def generate_timeline(song):

    raw_music, sr = librosa.load(song)
    bpm, onsets = get_beat_data(raw_music, sr)
    length = math.ceil(onsets[-1] )

    num_events = 10 * length
    timeline = []
    
    #color = get_color(song)
    color = (255,255,255)
    curr_onset = onsets[0]

    speed = 6
    speed_intervals = calc_speed_intervals(length)
    beat_intervals = get_bpm_intervals(bpm, length)
    beat_size = 35
    onset_size = 25
    
    for x in range(1, num_events):

        time = (x * 100) / 1000

        if time > len(speed_intervals) > 0 and speed_intervals[0]:
            speed += 1
            speed_intervals.pop(0)
        if len(beat_intervals) > 0 and time > beat_intervals[0]:
            event = (speed, color, beat_size)
            timeline.append(event)
            beat_intervals.pop(0)
        elif len(onsets) > 0 and time - curr_onset > 0:
            event = (speed, color, onset_size)
            timeline.append(event)
            onsets.pop(0)
            if len(onsets) > 0:
                curr_onset = onsets[0]
        else:
            timeline.append((0,color,0))
    
    return timeline
