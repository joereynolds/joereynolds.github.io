---
layout: default
permalink: /programming/2025/10/02/python-and-pygame-performance-dump.html
archived: true
---

# Python/Pygame performance dump

This is a living document that I update from time to time containing the dos
and don'ts to getting useable performance for your Pygame games. There's some
python stuff in here too but we're mostly here for Pygame.

Before doing anything, you should grab a profiler and run it against your game.
I personally use [scalene](https://github.com/plasma-umass/scalene).

Oh and a shameless plug before we begin, [my game](https://store.steampowered.com/app/3122220/Mr_Figs)


## Pygame

- Convert your images, all of them

- Don't scale things in a loop. Do it outside (usually in the `__init__`)

- Don't blit to your display size, blit to your game's resolution (320x180 in
  my case) and scale that up.

- Don't render text per frame. Do it in the `__init__` and then reference it later

- Alpha blitting is slower than non-alpha, beware of this

- If you just care about _if_ something has collided, use
  `pygame.sprite.spritecollideany`, it's faster than `spritecollide`, it even
  mentions this in the docs 

- Use object pools to prevent creating loads of stuff on the fly. This is a bit
  more involved but there's some good reading
  [here](https://gameprogrammingpatterns.com/object-pool.html). I use this
  successfully for my particle system.

- Use a [simple
  grid](https://gameprogrammingpatterns.com/spatial-partition.html) to speed up
  collisions. This is also slightly involved but it's helped me quite a lot
  with optimising bullets in my game

The last two in particular I'd only pull out _when_ you see a problem. Don't
optimise for the sake of optimising.

## Python

**Where building lists, dicts, sets etc, use comprehensions.**

<details>

## Why?

Comprehensions are at a C level so are always going to be faster than your
`for` loop

Don't do:

```
even_numbers = []
for i in range(10):
    if i % 2 == 0:
        even_numbers.append(i)
```

Do:

```
even_numbers = [i for i in range(10) if i % 2 == 0]
```
</details>


- Anywhere you're using `dict()` or `list()`, replace them with `{}` and `[]` respectively. Again, it's faster

- If the data in your list does not change, use a tuple. Again, faster
