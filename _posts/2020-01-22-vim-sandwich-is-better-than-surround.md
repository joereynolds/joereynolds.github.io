---
layout: default
title: vim-sandwich Not surround.vim
---

# vim-sandwich not surround.vim

[Time](https://www.reddit.com/r/vim/comments/d6k92i/how_to_insert_text_before_and_after_selected/f0u1ac7/)
and
[time](https://www.reddit.com/r/vim/comments/d6k92i/how_to_insert_text_before_and_after_selected/f0veru3/)
again people praise [surround.vim](https://github.com/tpope/vim-surround) for
what it can do. I don't think this is out of any sort of evangelism, just that
they're unaware of the alternatives offered <a href="#1">¹</a>.

[vim-sandwich](https://github.com/machakann/vim-sandwich) is our alternative in
this case. It boasts the feature set of surround.vim and more!


## Why vim-sandwich?

### 1) Can operate on all text-objects and motions

Whereas surround.vim can operate on a few motions (`w`, `W`, `s`) on targets,
vim-sandwich correctly operates on the entire vim vocabulary and can also take a
count. Doing `sa2}"` will surround the next two paragraphs in double quotes for
example.

This is by far the biggest advantage vim-sandwich has over surround.vim. Read
the
[docs](https://github.com/machakann/vim-sandwich/tree/master/doc/sandwich.txt)
(`:help sandwich.txt`) or better yet, install it and see for yourself.

### 2) Well tested

Seriously, look at the [amount of
tests](https://github.com/machakann/vim-sandwich/tree/master/test) this thing
has.
[Regressions](https://github.com/tpope/vim-fugitive/commit/d428032600f738ff5246576a92716779a2b9d5d7)
[in
code](https://github.com/tpope/vim-fugitive/commit/cb613ca05d3d195d52cfb5ce32f44c1d9e196214)
are very hard to make happen in well tested code.

### 3) Is repeatable with '.' without an extra plugin

surround.vim is repeatable however it relies on tpope's repeat.vim plugin being
installed, vim-sandwich has built-in support for repeatability.

### 4) Has a generic 'b' mapping, to target the outer block

Instead of being specific and having to say `sr'"` to replace single quotes with
double quotes, we can use `b` which means "the outer block". `sr'"` then becomes
`srb"`. I know it doesn't seem like a big deal but you'll quickly find this
slipping into your day-to-day use of vim-sandwich. surround.vim has something
similar though not as generic, `b` stands for `(`, `B`, stands for `{`. 

### 5) Does HTML/XML tags in a nice way

The `t` command after a motion or text object tells vim-sandwich that you want
to add a tag. At that point, it will bring a prompt up and you can enter
whatever you want.

To surround a paragraph in `p` tags you would do `sa}tp` (and of course you
could delete these with `sdb`).

### 6) Visual feedback

When using vim-sandwich, there is unobtrusive visual feedback every step of the
way. `sr'"` will highlight the single quotes until you have pressed the
replacement character. `sa}tp` will highlight the paragraph (`{`) until you have
added in the rest of your command. Having this available makes me much less
clumsy and more confident in what I'm doing.

### 7) Your own surroundings

If that's not enough, vim-sandwich boasts a thing called 'recipes' which are
your own surroundings that you can write in vimscript. I've never dug this far
in, my needs are quite basic but some users may find this useful.

### 8) A whole lot more

There's a load of other stuff in the documentation I've omitted that I recommend
reading (`:help sandwich.txt`).

## Why surround.vim?

After all that, why should you stick with surround? 

One of the biggest issues with vim-sandwich is that it messes with the `s`
substitute binding, I never used this anyway so I don't miss it. Apart from
that, I would say surround.vim has more intuitive mappings but the author of
vim-sandwich has made this [possible
anyway](https://github.com/machakann/vim-sandwich/wiki/Introduce-vim-surround-keymappings).


## A syntax comparison

### Changing ' to "

```
# surround.vim
cs'"

# vim-sandwich
sr'"
or
srb"
```

### Surrounding something with tags

```
# surround.vim
ysiw<em>

# vim-sandwich
saiwtem
```

### Deleting surrounding quotes

```
# surround.vim
ds"

# vim-sandwich
sd"
or
sdb

```

### You failed to mention [X] and that surround.vim can do [Y]

Cool, bring it up in this [thread](https://www.reddit.com/r/vim/comments/esrfno/why_vimsandwich_and_not_surroundvim/?) and I'll update this article.

### Just because it's the most popular doesn't mean it's the best choice

There are many great smaller vim plugins around and unfortunately, you really
have to search for them. A lot of the time they trump the competition but the
competition got there first and/or already have a name for themselves. 

I'd always suggest looking around for the plugin you want instead of settling on
the plugin that's offered, it's not always the best choice.


### References & Footnotes


[surround.vim](https://github.com/tpope/vim-surround/) 

[vim-sandwich](https://github.com/machakann/vim-sandwich) 


¹ <small id="1">I too have felt the pain of the tpope monopoly when
[dadbod](https://github.com/tpope/vim-dadbod) crushed my [sql plugin's
popularity](https://github.com/joereynolds/SQHell.vim) :(</small>
