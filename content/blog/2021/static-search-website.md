+++
author = "Toni Sagrista Selles"
categories = ["Website"]
tags = [ "website", "design", "programming", "javascript", "search"]
date = 2021-03-29
linktitle = ""
title = "Static search for your website"
featuredpath = "date"
type = "post"
+++

Search functionality in a small website like mine is usually arguably useless. I, for once, never even care to check whether a specific website offers it. I find a post that interests me via a search engine or aggregator, navigate to the page, read the post and then leave. However, I am not against local, serverless indexing and searching, even though most search engines [provide site-specific searches](https://help.duckduckgo.com/duckduckgo-help-pages/results/syntax/). That is why I moved the search function of this website to a local, JavaScript-based implementation. How to do it? Read on.

<!--more-->

## The method

I have been looking up different methods to include a static search into my site. Now, my site is statically generated from a bunch of source files using Hugo[^hugo], and in their very website they list a handful of resources to help you [implement a static search into a Hugo website](https://gohugo.io/tools/search). I have tried many and none of them worked well, or at all. Some are outdated, and some others are incomplete or imprecise. So I implemented a method which borrows bits and pieces from others and actually works. The method uses the JavaScript search library `lunr.js`[^lunr] and Hugo's JSON output, and it requires three simple steps:

1.  Generate an index for your site. In my case, I enable JSON output in the Hugo configuration, and manipulate the format with a special template.
2.  Use a JavaScript search library (`lunr.js`) to perform the search locally in the user's browser using the provided JSON index.
3.  Done! Really.

The advantages of this offline, local method are manifold:

-  It is **privacy-respecting**, as no data is sent at any time to external search engines, avoiding trackers.
-  **Fast**! Everything happens locally. No server-side communication required.
-  Works with any static site, and **can be deployed anywhere** (GitHub/GitLab pages for instance).
-  It is fun to implement ;)

It also has some downsides:

-  Since it is an offline search method, it is the user's computer the one in charge of actually searching, consuming a few resources (probably negligible).
-  It needs JavaScript. Some users choose to disable it altogether due to privacy and security concerns.
-  You actually need to do some plumbing instead of just adding an iframe to your site.

As always, the devil is in the details, so let's see how to do it.

## Generating the website index

Since we want to perform the search offline without external servers involved, everything must happen in the client's browser with the aid of JavaScript. We will generate an index file containing the website's content that we can later easily parse. This index file will be requested from the server whenever the user starts using the search functionality. Ideally, the index should not be large, but that's gonna depend on how much content you want to index. More on the size of the index at the bottom of this section.

Since I'm using Hugo, I can directly activate the JSON output and have it generate the index automatically. First, activate the output in your `config.toml`.

{{< highlight toml "linenos=table" >}}
[outputs]
    home = ["HTML", "RSS", "JSON"]
{{</ highlight >}}

We want to control the name and content of the fields in the JSON index file, so let's create a new template in `layouts/_default/index.json` (in Hugo) with the following content.

{{< highlight json "linenos=table" >}}
{{- $.Scratch.Add "index" slice -}}
{{- range .Site.RegularPages -}}
    {{- $.Scratch.Add "index" (dict "title" .Title "tags" .Params.tags "categories" .Params.categories "content" .Plain "href" .Permalink) -}}
{{- end -}}
{{- $.Scratch.Get "index" | jsonify -}}
{{</ highlight >}}

We'll have an entry in the index for every blog post and for eacy static page. Our JSON index will contain, for each entry, the tile under the name `"title"`, the tags under the name `"tags"`, the categories under `"categories"`, the full content under `"content"` and the link to the item under `"href"`. We will use these tags later when we set up the search library.

Here is an example of a chunk of the index of my site. I have left out the contents because they take up too much space.

{{< highlight json "linenos=table" >}}
[
    [...]
  {
    "categories": [
      "RaspberryPi"
    ],
    "content": "[...]",
    "href": "/blog/2021/raspberry-pi-4-first-impressions/",
    "tags": [
      "sbc",
      "raspberrypi"
    ],
    "title": "Raspberry Pi 4: First impressions"
  },
  {
    "categories": [
      "Gaia Sky"
    ],
    "content": "[...]",
    "href": "/blog/2021/gaiasky-3-tutorial/",
    "tags": [
      "programming",
      "opengl",
      "release",
      "version",
      "english",
      "tutorial"
    ],
    "title": "Gaia Sky 3 tutorial for complete beginners"
  },
    [...]
{{</ highlight >}}

The [index file in my site](/index.json) weighs **less than 300K**, which is not too bad to download with even slower connections. Especially when the trade-off is not using external services that may track your every movement.

This concludes the index creation. Let's see how to use it.

## Implementing the actual search 

Now, onto the actual search. We will serve it with a new page which is accessible under `/search` and contains only a text input. The results are generated and included under the search box on the fly via JavaScript.

Create a new page in `content/search/index.md` (in Hugo) with the following contents:

{{< highlight html "linenos=table" >}}
+++
title = "Search"
description = "Client-side search. No external servers involved."
weight = -170
+++

<p>
<input id="search" type="text" placeholder="Enter your search query here">
</p>

<ul id="results"></ul>

<script src="/js/jquery.min.js"></script>
<script src="/js/lunr.js"></script>
<script>
  [JAVASCRIPT GOES HERE!]
</script>
{{</ highlight >}}

As you can see, I have skipped the actual JavaScript code which uses `lunr.js` to implement the search. Also, notice that you need to download the `lunr.js` library and load it in your page, as well as `jquery.js`. I usually serve all libraries from my own site to avoid external tracking.
The unordered list `<ul id="results" />` is the element that we'll populate via JavaScript with the search results. The `<input id="search" type="text" />` is the search box that sits at the top of the page.

The JavaScript follows. Put it in place of the placeholder `[JAVASCRIPT GOES HERE!]` in the above HTML page or put it in its own file (i.e. `search.js`) and load it in the page below `lunr.js`. The JavaScript is an adapted version of the one found in [this post](https://www.integralist.co.uk/posts/static-search-with-lunr/).

{{< highlight javascript "linenos=table" >}}
var lunrIndex,
    $results,
    documents;

function initLunr() {
  // retrieve the index file
  $.getJSON("/index.json")
    .done(function(index) {
        documents = index;

        lunrIndex = lunr(function(){
          this.ref('href')
          this.field('content')

          this.field("title", {
              boost: 10
          });
          this.field("tags", {
              boost: 5
          });
          documents.forEach(function(doc) {
            try {
              this.add(doc)
            } catch (e) {}
          }, this)
        })
    })
    .fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.error("Error getting Lunr index file:", err);
    });
}

function search(query) {
  return lunrIndex.search(query).map(function(result) {
    return documents.filter(function(page) {
      try {
        console.log(page)
        return page.href === result.ref;
      } catch (e) {
        console.log('whoops')
      }
    })[0];
  });
}

function renderResults(results) {
  if (!results.length) {
    return;
  }

  // show first ten results
  results.slice(0, 10).forEach(function(result) {
    var $result = $("<li>");

    $result.append($("<a>", {
      href: result.href,
      text: "» " + result.title
    }));

    $results.append($result);
  });
}

function initUI() {
  $results = $("#results");

  $("#search").keyup(function(){
    // empty previous results
    $results.empty();

    // trigger search when at least two chars provided.
    var query = $(this).val();
    if (query.length < 2) {
      return;
    }

    var results = search(query);

    renderResults(results);
  });
}

initLunr();

$(document).ready(function(){
  initUI();
});
{{</ highlight >}}

This is the last piece of the puzzle, and that's pretty much it. If you have set up everything correctly, your search should work. You can see a working example of it all here: [**Static search page**](/search).

## Conclusion

In this post we have seen a simple way to add a privacy-respecting offline search functionality to a statically-generated website. The search method is based on a pre-generated JSON index file which are parsed using `lunr.js` and a few lines of JavaScript code that run on the browser.

```
this code block
does not 
have a
language set
```

[^hugo]: Hugo is a popular static site generator: https://gohugo.io
[^lunr]: `lunr.js` is a JavaScript search library https://lunrjs.com

