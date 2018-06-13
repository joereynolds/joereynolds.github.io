Title: How My Site Works

----

Text: 

I just want to take a quick minute to talk about how this site works, what's going on underneath the hood and some other small bits

# CMS

The CMS I'm using is Kirby CMS. The way I would describe Kirby, is that it's a developer friendly, NoSQL CMS that is based on text files. I love it, seriously, it's flexible and the API is friendly but of course it has a few flaws.

Anyway, the main thing that enticed me to kirby was its simplicity and its flexibility. If you're comfortable with PHP then you're comfortable with Kirby. Enough talk, let's get to it.

##  Features

### Article Lists
On every section of my site (Music, Programming, and Misc) there is a list of every article that pertains to that set of pages. Everytime I add a new article to the site, I don't want to have to manually add it myself to every page that references it. I've built a simple Kirby template which does this for me. It fetches the title and wraps it in 'a' tags and links through to the correct page. The main part of code looks like this:

```      
<?php foreach($page->children()->children()->visible() as $article): ?>
    <a href="<?php echo $article->url() ?>"> 
        <?php echo html($article->title()) ?>
    </a>
<?php endforeach ?>
```
Fairly simple and it shows the simplicity of the API. I found that the classes used in the CMS are very logical and what you would expect.

### Blurbs

The next thing I wanted to do was to create a 'blurb' of each article. Basically, this would be a short description of each article with a 'read more' link for the user. This enables the user to view a snippet of the article before they have to dive straight into it. Here's what the code for that looks like:

```
 <!-- Echo the title and the first X amount of words as a blurb' -->
 <?php foreach ($page->children()->visible() as $article): ?>
     <a href="<?php echo $article->url() ?>">
         <?php echo html($article->title()) ?>
     </a>
     <div class="blurb">
     <i>
         <?php echo substr($article->content()->text(),0,150) ?>
     </i> 
     <a href="<?php echo $article->url() ?>">
         read more...
     </a>
     </div>
<?php endforeach ?>
```
Again, fairly simple. It should be noted that I created a  'blurb' class that I can later style individually to my needs (In this case, I ended up graying out the blurb so that the 'read more' link stands out more)

### Downloads

On my downloads page, there is a list of all songs categorised by genre; Acoustic, Electronic, and Rock.
Each of these get's put in the relevant heading dictating the genre. It's all automatic so all I really have to do is pop a file in a folder and it appears on my site!

Here's how it works:
(image: assets/images/musicShot.png)

Each song is prepended with a letter ('A', 'E', 'R'). Each letter represents a genre, anything that doesn't have a capital of those 3 letters is ignored.
A = Acoustic
E = Electronic
R = Rock

Once we have the correct genre, all that's left is to trim off the letter and the whitespace before it and give the rest of the title to the page!

Here's what this code looks like :
```
<div class="downloadBox" id="acousticDownload">
    <h2>Acoustic</h2>
    <!--Grabs all acoustic music. Acoustic music starts with an 'A'-->
    <?php foreach($page->files() as $file): 
        if ($file->filename()[0] == 'A'){
            echo '<a href="'.$file->url().'">'. substr($file->name(),1).'</a>';
        }
    ?>
    <?php endforeach ?>
</div>
```
Pretty simple
1. Wraps it up in a div for styling
2. Gives it a header
3. Grabs the relevant files
4. Echoes the files name (ignoring the first capital letter')
5. Ends

### Article Counts 

I had the idea of a small line of text displaying the total number of article counts on that page but then I thought it was a bit pointless and removed it. Nonetheless, I'll share the code since it's fairly simple and it might come of use later on for me.
```      
<!-- Echoes the number of programming articles -->
<?php echo $page->children()->children()->count() ?> Articles so far<br>
```

# More About The CMS
## CMS Awes

These things really struck me as great things about Kirby. 
Obviously different CMS' cater to different peoples needs, but Kirby does everything I need. Here's a list of a few things I was especially fond of...

### The Editor

I've put the editor as a good thing. It's simplistic and it teaches you to keep HTML out of your editor and that if you really need it, then put it in a template or a snippet.

It's also **very** minimal. It has 4 options (Bold, italic, link, email) and the rest must be done via markdown syntax. I think this is a great idea because it stops users (normal people) from abusing it by adding their own god-awful stylistic choices onto the website. There's nothing worse (as a developer) than spending hours on a site and then the owner of the site logs onto the CMS and decides to change all of the text to 42pt size and bright pink. The minimal aspects of the editor help alleviate those potential problems.

### API

The API to me is very logical. In fact, it was how I started programming my own it until I heard about Kirby. The code samples above show what I mean.

### Flexibility

Since everything is built on templates and snippets, you can actually code a lot of the site yourself to your exact specification. I haven't gone crazy with this. The only real customising I'll be doing is with layout (floats and maybe a sticky header).

### They've used Markdown

Kirby uses the popular Markdown syntax which is present on many other websites such as Github. This means that we don't have to learn yet another language to do a task that should be easy.

## CMS Flaws

### Infancy

Kirby is only a few years old and by the looks of it, is mainly run by one guy. I've had a few instances where the online documentation is lacking and I've had to trawl through the source code myself to see what classes do what. Not ideal, but I understand he's probably working on this as I speak.

### Bugs

There are a few weird bugs that I've encountered. One in particular required me to wrap a coding example in backticks to ensure that the document actually worked. If I didn't wrap it in backticks, the link to that page would come back with 'The connection was reset'...very helpful...

Another one that I still haven't figured out entirely yet was concerning the content of one of my music articles (completely codeless). I trimmed off a few characters from the end of the article, and it magically started working again. 


### Changing things after the fact

There are a few different templates/style of pages that come built into Kirby. These are 'Page' and 'Project'. basically, with a project, you can have multiple pages under one project and then link through to them with a 'next' and 'previous' button (you can change this in the template, this is just default behaviour). A page template is just a static page, nothing fancy.

I created 4 page templates not entirely knowing the difference. Once I learned the difference I went to switch my page to a project template instead and it doesn't have the option. The only solution therefore is to delete the page and create another one correctly named as template. My fault, but still, I feel it could be added as a feature with (fairly) minimal effort.
****
This is only my first week with Kirby so I can't comment too much on all of it yet. Despite the (few) bugs I've encountered, it is definitely a great CMS and allows massive flexibility for anyone (especially developers) looking for a website tailored exactly to them.

I'll be adding more code snippets here over time to demonstrate how Kirby can be used so check back every now and then to see what's new!