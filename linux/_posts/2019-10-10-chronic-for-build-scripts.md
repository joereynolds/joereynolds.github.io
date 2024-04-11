---
layout: default
tags: [programming]
---

# Chronic for build scripts

Today I was working on a build script where I only wanted output if there were
failures (syntax errors, failing tests, lint errors etc...). 

Most people when encountered with this are probably used to doing the `2>&1`
hacks to silence expected output. 

## There's a better way

Or atleast more readable...

In the `moreutils` package which you probably already have on your machine
(If not you can do `sudo apt install moreutils`) is a tasty little number
called `chronic` (I'm also a fan of `vidir` but we'll leave that for another
time).

`chronic` will only display any output if it exited with a non-zero exit status.
This is useful for build scripts and the like where you don't want noise unless
it's warranted.

Running it is as simple as prefixing your command with `chronic`.

i.e.

This
```
phpunit --group myTestSuite
```

Becomes this
```
chronic phpunit --group myTestSuite
```

Enjoy your cleaner build scripts!
