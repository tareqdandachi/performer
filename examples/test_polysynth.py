import asyncio
from signal import signal
from performer import *

from threading import Thread

from performer.controllers.controller import Controller

controller = MIDIKeyboard(midiout=False)

# print(sounddevice.query_devices())

audio = AudioOut(fs=44100, 
                    buffer_bit_size=8, 
                    channels=1, 
                    volume=0.4, 
                    controller=controller, 
                    output_device=1,
                    latency=0.01,)

F = Param(300, 'freq')

freqs = {}

controller.attach_freq(F)

def loop(audio):
    global freqs

    f = F.get()

    idx = freqs.index(F.get())

    if idx == None:
        freqs[f] = LFO(audio=audio, f=F, volume=1, type=Sine, fmul=1)

    else:

        freqs[idx]

# lfo_mod = 0.5*LFO(f=10)+0.5
# lfo_mod = LFO(f=200)+200
# lfo_mod.audio = audio

# audio.add(lfo_mod)


# lfo2 = LFO(f=F, fmul=0.66, volume=A) + LFO(None, f=F, fmul=0.33, envelope=None, volume=A)

# lfo1.audio = None
# lfo2.audio = None

out = lfo1

# out = ADSR(lfo1 + lfo2, None)
# controller.attach_envelope(out)

audio.attach_voice(out)

out.audio = audio

# asyncio.run( audio.stream() )

# asyncio.ensure_future( audio.stream() )
# loop.run_forever()

print("RUNNING")

audio.stream(loop)

# audio.destroy()

# def asyncloop(loop):
#     # Set loop as the active event loop for this thread
#     asyncio.set_event_loop(loop)
#     # We will get our tasks from the main thread so just run an empty loop    
#     loop.run_forever()

# create a new loop
# loop = asyncio.new_event_loop()
# # Create the new thread, giving loop as argument
# t = Thread(target=asyncloop, args=(loop,))
# # Start the thread
# t.start()


# asyncio.run(  audio.testing() )


# C4 is 60
# A is C, thru L is D
# wetyuo sharps