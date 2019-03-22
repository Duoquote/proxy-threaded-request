import requests, threading, os, time, queue, json
requests.packages.urllib3.disable_warnings()
from pprint import pprint
if not os.path.exists("px.json"):
	pxx = requests.get("https://www.proxy-list.download/api/v1/get?type=http").text.split("\r\n")[:-1]
	proxxies = {"blacklist": [], "proxies": pxx}
	with open("px.json", "w") as f:
		f.write(json.dumps(proxxies))
testqueue = queue.Queue()
urlqueue = queue.Queue()
pxsend = queue.Queue()
pxget = queue.Queue()
dumpq = []
netstate = True
header = False
pformat = "X> [{}]: {: ^14} > {}"
donelist = []

def done():
	with open("donelist.json", "w") as f:
		f.write(json.dumps(donelist))
def xprint(node, name, value):
	print(pformat.format(node, name, value))
	
class statsUpdater(threading.Thread):
	def __init__(self):
		threading.Thread.__init__()

def netCheck():
	while True:
		done()
		last = time.time()
		try:
			req = requests.get("http://example.com", timeout=5)
			netstate = True
		except:
			netstate = False
		current = time.time()
		if current - last <= 5:
			time.sleep(last - current + 5)
ncheck = threading.Thread(target=netCheck)
ncheck.start()
def proxyCheck(proxy):
	try:
		req = requests.get("http://example.com", proxies={"HTTP": proxy}, verify=False, timeout=5)
		if req.status_code == 200:
			xprint("PCheck <{}>".format(proxy), "PXStatus", "Working")
			return True
		else:
			xprint("PCheck <{}>".format(proxy), "PXStatus", "Not working")
			return False
	except:
		xprint("PCheck <{}>".format(proxy), "PXStatus", "Internet Connection Error (Probably)")
		return False
class pxh(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, target=self.send)
		self.start()
	def send(self):
		while True:
			if not pxsend.empty():
				proxy = pxsend.get()
				if proxy:
					pxHandler.tempblack.append(proxy)
					testqueue.put(proxy)
					del pxHandler.active[pxHandler.active.index(proxy)]
				else:
					for i in pxHandler.pxlist["proxies"]:
						if i not in pxHandler.pxlist["blacklist"] and i not in pxHandler.active and i not in pxHandler.tempblack:
							pxget.put(i)
							pxHandler.active.append(i)
							break

class px(threading.Thread):
	def __init__(self):
		with open("px.json") as f:
			self.pxlist = json.loads(f.read())
		xprint("PThread", "PXList", "Loaded")
		self.active = []
		self.tempblack = []
		threading.Thread.__init__(self, target=self.proxyTest)
		self.start()
		xprint("PThread", "PXThread", "Started")

	def update(self):
		with open("px.json", "w") as f:
			f.write(json.dumps(self.pxlist))
		with open("px.json") as f:
			self.pxlist = json.loads(f.read())
		xprint("PThread", "PXList", "Updated")

	def proxyTest(self):
		while True:
			last = time.time()
			if not testqueue.empty():
				if netstate:
					proxy = testqueue.get()
					state = proxyCheck(proxy)
					if state == False:
						self.pxlist["blacklist"].append(proxy)
						self.update()
						del self.tempblack[self.tempblack.index(proxy)]
						xprint("PThread", "PXList", "Blacklisted: <{: ^15}>".format(proxy))
					else:
						del self.tempblack[self.tempblack.index(proxy)]
			current = time.time()
			if current - last <= 3:
				time.sleep(last - current + 3)
pxHandler = px()
pxSecond = pxh()
def getData(url, proxy=False):
	if proxy:
		px = {"HTTP": proxy}
	else:
		px = False
	try:
		data = requests.get(url, headers=header, proxies=px, verify=False, timeout=15)
		if data.status_code == 200:
			return data.content
		else:
			return False
	except:
		return False
class rqThread(threading.Thread):
	def __init__(self, index):
		threading.Thread.__init__(self, target=self.main)
		pxsend.put(False)
		self.index = index
		self.px = pxget.get(block=True)
		xprint("RQThread <{:0>4}>".format(self.index), "PXGet", "Attached Proxy: {}".format(self.px))
		self.start()
		xprint("RQThread <{:0>4}>".format(self.index), "RQTStatus", "Started")
	def main(self):
		while True:
			last = time.time()
			if not urlqueue.empty():
				self.url = urlqueue.get()
				data = getData(self.url[0], self.px)
				if data:
					if "/" in self.url[1]:
						if not os.path.exists(self.url[1].rsplit("/", 1)[0]):
							try:
								os.makedirs(self.url[1].rsplit("/", 1)[0])
							except:
								pass
					with open(self.url[1], "wb") as f:
						f.write(data)
				else:
					time.sleep(5)
					if netstate:
						pxsend.put(self.px)
						self.px = pxget.get(block=True)
						xprint("RQThread <{:0>4}>".format(self.index), "PXGet", "Attached Proxy: {}".format(self.px))
					urlqueue.put(self.url)
			current = time.time()
			if current - last <= 7:
				time.sleep(last - current + 7)

rqTList = {}
for i in range(10):
	rqTList["thread-"+str(i)] = rqThread(i)
xprint("Log", "ProxyHandler", pxHandler)
xprint("Log", "NetCheck", ncheck)