---
layout: default
title: Entr - The File Watcher You've Never Heard Of
---

# Entr - The file watcher you've never heard of

[Entr's website](http://eradman.com/entrproject/)

`gulp`, `grunt`, `watchman` or any of the proprietary built-in watchers in
IDE's. You do not need them, or rather, there is a light alternative that I want
to show you and it's 'unixy'.

Its name is `entr`, it's written in C, it's small and simple. There are no
configuration files and no installation steps, it just works™.

Let's start with the classic example of rebuilding the project on change:

```
ls | entr make
```

How about running unit tests after certain files have changed?

```
fd . {src/,tests/} -t f | entr composer run test-unit
```

How about re-executing that SQL you're working on?

```
fd . | entr mysql -h 12.345.67 -u sql-user -p somepassword < your_sql_script.sql
```

Basically, get a list of files you want to watch (I use `ls` and `fd` in the
examples above) and pipe it to `entr`.

## Where it shines

Local development environments where you want to quickly iterate with immediate
feedback.

## Where it doesn't

Anything past local development environments. These kind of things are not
maintainable in the long run, unless you're a code golfer I guess.

## Versioning your watchers

Want to version and alias your watchers so you don't have to type out that long
command everytime you start developing?

If this is you (it's definitely me), then you probably want
[entree](https://github.com/joereynolds/entree). A version controllable wrapper
for entr that also aliases watchers. I created it a while back to scratch the
itch I just described. I [wrote about it
too](https://joereynoldsaudio.com/2018/06/17/entree.html). You should use it. It
has tab completion.
