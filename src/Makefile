#

JADE = 

OUTPUT  := ../bin

DIRS = dynamics electronic sampling sampling2

.PHONY: all clean distclean install $(DIRS) 

all: $(DIRS)
install: $(DIRS)
clean: $(DIRS) 

$(DIRS): 
	$(MAKE) -j2 -C $@ $(MAKECMDGOALS) 

