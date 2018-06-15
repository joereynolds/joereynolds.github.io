---
layout: default
---

I like words, I like lists, I like lists of words!

Below's a list of some free public-domain lists that I would recommend programmers and wordy aficionados to check out.

####(link: wordlists/animals text: animals.txt)
2996 animals, sadly not ordered but that's a (fairly) trivial task. Again, scraped by myself with similar methods to extracting all the pokemon.

####(link: wordlists/countries text: countries.txt)
An alphabetized list of 196 countries from A..Z.

####(link: wordlists/enable1 text: enable1.txt)
The trusty enable1.txt. This seems to be the most common file that will pop up on the internet if you search for a wordlist.

####(link: wordlists/FFVIIMonsters text:FinalFantasyVIIMonsterList.txt)
List of all the monsters (and bosses!) from the great Final Fantasy VII. Something tells me this list of wordlists might need to be better categorized...

####(link: wordlists/planets text: minorplanets.txt)
A list of 19,000 minor planet names, from Aberghaiz to Zyskin!

####(link: wordlists/plantFamilies text: plantFamilies.txt)
Making this list of wordlists has given me a bug for scraping. So I scraped some plant stuff too!
620 families of plants.

####(link: wordlists/plantGenera text: plantGenera.txt)
14,000 + plant genera

####(link: wordlists/pokemon text: Pokemon.txt)
Complete list of all pokemon up to the current series (whatever that is) scraped by yours truly.

Here's the main part of the code :
```
pokemon = $('.wikitable').find('td:nth-child(2)');
$.each($(pokemon), function(){ 
    console.log($(this).find('a').attr('title')); 
});
```
jQuery  is magic, I swear...

####(link: wordlists/RoyalNavyShipNames text: RoyalNavyShipNames.txt)
I made this (link: https://github.com/joereynolds/RoyalNavyShipScraper text: badboy) myself. It's a list of all British navy ships scraped from Wikipedia.

####(link: wordlists/Synonyms text: Synonyms.txt)
I found this backed up on a hard-drive from a while ago, I'm completely unaware of its origins.
I have no idea what it is but looking at it, it looks like a list of words in the following scheme:

**Word : Classification**

Could be useful to some people?

####(link: wordlists/wordlist text: Wordlist.txt)
This originated from the AutoHotKey community and basically serves as a much bigger enable1.txt
