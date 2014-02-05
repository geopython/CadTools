
UI_FILES = tools/ui_arcintersection.py tools/ui_orthogonaltraverse.py tools/ui_rotateobject.py tools/ui_cadconsole.py tools/ui_parallelline.py tools/ui_showazimuth.py tools/ui_cadtoolssettings.py  tools/ui_rectangularpoints.py

default: compile

compile: resources.py $(UI_FILES)

resources.py : resources.qrc
	pyrcc4 -o resources.py resources.qrc

ui_%.py : %.ui
	pyuic4 -o $@ $<

