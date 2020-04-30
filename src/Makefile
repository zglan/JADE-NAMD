#

JADE = 

#DIRS := `find -maxdepth 1 -type d | sed "/bin/d;/sample2/d" | sed "1d" | sed "s/.\///g"`

OUTPUT  := ../bin

DIRS = dynamics ci_overlap sampling sampling2

.PHONY: all clean distclean install $(DIRS) 

all: $(DIRS)
install: $(DIRS)
clean: $(DIRS) 

$(DIRS): 
	$(MAKE) -j2 -C $@ $(MAKECMDGOALS) 

