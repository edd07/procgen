"""
Using Markov chains to produce a lilypond music score
"""

import os
import random

transitions = {
    # C major scale, preferring perfect intervals and eliminating tritones
    'c': 'cdeffggab',
    'd': 'cdefggaab',
    'e': 'cdefgaabb',
    'f': 'ccdefga',
    'g': 'ccddefgab',
    'a': 'cddeefgab',
    'b': 'cdeegab',
}

octave_transitions = {
    # Separate Markov chain to determine which octave we are playing. Avoids
    # sudden jumps from the highest to the lowest
    # In Lilypond, the comma denotes a lower octave, the apostrophe a higher one
    '': ['', ',', "'"],
    ',': [',', ''],
    "'": ['', "'"],
}

durations = ['4', '8', '16', '']

melody = []
state = 'c'
octave = ''
for _ in range(200):
    melody.append(state + octave + random.choice(durations))
    state = random.choice(transitions[state])
    octave = random.choice(octave_transitions[octave])


with open(os.path.expanduser('~/notes.ly'), 'w') as f_out:
    f_out.write(
rf"""
\score {{
  {{\clef bass
  {' '.join(melody)}
  }}
  \midi {{ }}
  \layout {{ }}
}}
"""
)