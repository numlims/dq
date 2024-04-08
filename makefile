all: qp.py # readme.md
qp.py: qp.ct
	# syncnv qp.org qp.ct orgtoct cttoorg
	./ct/ct qp.ct
