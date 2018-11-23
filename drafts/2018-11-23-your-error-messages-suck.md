This morning I updated a plugin for my Vim config and I'm a keen bean so I like
to look at the diffs of what's changed, this was one of the commits.

```
commit c1ea19aa215ca211eb06717443e3457491a1375e
Author: Shougo Matsushita <Shougo.Matsu@gmail.com>
Date:   Fri Nov 23 16:21:26 2018 +0900

    Improve except

diff --git a/rplugin/python3/deoplete/logger.py b/rplugin/python3/deoplete/logger.py
index 3cb8370..59127df 100644
--- a/rplugin/python3/deoplete/logger.py
+++ b/rplugin/python3/deoplete/logger.py
@@ -49,9 +49,7 @@ def setup(vim, level, output_file=None):
             import pkg_resources
 
             pynvim_version = pkg_resources.get_distribution('pynvim').version
-        except ImportError:
-            pynvim_version = 'unknown'
-        except pkg_resources.DistributionNotFound:
+        except Exception:
             pynvim_version = 'unknown'
 
         log = getLogger('logging')
```

Sadly this is all too common at where I work, I didn't know it stretched out
elsewhere but apparently it does :(

Here are a few more examples


screenshot this http://stash.sykescottages.co.uk/projects/HYP/repos/hyperion/pull-requests/2057/overview

## What's The Problem

**They've replaced two (potentially) specific errors with one very generic
`Exception.`**

In any case this is the opposite of how I'd work, if a new abnormal situation
occurs, I'd like a specific exception to be thrown so we can handle it
correctly.

All they've done here is mask every future error with the string 'unknown'




## What's The Solution

In my eyes (correct me if I'm wrong) I would:

- Keep those two previous errors, `ImportError` and `DistributionNotFound`
- Add the generic `Exception` on top of the other two (not replace them)
- Give better messages and include the exception's message.

We go from this:

```

```

To this:

```

```



# TODO

The PR doesn't actually change the message, it changes the pynvim version, still
it should alert or something anyway
