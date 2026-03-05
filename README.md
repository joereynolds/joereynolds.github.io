# joereynolds.github.io

The source for joereynoldsaudio.com

To start it locally, use the Jekyll docker containers:

```
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

It's then available on localhost port 4000.


## How it works

Internal notes for myself...

Images are slurped up from Dropbox.
There's a workflow that runs weekly in here (or you can run it manually) that will sync all of our website images from dropbox. 

I prefer keeping all my images in one place (Dropbox). We sync it down to this repo for speed reasons. Dropbox isn't a CDN and is dog slow.

The process is

- Create a "site" directory for the climb you care about in dropbox
- Run the `compress_images` script on your machine
  - This will compress the images contained in the "site" directory and
    generate thumbnails
- Trigger the workflow
  - This will pull down all thumbnails and compressed images into here
