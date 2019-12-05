---
layout: default
tags: [music, programming]
published: false
---

# The sounds of Pi

<iframe 
    width="100%" 
    height="296" 
    src="https://www.youtube.com/embed/ieRqPCtJfew" 
    frameborder="0" 
    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
</iframe>

## What is it?

The sound of Pi is another Pure Data experiment. Similar to my last one
([meteor](/2019/07/24/meteor.html)) it is focused around sonifying data.

The sound of pi plays the first 400 digits of pi. There are 8 sawtooth
oscillators and each one is assigned 50 notes from pi. The whole thing is based
off of pitch classes and musical set theory (we'll get to that later). For now,
here's the patch.

## The patch

![Imgur](https://i.imgur.com/yKOp0uS.jpg)

There are 8 oscillators going off continuously (`nth-pi-osc`). As you can see
from the creation of `nth-pi-osc`, each one has its own segment to look after.
One starts reading at 0, another at 50, another at 100 and so on...

## Pitch classes

## Data

## Abstractions

### nth-pi-osc

![Imgur](https://i.imgur.com/HDb2Dao.jpg)

This abstraction is responsible for getting the current value of pi for its
oscillator and sending over the frequency. Nothing complex here but note the
following:

1) `+ 60`. We add 60 to every MIDI note as we want it to be based off of C (that
           is to say that 0 in our pitch class is C).

### pd-ramped-osc

![Imgur](https://i.imgur.com/06C8ioi.jpg)

This is what produces the majority of the sound, the rest of the patch is just
reading data and using math to make sure we're using the correct digits of pi
for each oscillator.

Still, this sub-patch is very simple.

## Misc

