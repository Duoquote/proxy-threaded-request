### Threaded Proxy Requester

With this program, you can either use your own proxies or let it download a proxy list from other source and then specify the thread amount and each thread will send a get request to the url you provide and each thread will have it's own proxy url. The program in the current state may not work properly and it also is not perfected, there are a lot junk code in there and I did not implemented many error handlings, things can go wrong but I need to say that I tested it with 1000 threads with 1000 proxy addresses scraped data without crashing or something. Also I need to mention that, I didn't add many flexibility like, you can't do some things without touching the source code a lot.

I made this program to easily scrape data.

### How to use it?

You need to prepare a url list to send request and save the data. The list should be in a format like this:
[
	["http://url-to-download.domain", "location/of/data/name0.extension"],
	["http://url-to-download.domain", "location/of/data/name1.extension"],
	["http://url-to-download.domain", "location/of/data/name2.extension"],
	["http://url-to-download.domain", "location/of/data/name3.extension"]
]

Firstly you need to import my script into your python project or if you know what you do, then you feed the url list into urlqueue object.

Then you need to iterate the url list and send every [url, location] nested lists into proxy.urlqueue like:

proxy.urlqueue.put(["http://url-to-download.domain", "location/of/data/name3.extension"]).

As you add the urls it will automatically download and save the data.

### Functionalities

- Auto blacklist if a proxy dies and sends a new proxy to it from the proxy list.

- Auto check whetther a proxy died or the internet is available.

- Auto save the data.

### Disclaimer

I only publish the code here and how you are going to use it is left to your own discretion.