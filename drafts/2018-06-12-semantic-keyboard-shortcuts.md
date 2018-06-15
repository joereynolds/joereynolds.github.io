Title: Semantic Keyboard Shortcuts

----

Text: 

## Table Of Contents

- Intro
    - Mouse / Keyboard parity
- Tabbed Interfaces
- Menus
- Video players
- Reference


## Intro
The SemKey (Semantic Keyboard Shortcuts) document describes a general behaviour for hotkeys that programs should (try to) adhere to.

First off, there are generally 3 kinds of program.
- Desktop Application
- Web Application
- Interactive (Game etc...)

The Semkey document tries to outline the general behaviour for all 3 of these. Where there are any distinctions, there will be a separate line for that application. i.e. (Crude example)

Ctrl + s : Save a document
```F5 for interactive applications```

### Reasoning

The reasoning (and requirement) for such a specification is due to the large amount of inconsistencies between programs. For example to open a File Finding Search Bar, generally the shortcut is ctrl+p, however in the case of Foobar2000 (A desktop application), this becomes impossible as ctrl+p is the expected shortcut for preferences.

### Mouse / Keyboard parity

As there can be accessibility issues, and sometimes it is much quicker to do things with a keyboard, anything that can be achieved via the mouse should be achievable (in simple steps) using a keyboard.


## Tabs
### 'Tabbing'

'Tabbing' is the act of pressing the tab key in order to navigate somewhere.
Generally speaking, pressing the tab key should always take you to the next possible input

### Tabbed Interfaces

Where an interface is tabbed (i.e. a Web Browser, Busy desktop application) they should abide to the following hotkeys

```ctrl+t``` Creates a tab item (provided once can be created).
```ctrl+w``` Removes a tab.
```ctrl+tab``` Navigate forward through the tabbed items.
```ctrl+shift+tab``` Navigate backward through the tabbed items.
```ctrl+{N}``` takes you to the Nth tab

## Menus

### Listed menus
Where a menu is present. The user should be able to navigate between the menu using the arrow keys.
```In the case of an interactive application, they may also include the WASD keys```

#### Nested Menus
If there are further menus within a menu, you should be able to advance to the next menu with the right arrow key and navigate back to the previous menu with the left arrow key.
To enter a menu item the user should be able to press the Enter key.

Examples of 'listed' menus.

[Pictures here]

### Context Menus

Pressing the context menu key should open up a context menu (provided there is one) from there, the menu items should be able to be navigated via the arrow keys or in the case of an interactive application, also the WASD keys.

## Video players
A video player is either a web or desktop application. Think YouTube, Vimeo, VLC, Windows Media Player etc...

Where a video player is present and in full-screen mode, the following should apply

```0-9``` The numbers 0 through 9 take you to that portion of the video. I.e. 0 takes you to the start, 9 to the end, 3 to 40% through of the video etc...
```space``` pauses/resumes playback
```esc``` Gets the user out of full-screen mode
```tab``` tabs through the video players elements (if any exist)

Where the player is **not** in fullscreen, the following should apply.



## Rambles, categorise

http://www.usability.gov/how-to-and-tools/methods/user-interface-elements.html

https://developer.yahoo.com/ypatterns/everything.html


Where an item is selected and can be viewed/deleted etc (like Gmails email listing)
```del``` Should delete the item (in the case of gmail take it to the trash)
```enter``` Should drill down and view the item
As with other menus (is this a menu)
```up``` takes you to the item above
```down``` takes you to the item below

## Games

### Small levels

Where a game has distinct levels,

```r``` should restart the level.

## Hotkey Reference

### Menus

### Tabbed Interfaces