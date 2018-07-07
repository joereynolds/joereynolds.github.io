# You (probably) don't need Vimwiki

Why are you using [vimwiki](https://github.com/vimwiki/vimwiki)?

Probably to make notes, right?

Well did you know that you don't need a plugin for this?

Of course you did!

Let's go through some of Vimwiki's features and dispel them in places of vim alternatives.

Vimwiki states the following features   

##### 1. Organise notes and ideas

TODO - weird phrasing
It's understandable vimwiki boasts this feature, when I used to use vimwiki, I loved the linking and referencing all over the place, 
but I have two letters for you; `gf`.

`gf` allows you to edit the file under the cursor (assuming it's in your path).

With a sensible directory structure, you can easily organise your notes and ideas.

Take a look at [my repo](https://github.com/joereynolds/life) and come back here when you're done.

That repository is just a dumping ground of articles that I may or may not write at some point but the point is,
it's entirely navigable with vim.

The directory structure is:

```
README.md   
docs/
  article-1.md
  article-2.md
  article-3.md
  article-4.md
  index.md
```

`README.md` is the 'entrypoint' that most devs would open up straight away and contains a link to   
our main page, `index.md`.

`index.md` is just a table of contents hyperlinking to all other articles and looks like this:

```
- article-1.md - A description of what article-1 is
- article-2.md - A description of what article-2 is
- article-3.md - A description of what article-3 is
- article-4.md - A description of what article-4 is
```

From here, you can easily browser articles by pressing `gf` to edit the file your cursor is on.

From there, I usually use the jumplist (`<c-o>`, `<c-i>`, see `:help jumplist` for more) to go back and forth
between the article and index page.

The only thing that Vimwiki has over vanilla vim at this point is that with Vimwiki you can name the links, but
a well-named file would serve that purpose too.

##### 2. Manage todo lists

I don't really understand this one. In my eyes, a todo is just a text file, so you can 
manage that how you want.

##### 3. Write documentation

There are two thoughts that go through my mind with this one:

1) You can easily write documentation in any editor, I'm not sure what vimwiki brings to the table here (TODO find out) but it's possible'

2) I would prefer something built for this purpose such as [readthedocs](https://readthedocs.org/) 

##### Maintain a diary

Ok, vimwiki wins here, I have no idea how you'd do this without too many lines of vimscript.

##### Export everything to HTML

Again, two points here:

1) The entire point of markdown is that it's easily editable and readable just as is, 
   write your notes in markdown and you won't even need to render it to HTML.

2) If you want to render stuff to HTML, just use [pandoc](https://pandoc.org/) it's entire purpose 
   is converting files from one format to another and will do what you need here.

   A mapping to convert the current markdown file to HTML could look like:

   ```
   nnoremap <leader>r :!pandoc % --to=html5 > %.html
   ```
