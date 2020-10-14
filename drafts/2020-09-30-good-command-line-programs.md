---
layout: default
---

A good command line program should:

# Offer both short and long options

Options are important. I doubt your program can satisfy every user's needs
without *some* configuration. When a user is typing out a command,
they want the quick and dirty way that doesn't waste time and gets the job
done.

Imagine if `ls -h` had to be `ls --human-readable` every time. Talk about
--human-usable amirite?

On the other end of the scale, you probably *do* want those nice hefty longbois
in scripts. You're going to need to come back to that script at some point to
fix your inadequacies and you'll get round to fixing them much quicker if you
can read your script like a well-written novel. Ripgrep (`rg`) is an excellent
example of doing it right and there's an excellent article by /u/skeeto that
goes into further (and better) detail [here](https://nullprogram.com/blog/2020/08/01/).

# Not be chatty

**By being too verbose**
This is a mistake a lot of people new to creating command line programs fall
into. They think the clarity (read: verbosity) of the actions of the program
inspire confidence and a better UI. Can you imagine if every time you did an
`ls` it came back with

```
Listing directories...
```

before then listing the directories? It's useless. The user knows what the
program is about to do, that's why they're using it. If you still want to add a
bit of interactivity to the process, hide it behind a `-v/--verbose` flag. 

**By double-checking everything**

# Accept stdin

If you want your program to pipe and be piped into other programs,
you should make sure your program works with stdin. stdin is a beautiful thing
and one of the main unix philosophies. Take a contrived example from a simple
utility that transforms text

```
echo "STOP SHOUTING" | tf lower
>> stop shouting

echo 'tuohs esrever' | tf reverse | tf upper
>> REVERSE SHOUT
```

The true beauty comes when combining multiple programs. 
Here's an example where I go into an interactive session in `vidir` to rename
some `sql` files

```
fd --extension sql | vidir
```

(Mention here that if you don't allow stdin that you should at least try and
make it `xargs` friendly as an alternative)

# Exit correctly

Your program's your baby right? And you want people to use it **right**?
People might even use it in scripts! In this case especially, you'll want to
exit cleanly.

This means exiting with a 0 when all is gravy and then anything
non-zero for the bad times. Be as specific as you can otherwise you end up
googling what a `251` exit code when converting docx's to pdfs with `unoconv`
means (the actual issue was bad permissions which could have been documented
in the man page but instead they chose 251 as a 'catch-all' with no further
documentation).
