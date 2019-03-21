import proxy, json

urs = ""

with open("examplelist.json") as f:
	urs = json.loads(f.read())

for i in urs:
	proxy.urlqueue.put(i)

startlen = len(urs)

def status():
	print("{:>10}/{}".format(startlen - proxy.urlqueue.qsize(), startlen))

while True:
	try:
		d = input()
		if d == "status":
			status()
		else:
			pass
	except:
		pass