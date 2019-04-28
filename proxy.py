import requests, threading, os, time, queue, json, socket
from datetime import datetime

socket.setdefaulttimeout(3)

netStatus = True

def getData(url, headers=False, proxy=False):
	if proxy:
		proxy = {"HTTP": proxy}
	tryCount = 0
	error = False
	while True:
		try:
			if netStatus:
				data = requests.get(url, headers=headers, proxies=proxy, verify=False, timeout=15)
			else:
				time.sleep(5)
				continue
		except:
			tryCount += 1
			if tryCount == 5:
				error = True
				break
			time.sleep(5)
			continue
		if data.status_code == 200:
			break
		else:
			tryCount += 1
			if tryCount == 5:
				error = True
				break
			time.sleep(5)
			continue
	if error:
		return {"status": 0}
	else:
		return {"status": 1, "data": data}

class Descriptor(threading.Thread):
	def __init__(self):
		try:
			if os.path.exists("log.txt"):
				timestamp = datetime.fromtimestamp(int(os.stat("log.txt").st_ctime))
				os.rename("log.txt", "log-"+datetime.strftime(timestamp, "%Y-%m-%dT%H-%M-%S")+".txt")
		except:
			timestamp = datetime.fromtimestamp(int(os.stat("log.txt").st_ctime))
			os.rename("log.txt", "log-"+datetime.strftime(timestamp, "%Y-%m-%dT%H-%M-%S")+".txt")
		self.saveQueue = queue.Queue()
		self.options = {
			"log": True,
			"print": True
			}
		threading.Thread.__init__(self, target=self.run)
	def run(self):
		while True:
			if not self.saveQueue.empty():
				processData = self.saveQueue.get()
				if self.options["log"]:
					with open("log.txt", "w") as f:
						f.write(processData)
				if self.options["print"]:
					print(processData["data"])
			else:
				time.sleep(1)

class Proxy(threading.Thread):
	def __init__(self):
		if not os.path.exists("px.json"):
			proxies = getData("https://www.proxy-list.download/api/v1/get?type=http")["data"].text.split("\r\n")[:-1]
			self.proxies = {"blacklist": [], "proxies": proxies}
			with open("px.json", "w") as f:
				f.write(json.dumps(self.proxies))
		else:
			with open("px.json", "r") as f:
				self.proxies = json.loads(f.read())
		self.active = []
		self.renewQueue = queue.Queue()
		self.waitQueue = queue.Queue()
		threading.Thread(target=self.netTest)
		threading.Thread.__init__(self, target=self.run)
	def run(self):
		while True:
			if not self.renewQueue.empty():
				proxy = self.renewQueue.get()
				if not self.test(proxy):
					self.proxies["blacklist"].append(proxy)
					with open("px.json") as f:
						f.write(json.dumps(self.proxies))
				if proxy in self.active:
					del self.active[self.active.index(proxy)]
				for px in self.proxies:
					if px not in self.proxies["blacklist"] and px not in self.active:
						self.waitQueue.put(px)
						break
			else:
				time.sleep(1)
	def netTest(self):
		while True:
			try:
				socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
				netStatus = True
			except:
				netStatus = False
			time.sleep(3)
	def test(self, proxy):
		try:
			socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((proxy[0], int(proxy[1])))
			return True
		except:
			return False


class Main:
	def __init__(self, threadCount, headers=False, log=True, print=True):
		self.descriptor = Descriptor()
		self.descriptor.options["log"] = log
		self.descriptor.options["print"] = print
		self.descriptor.start()
		self.proxy = Proxy().start()
		self.threads = {}
		self.urlQueue = queue.Queue()
		self.headers = headers
		for t in range(threadCount):
			self.threads[t] = threading.Thread(target=self.Thread).start()
	def Thread(self):
		while True:
			if not self.urlQueue.empty():
				data = self.urlQueue.get()
				if len(data) > 3:
					headers = data[-1]
				else:
					headers = self.headers
				while True:
					result = getData(data[0], headers=headers)
					if result["status"] == 1:
						path = data[2].replace("\\", "/").rsplit("/", 1)[0]
						if not os.path.exists(path):
							os.makedirs(path)
						if data[1] == "json":
							write = result["data"].json()
						else:
							write = result["data"].text
						with open(data[2], "w") as f:
							f.write(write)
						break
			else:
				time.sleep(1)

# Old code below, may delete it in future updates, actually I may have found
# the problem that is causing 100% cpu usage but I had the time to rewrite
# everyting and didn't even tried to fix the problem. If you want to use the
# code below, to prevent 100% cpu usage you should put an else statement where
# the queue checks happen, like 'if not someQueue.empty()' and make the
# thread/code wait for a little time to make it not to check the queues in every
# time that it can possibly check. My guess is it will be ok if queues are full
# without the edits.

# if not os.path.exists("px.json"):
# 	pxx = requests.get("https://www.proxy-list.download/api/v1/get?type=http").text.split("\r\n")[:-1]
# 	proxxies = {"blacklist": [], "proxies": pxx}
# 	with open("px.json", "w") as f:
# 		f.write(json.dumps(proxxies))
# testqueue = queue.Queue()
# urlqueue = queue.Queue()
# pxsend = queue.Queue()
# pxget = queue.Queue()
# dumpq = []
# netstate = True
# header = False
# pformat = "X> [{}]: {: ^14} > {}"
# donelist = []
#
# def done():
# 	with open("donelist.json", "w") as f:
# 		f.write(json.dumps(donelist))
# def xprint(node, name, value):
# 	print(pformat.format(node, name, value))
#
# class statsUpdater(threading.Thread):
# 	def __init__(self):
# 		threading.Thread.__init__()
#
# def netCheck():
# 	while True:
# 		done()
# 		last = time.time()
# 		try:
# 			req = requests.get("http://example.com", timeout=5)
# 			netstate = True
# 		except:
# 			netstate = False
# 		current = time.time()
# 		if current - last <= 5:
# 			time.sleep(last - current + 5)
# ncheck = threading.Thread(target=netCheck)
# ncheck.start()
# def proxyCheck(proxy):
# 	try:
# 		req = requests.get("http://example.com", proxies={"HTTP": proxy}, verify=False, timeout=5)
# 		if req.status_code == 200:
# 			xprint("PCheck <{}>".format(proxy), "PXStatus", "Working")
# 			return True
# 		else:
# 			xprint("PCheck <{}>".format(proxy), "PXStatus", "Not working")
# 			return False
# 	except:
# 		xprint("PCheck <{}>".format(proxy), "PXStatus", "Internet Connection Error (Probably)")
# 		return False
# class pxh(threading.Thread):
# 	def __init__(self):
# 		threading.Thread.__init__(self, target=self.send)
# 		self.start()
# 	def send(self):
# 		while True:
# 			if not pxsend.empty():
# 				proxy = pxsend.get()
# 				if proxy:
# 					pxHandler.tempblack.append(proxy)
# 					testqueue.put(proxy)
# 					del pxHandler.active[pxHandler.active.index(proxy)]
# 				else:
# 					for i in pxHandler.pxlist["proxies"]:
# 						if i not in pxHandler.pxlist["blacklist"] and i not in pxHandler.active and i not in pxHandler.tempblack:
# 							pxget.put(i)
# 							pxHandler.active.append(i)
# 							break
#
# class px(threading.Thread):
# 	def __init__(self):
# 		with open("px.json") as f:
# 			self.pxlist = json.loads(f.read())
# 		xprint("PThread", "PXList", "Loaded")
# 		self.active = []
# 		self.tempblack = []
# 		threading.Thread.__init__(self, target=self.proxyTest)
# 		self.start()
# 		xprint("PThread", "PXThread", "Started")
#
# 	def update(self):
# 		with open("px.json", "w") as f:
# 			f.write(json.dumps(self.pxlist))
# 		with open("px.json") as f:
# 			self.pxlist = json.loads(f.read())
# 		xprint("PThread", "PXList", "Updated")
#
# 	def proxyTest(self):
# 		while True:
# 			last = time.time()
# 			if not testqueue.empty():
# 				if netstate:
# 					proxy = testqueue.get()
# 					state = proxyCheck(proxy)
# 					if state == False:
# 						self.pxlist["blacklist"].append(proxy)
# 						self.update()
# 						del self.tempblack[self.tempblack.index(proxy)]
# 						xprint("PThread", "PXList", "Blacklisted: <{: ^15}>".format(proxy))
# 					else:
# 						del self.tempblack[self.tempblack.index(proxy)]
# 			current = time.time()
# 			if current - last <= 3:
# 				time.sleep(last - current + 3)
# pxHandler = px()
# pxSecond = pxh()
# def getData(url, proxy=False):
# 	if proxy:
# 		px = {"HTTP": proxy}
# 	else:
# 		px = False
# 	try:
# 		data = requests.get(url, headers=header, proxies=px, verify=False, timeout=15)
# 		if data.status_code == 200:
# 			return data.content
# 		else:
# 			return False
# 	except:
# 		return False
# class rqThread(threading.Thread):
# 	def __init__(self, index):
# 		threading.Thread.__init__(self, target=self.main)
# 		pxsend.put(False)
# 		self.index = index
# 		self.px = pxget.get(block=True)
# 		xprint("RQThread <{:0>4}>".format(self.index), "PXGet", "Attached Proxy: {}".format(self.px))
# 		self.start()
# 		xprint("RQThread <{:0>4}>".format(self.index), "RQTStatus", "Started")
# 	def main(self):
# 		while True:
# 			last = time.time()
# 			if not urlqueue.empty():
# 				self.url = urlqueue.get()
# 				data = getData(self.url[0], self.px)
# 				if data:
# 					if "/" in self.url[1]:
# 						if not os.path.exists(self.url[1].rsplit("/", 1)[0]):
# 							try:
# 								os.makedirs(self.url[1].rsplit("/", 1)[0])
# 							except:
# 								pass
# 					with open(self.url[1], "wb") as f:
# 						f.write(data)
# 				else:
# 					time.sleep(5)
# 					if netstate:
# 						pxsend.put(self.px)
# 						self.px = pxget.get(block=True)
# 						xprint("RQThread <{:0>4}>".format(self.index), "PXGet", "Attached Proxy: {}".format(self.px))
# 					urlqueue.put(self.url)
# 			current = time.time()
# 			if current - last <= 7:
# 				time.sleep(last - current + 7)
#
# rqTList = {}
# for i in range(10):
# 	rqTList["thread-"+str(i)] = rqThread(i)
# xprint("Log", "ProxyHandler", pxHandler)
# xprint("Log", "NetCheck", ncheck)
