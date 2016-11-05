import re as re
file = open('test.txt','r')
pattern = r"((\d+) of (\d+) DOCUMENTS)"
with open('test.txt') as f:
    lines = f.readlines()
count = 1
flag = 0
a=[]
for i in range(len(lines)):
	if re.search(pattern, lines[i]):
		if flag==0:
			flag=1
			a.append(lines[i])
		else:
			filename = "Text " +str(count) +".txt"
			count += 1
			newfile = open(filename,"w")
			for k in a:
				newfile.write(k)
			newfile.close()
			del a[:]
			a.append(lines[i])
	else:
		a.append(lines[i])
		if i==len(lines)-1:
			filename = "Text " +str(count) +".txt"
			newfile = open(filename,"w")
			for j in a:
				newfile.write(j)
			newfile.close()