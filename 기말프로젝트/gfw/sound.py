from pico2d import *

sounds_m = {}
sounds_w = {}

def load_m(file):
    global sounds_m
    if file in sounds_m:
        return sounds_m[file]

    sound = load_music(file)
    sounds_m[file] = sound
    return sound

def unload_m(file):
    global sounds_m
    if file in sounds_m:
        del sounds_m[file]

def load_w(file):
    global sounds_w
    if file in sounds_w:
        return sounds_w[file]

    sound = load_wav(file)
    sounds_w[file] = sound
    return sound

def unload_w(file):
    global sounds_w
    if file in sounds_w:
        del sounds_w[file]
