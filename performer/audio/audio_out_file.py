import sounddevice as sd
import soundfile as sf

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import numpy as np
import queue

class AudioOutFile:

    def __init__(self):

        self.window_size = 200
        self.fs = 44100
        self.downsample = 1#20

        self.q = queue.Queue()

    def start(self, stream):
        with sf.SoundFile("test.wav", mode='x', samplerate=44100,
                      channels=1, subtype='PCM_24') as file:
            while True:
                file.write(self.q.get())

    def update_plot(self, frame):
        return

    def update(self, indata, *args, **kwargs):
        """This is called (from a separate thread) for each audio block."""
        # TODO: rn this takes in args and kwargs and discards them...

        self.q.put(indata[::self.downsample, (0, )])

