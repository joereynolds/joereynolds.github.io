Title: Webpage crashing on iOS

----

Text: 

I've recently been using (link:http://flowtime-js.marcolago.com/ text:flowtime.js) on a project and it would die on iPad and iPhones on both Chrome and Safari. After a **lot** of digging. I found out that it was the 'webkit' property.

In particular, (link:http://blogs.adobe.com/webplatform/2014/03/18/css-animations-and-transitions-performance/ text:transitions) absolutely destroy memory usage with iOS devices. The simplest fix was to remove any '-webkit-' rules in the CSS and boom, we're in business. Obviously, it's not as shiny and impressive as it was now that we've removed transition effects, but it's better than not being visible at all.

Hopefully this tip will save you the days it took me to find the answer.


## Read More

(link: https://github.com/woothemes/FlexSlider/issues/727 text: FlexSlider Issues)
(link: http://stackoverflow.com/questions/15987787/my-website-crashes-safari-both-desktop-and-ios-consistently text: Safari crashes on iOS and desktop)
(link: https://wordpress.org/support/topic/page-on-site-crashes-when-trying-to-view-on-ipad text: Site crashes on iPad)
