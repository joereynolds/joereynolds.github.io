# Things I learnt from N years of solo-developing a game and losing my mind

This is a long exhaustive post. I'd recommend just reading the parts that are
relevant/interesting to you.

## Backstory

I wanted to make a game.

It would be a game that _I_ would want to play and would've enjoyed had someone
else made it instead (spoiler, they hadn't. At least not my vision).

The game would be a topdown Bomberman dungeon crawler.

Nothing groundbreaking but I always thought the bombs in bomberman were neat
and nobody ever seemed to take it anywhere sadly

A quick in-out mission. 50 levels, all short, no frills, simple.

[Rick and morty image here]

Fast-forward 5 years and we have:

- 120 levels (at time of article)
- Bosses
- Secrets
- Puzzles


Here's everything I learnt during the journey. Solo-developing is multi-faceted
and you will wear every hat you can think of. Even the smelly sweaty ones you
don't want to wear.

Let's begin

TOC

- Gamedev
- Python
- Pygame
- Level design
- Art
- Audio
- Marketing


### Gamedev

We start with the big guns. This is the core of your game and here are some
lessons I learnt along the way which perhaps would've been more useful at the
start.

- Add visual debugging as early as possible.
    - It's much easier to _see_ why something is going wrong versus reading it
      in the code. A small line that displays an enemies line of sight is
      invaluable whilst debugging

- A feature sometimes needs to be fleshed out to test
    - You might have an idea for an enemy in your game. To save time, you don't
      source any sound fx, or any art. You use squares for now. I did this and
      I found that it really killed the idea dead in its tracks. Sometimes
      (even if it doesn't work), you need to flesh out your idea a lot to see
      its true potential. Sadly, this also means wasted time sometimes.

      A good example of this is the butchering mechanic in Stardew Valley. It
      never becamse a thing because the creator found it a bit too dark in
      contrast to the rest of the game (show a screenshot of that mechanic
      here)

- Save your time as much as possible
    - Originally, I intended Mr Figs to be my magnum opus. A complete "me"
      creation. That is, my own music, art and sound FX. One day a dev on the
      team I was in at my actual job sent me a link to some royalty free bundle
      of music and FX for £30. It's RRP was £2500. Yes, two thousand and five
      hundred pounds. The music and FX in here were vast, covered everything
      needed, would save me hundreds of hours and (painful to admit as a
      musician first and dev second) would be better than anything I could
      produce. 
    
- Components are your friend. DRY
    - See how you have 5 different enemies all needing to move?
    Yeah, just make a `moves` component and then attach it to that entity.
    Instant reuseability and you can whip up new mechanics much faster

    I do this all over the place. Nothing is a "skeleton" for example, it's all just a bag of components that might look like

    ```
    # components
    [
        Speed,
        Velocity,
        Moves,
        EmitsEventOnSight,
        ChangesStateOnEvent
    ]
    ```

- spatial grids are a relatively easy way to get good performance from
  collisions
    - Don't go straight for the recursive quad tree (unless you really want
      to). Do the simplest thing you can to get performance out of your game.
      Even a level subdivided into even gridded cells works and is incredibly
      simple

- Object pools are a great way to combat the side effects of Python's GC (show
  picture here)
- particle pools are an excellent way to get more particles on screen and
  increase performance. Fiddly to set up but great rewards

Some more reading material

- Game Programming Patterns
    - I kept this around all of the time. Use it when you need it, it's not
      something you read cover-to-cover and you certainly won't need every
      pattern in this book

- Game Engine Architecture
    - Admittedly not very relevant for topdown 2d games (they're pretty simple)
      but it still had some common concepts and ideas that you should take
      on-board. Think of this one as optional

- Tyler Glaieals blog
    - I have a soft spot for this man because he programmed some of my
      favourite games. His article on gettin a reliable stutter-free FPS is
      worth a read

### Python

This is probably not a section you'd like to read (especially if you're coming
from /r/python, sorry) but I did not enjoy my time with Python.

Python was the first language I learned when I started learning to program in
2013 so it has a special place in my heart for that reason but it kind of ends
there.

I found numerous small but annoying issues with Python while creating Mr Figs:

- Packaging is a complete mess. It's 2025 and only now are they finally talking
  about lock files.
  - It's only through the wonders of uv that Python is tolerable. Virtual envs are clunky.

- It's bloated.
    - This is more of a personal rant. I like small and minimal and python is
      just not that. I don't need `linear_regression()`s, `harmonic_means()`,HTTP
      servers and 456456 different ways to format a string. If I could have
      told myself to consider Lua, I would have. those guys got it right.
    
- It's S L O W. Ordinarily not too much of a problem but it's very
  disheartening when I'm having to do particle pools just to get 2000 particles
  on the screen. If this were C I'd easily be getting 10/100 times that amount.

- The type system is very much bolted on and an afterthought.
    - You have to specifically import certain types, seriously? I don't want to
      `from typing import List`, I just want to typehint it as `List`, no
      import.

That said, with all the terrible performance and strange design decisions, you
do get some good stuff out of it:

- Itertools is great
- List comprehensions have always been great
- There's a tool for everything
    - Admittedly I'd prefer a smaller stdlib but when I have the choice of
      writing my own or using theirs. I'm using theirs. It's been optimised and
      most likely it's written in C
- Not using datacalsses for speed

### Pygame

- Use groups where it makes sense to minimise calls to collision methods 
    - Don't just have a `sprites` group. Why? Because if you add everything
      into it and you're then checking that group for collisions, you're
      checking against waaay more than you need to. I didn't do any fancy
      active/inactive groups but I did split things out into many smaller
      groups which ended up usually consisting of less than 10 objects per
      level.

      The game knew how to poll the correct groups depending on the levels too.

- Use libraries. There's nothing available to you out the box so don't make it
  harder on yourself 
    - pygame-text is good for quickly getting text on the screen
    - pytmx for parsing tiled map files
    - pyscroll for scrolling maps

### Level Design

Level design is one of those things where people won't notice if it's good.
However, if it's bad, players might get frustrated (level too hard), or bored
(level too easy).

You need to hit that sweet spot and keep it interesting. For me, this meant
doing the following:

Keep in mind that all my lessons on level design strictly apply to a topdown
view with a slight lean towards puzzles. There's no hiding behind obstacles or
any stealth elements and there's certainly no Z-axis, we do 2D here sir.

- Enter the design of the level by answering "What am I trying to teach the
  player?"

- Linear vs Parallel levels
    - Show an example of a parallel level (third area with tape at beginning)
    - Show example of linear level (most of the other third area ones)

- Bring in mechanics one at a time, slowly and ramp it up
- Give the players breaks after lots of intense levels

- Show the problem before the solution
    - Show example here

- Empty space is a no-no (unless used for effect)


Some games I learnt level design from:

- Hollow Knight
    - Within the first 5 minutes of this game you're getting blasted by many
      different mechanics. Bugs, spikes falling from the ceiling, large drops
      and also tiles that crumble when stood on. This showed me you don't have
      to be _too_ sensitive around introducing things to the player.

- Celeste
    - Players can withstand dying lots of times if the game plays fairly. Mr
      Figs is nothing like Celeste really but the lesson is still relevant

- The End is Nigh
    - This game is mechanics galore. It taught me that it's okay to have loads
      of different mechanics. You should be intentional with this though. Don't
      introduce unneccessary mechanics. Keep things as simple and tight as
      possible


### Marketing

- Be consistent
    - Post _something_ as often as you can. I'm not expecting huge success from
      my game so I just try and post once a week. I believe if you're more
      serious you should be aiming for daily. This is hard for a solo dev in
      their spare time though...

      It could be a random clip, a short or YouTube video but without these,
      people won't know your game exists. The baseline for any game in terms of
      wishlists if you don't market is 0, remember that

- Don't get discouraged by failure
    - I think most people (me and included) thinks that either there game is
      something special or it will be something special when it's done. When I
      released the early-access demo of my game, I got very few bites. It was a
      reality check and also a glimpse at what the release would probably be
      like.

- Do the math
    - Let me bring Mr Buzzkillington in for a second and do some basic math
      that will hopefully guide you on a sensible path. We'll assume that you
      released your game with 10000 wishlists since that's what everyone aims
      for.

    Let's say 100% of those convert (won't happen) and your game is $10. That
    makes you £100,000, a nice wad of change.

    However.

    - Steam take their cut of 30% - £30000 (£70000 left)
    - The average refund rate is ~10% so say goodbye to another £10000 (£60000 left)
    - Income and VAT - Variable but let's say £5000 (£55000)
    - You probably released it at a discounted rate so let's that's another £5000 (£50000)

    You're left with £50k. I've been kind here and not factored in any other
    expenses you may have but what this equates to more-or-less an annual wage
    of a mid/senior-level software developer.

    Only difference is you put more than a year into your game, burnt yourself
    out and expected the world.

    Take the lesson that nobody cares about your game. You have to _make_
    people care. Once you have a realistic vision of what might happen, I think
    you'll be better off.


### Art

The art in Mr Figs is simple. It's cohesive (mostly) but simple. This was
intentional.

All the sprites are 16x16 so that I could give myself a fighting chance at
making something aesthetically pleasing.

- Keep it simple. 
    - You're going to have to animate that sprite which contains 40 colours and
      5 different shades of red. Do yourself a favour and do less. You'll gain
      clarity, speed and your time back
    - Edmund McMillen (Supermeatboy, TBOI, Mewgenics) is a great example of
      this)

- Be consistent.
    - See that green you used for the bushes? Yeah, that should be _your
      green_. Any time as much as possible (just like a well written function)
      try and re-use a colour. The exceptions I have to this are for small
      deviations for shading but generally speaking I reuse as much as I can
      and keep my palette small

- Lose the detail.
    - This one is specific to working on a 16x16 canvas but the fact is, you're
      not going to be able to fit in the shine of that person's eye on their
      pupil. You can try but people will definitely confuse it for anything but
      that.

Some resources I liked:

- Pixel Pete Youtuber
    - The opposite of Adam Younis. Get's right to the drawing without much
      theory. Generally I prefer this, I have to be in a particular mood for
      Adam

- Adam C Younic Youtuber
    - Longer form videos on pixel art. Discussions around shading, intent,
      character design etc...

- Jackie Droujko
    - An animator that works for Disney (I think?). She does excellent
      portfolio reviews where you can see how she touches up bad art. Not pixel
      art but still very good

### Audio

There's actually not much to put here thankfully. I did music at University and
have written music ever since.

This hat was well worn and didn't need any explanation.


### Everything else

