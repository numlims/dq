all: dq.py # readme.md
dq.py: dq.ct
	# syncnv dq.org dq.ct orgtoct cttoorg
	./ct/ct dq.ct
#readme.md: dq.ct
#	cttomd dq.ct > readme.md
