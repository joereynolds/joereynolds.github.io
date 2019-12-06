---
layout: default
tags: [music, programming]
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

The sound of pi is based off of the first 400 digits of pi. There are 8 sawtooth
oscillators and each one is assigned 50 notes from the 400 digits. The patch is
based off of pitch classes and musical set theory (we'll get to that later).

## The patch

![Imgur](https://i.imgur.com/yKOp0uS.jpg)

As you can see, it's pretty small and there aren't many abstractions hidden
underneath either.

The 8 oscillators mentioned previously are the `nth-pi-osc`s that you see in the
patch.  You can see from the creation of `nth-pi-osc` that each one has its own
portion of pi (heh) to look after. One starts reading at 0, another at 50,
another at 100 and so on...

The 50 numbers contained within each oscillator are 50 numbers of pi and are
treated as integer pitch classes all relative to the root of C.

The concept of a pitch class is simple. If you can count to 12 and know the
alphabet up to G, then congratulations, you can understand pitch class theory.
Let's go through it anyway...

## Pitch classes

We'll dissect the first few notes of this patch to get a better idea of what a
pitch class is.  Let's take the first oscillator (`[nth-pi-osc 0]` in our case).
It will be dealing with the first 50 digits of pi. Here are the first 10 it
encounters:

`
{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}
`

We treat each number as a semitone distance from a chosen root note. We've
chosen the root of C so in this case it will yield the following:

`
{Eb, Db, E, Db, F, A, D, Bb, A, Eb}
`

For the most part, that's it, you now understand pitch classes and musical
set theory. There's a whole lot more to pitch classes that you **can** explore,
but for the purposes of understanding this patch, that about covers it.


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

Still, this sub-patch is very simple. Where the magic happens is all contained
within the `line` object. It takes 60000 milliseconds to reach it's target
frequency of whatever `$1` is. Finally, it passes that on to our sawtooth wave
(`phasor~`).

## Data

The patch reads from a text file which contains 1000 entries of pi (I only chose
to use the first 400). Each entry is on its own line so have the following:

```
3
1
4
1
5
9
2
6
5
3
5
8
9
...
```

There's nothing really magical here though I do like the rendered array of pi
that Pure Data produced. Neato.

