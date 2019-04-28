import proxy, json

# The numner inside the call statement defines how many threads are going to be
# created.

tProxy = proxy.Main(5)

# If you want to set the headers you can either define tProxy.headers like
# below.

tProxy.headers = {
	"Origin": "http://some-domain.extension",
	"Referer": "http://some-domain.extension"
}

# Or if you want to specify per url headers, you can pass it with a fourth
# parameter in the url list like:

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

for i in urs:
	tProxy.urlQueue.put(i)
