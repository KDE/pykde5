import sys,DLFCN
# This is needed to ensure that dynamic_cast and RTTI works inside kdelibs.
sys.setdlopenflags(DLFCN.RTLD_NOW|DLFCN.RTLD_GLOBAL)
     