from time import time
import numpy as np

from random import randint

class Oscillator:

    def __init__(self, audio=None, controller=None, volume=1, multiplier=1, offset=0, child_osc=[], dependents = set()):

        self.audio = audio
        if audio:
            audio.attach_voice(self)

        self.controller = controller

        self.annimatable_param = {}

        self.current_index = randint(0, 44100)

        self.child_osc = child_osc

        self.volume = volume

        self.multiplier = multiplier
        self.offset = offset

        self.last_sample = np.array([0])

        self.dependents = dependents

        self.launched_dependents = False

    def _add_dependents_to_audio(self):
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                # print(getattr(self, attr), isinstance(getattr(self, attr), Oscillator))

                if isinstance(getattr(self, attr), Oscillator):
                    print("ADDING", attr)
                    self.audio.add(getattr(self, attr))

    def __float__(self):
        # print('s', self.last_sample)
        return self.last_sample

    def next(self, buffer_size=None):

        if not self.launched_dependents: 
            self._add_dependents_to_audio()
            self.launched_dependents = True

        self.current_index += 1

        self.current_index = self.current_index % (2 * self.audio.fs)

        if buffer_size==None: buffer_size = self.audio.buffer_size()

        s = self.volume.__float__() * self._next(buffer_size=buffer_size, fs=self.audio.fs, sample_index=self.current_index)

        self.last_sample = s

        return s

    # note factors can be either ints or other osc objects

    def __add__(self, factor):
        # TODO: implement audio, controller merge for sum of separate sources/controllers

        if type(factor) in {int, float}: 
            # self.offset += factor
            return Oscillator(audio=self.audio, controller=self.controller, offset=self.offset+factor, multiplier=self.multiplier, child_osc=[self], dependents=self.dependents.union({self}))

        return Oscillator(audio=self.audio, controller=self.controller, child_osc=[self, factor], dependents=self.dependents.union({self, factor}))

    def __radd__(self, factor):
        return self.__add__(factor)

    def __mul__(self, factor):
        if type(factor) in {int, float}: 
            return Oscillator(audio=self.audio, controller=self.controller, offset=self.offset, multiplier=self.multiplier*factor, child_osc=[self], dependents=self.dependents.union({self}))
        
        # handle amplitude modulation in this way...
        raise NotImplementedError
        return self

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def _apply_consts(self, signal):
        return self.offset + self.multiplier * signal

    def _next(self, buffer_size, fs, sample_index):
        return self._apply_consts( sum([i._next(buffer_size, fs, sample_index) for i in self.child_osc]) )