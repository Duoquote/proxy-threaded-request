### Threaded Proxy Requester Rev.2

With this program, you can either use your own proxies or let it download a proxy list from some source and then specify the thread amount and each thread will send a get request to the url that you provide and will have it's own proxy.

The old code may not work properly and it also is not perfected, there are a lot junk code in there and I did not implemented many error handlings, things can go wrong but I need to say that I tested it with 1000 threads with 1000 proxy addresses scraped data without crashing or something. Also I need to mention that, I didn't add many flexibility like, you can't do some things without touching the source code a lot.

I made this program to easily scrape data.

### How to use it?

You can start by importing my program into your script.

```python
import proxy, json
```

The number inside the call statement defines how many threads are going to be created.
For demonstration purposes I assigned the 'Main' class to tProxy variable in the code below.

```python
tProxy = proxy.Main(5)
```

If you want to set the headers you can either define tProxy.headers like below.

```python
tProxy.headers = {
	"Origin": "http://some-domain.extension",
	"Referer": "http://some-domain.extension"
}
```

Or if you want to specify per url headers, you can pass it with a fourth parameter in the url list like:

```python
urs = [
	["http://some-domain.extension", "html", "test/test.html"],
	["http://some-domain.extension", "html", "test/asdasd.html", {
		"Origin": "http://some-domain.extension",
		"Referer": "http://some-domain.extension"
	}],
	["http://some-domain.extension", "html", "test/testzxc.html"],
	["http://some-domain.extension", "html", "test/testfqwe.html"],
	["http://some-domain.extension", "html", "test/testasd.html"]
]
```

Then just iterate through and watch the magic happen.

```python
for i in urs:
	tProxy.urlQueue.put(i)
```

### TO-DOs

- The logging part itself is ready but need to add what to log.

- Testings are not done yet, will test.

- Add post request capability.

### Functionalities

- Auto blacklist if a proxy dies and sends a new proxy to it from the proxy list.

- Auto check whether a proxy died or the internet connection is available.

- Auto save the data.

### Disclaimer

I only publish the code here and how you are going to use it is left to your own discretion.
