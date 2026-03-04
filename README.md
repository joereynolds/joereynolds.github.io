# joereynolds.github.io

The source for joereynoldsaudio.com

To start it locally, use the Jekyll docker containers:

```
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

It's then available on localhost port 4000.


## How it works

Internal notes for myself...

Images are populated via my Dropbox. Create a "site" directory for any climbing stuff and then run the compress images script to compress and create thumbnails. Then, run the fetch images script to populate the site with them.
