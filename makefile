all: dq.py # readme.md
dq.py: dq.ct
	# tie dq.org dq.ct orgtoct cttoorg
	./ct/ct dq.ct
