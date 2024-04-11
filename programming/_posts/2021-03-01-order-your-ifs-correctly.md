---
layout: default
tags: [programming]
---

# Order your ifs correctly

One thing we all learn to do right at the beginning of our programming journey
is to learn about conditionals. The majority of the time (depending on the
language) they'll also mention that an `if` statement "short circuits". This
basically means it evaluates the first condition and will continue/exit
depending on the result of that condition.

Example in Python:

```
                         -- Only ran if some_operation() runs successfully
                        |
                        v
if some_operation() and some_other_operation():
    ...
```

We can use this to our advantage when looking for easy things to optimise.  A
rule I follow is "put the cheapest condition first".

There's no point in putting an expensive check at the beginning if it's not
going to enter into the rest of the block.

Here's an example using the same `if` but re-ordered:

### Good

Checks for a simple boolean before continuing on to a more expensive check on
whether some in-game effects are still rendering.

```
if not self.level.renderer.escape_menu.is_visible and not self.level.renderer.transition.is_transitioning():
```


### Bad

Checks that all in-game effects are no longer transitioning and then checks a
boolean on the escape menu.
```
if not self.level.renderer.transition.is_transitioning() and not self.level.renderer.escape_menu.is_visible:

```

And that's it!
