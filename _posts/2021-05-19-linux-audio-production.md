---
layout: default
tags: [programming]
---

# Linux Audio Production

The future is here. I have moved my audio stack to Linux with no problems.

All the VST's I used on Windows can be bridged to work on Linux.

The guide below assumes that the distro you're using is Arch based (I use
Manjaro) and the DAW is Reaper.

**Note** I had this working successfully with Ubuntu 20.04 but switched over to
Manjaro for unrelated reasons. To reiterate, this *will* work on Ubuntu, the
installation is a tiny bit more involved (though still not very, just follow
the README and you'll be fine) but that's all.

## Setup

### Install yabridge and yabridgectl

Use yabridge and yabridgectl (much easier than linvst and the dev is on discord
and very active)

If you're on Arch or something similar

```

yay -S yabridge
yay -S yabridgectl
```

### Tell yabridge where the plugin directories live

For Reaper the VST directories are `~/.vst` and `~/.vst3` by default. 
Tell yabridge about these with the following:

```
yabridgectl add ~/.vst
yabridgectl add ~/.vst3
```

### Install some plugins

Download some plugins and move them into ~/.vst.

Do the following to confirm

```
yabridgectl status
```

Once you're happy, do

```
yabridgectl sync
```

To bridge them over and that's it!

Start up Reaper and your windows plugins will be on your Linux machine <3

#### Plugins through wine

Some plugins like to be inconvenient and have `.exe` executables to run instead
of a .DLL In that case, do this:

- Install the plugin using wine
- Make note of the VST plugin path (something like C://Users/Joe/Program Files/VST...)

This path lives in Linux under a `.wine` directory.
Mine is

```
/home/joe/.wine/drive_c/Program Files (x86)/VstPlugIns
```

- Add this path with yabridgectl (You need to escape spaces and braces)

```
yabridgectl add /home/joer/.wine/drive_c/Program\ Files\ \(x86\)/VstPlugIns
```

Remember to add this path to Reaper too in preferences so that it knows to look
here for plugins.

And there we go... again.


