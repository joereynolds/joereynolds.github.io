---
layout: default
---

So, when I run `xbacklight` locally with i3 as my window manager, I get:

> No outputs have backlight property

I've tried multiple "proper" fixes to this and they either bork my desktop
environment or just plain do not work. I've hacked around it with some terrible
bash that I thought I'd share on the off-chance others have had this happen to
them.

Here we go:

```
reduce_brightness() {
    brightness=$(echo "$(cat /sys/class/backlight/intel_backlight/brightness) - 1000" | bc)
    echo "Reducing brightness to $brightness"
    sudo bash -c "echo $brightness > /sys/class/backlight/intel_backlight/brightness"
}

increase_brightness() {
    brightness=$(echo "$(cat /sys/class/backlight/intel_backlight/brightness) + 1000" | bc)
    echo "Increasing brightness to $brightness"
    sudo bash -c "echo $brightness > /sys/class/backlight/intel_backlight/brightness"
}
```

Standard stuff really. Just subtract 1000 from the current value and set that as
our new value.

Enjoy!
