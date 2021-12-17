# This file was generated using the following command:
# ./configure --static --static-math=yes --static-fst=yes --use-cuda=no --openblas-root=../tools/OpenBLAS/install

CONFIGURE_VERSION := 11

# Toolchain configuration

CXX = g++
AR = ar
AS = as
RANLIB = ranlib

# Base configuration

DEBUG_LEVEL = 1
DOUBLE_PRECISION = 0
OPENFSTINC = /home/saad/Downloads/gentle-Final/ext/kaldi/tools/openfst-1.6.7/include
OPENFSTLIBS = /home/saad/Downloads/gentle-Final/ext/kaldi/tools/openfst-1.6.7/lib/libfst.a
OPENFSTLDFLAGS = 

CUBROOT = /home/saad/Downloads/gentle-Final/ext/kaldi/tools/cub-1.8.0
WITH_CUDADECODER = 1

OPENBLASINC = /home/saad/Downloads/gentle-Final/ext/kaldi/tools/OpenBLAS/install/include
OPENBLASLIBS = -L/home/saad/Downloads/gentle-Final/ext/kaldi/tools/OpenBLAS/install/lib -l:libopenblas.a -lgfortran

# OpenBLAS specific Linux configuration

ifndef DEBUG_LEVEL
$(error DEBUG_LEVEL not defined.)
endif
ifndef DOUBLE_PRECISION
$(error DOUBLE_PRECISION not defined.)
endif
ifndef OPENFSTINC
$(error OPENFSTINC not defined.)
endif
ifndef OPENFSTLIBS
$(error OPENFSTLIBS not defined.)
endif
ifndef OPENBLASINC
$(error OPENBLASINC not defined.)
endif
ifndef OPENBLASLIBS
$(error OPENBLASLIBS not defined.)
endif

CXXFLAGS = -std=c++11 -I.. -isystem $(OPENFSTINC) -O1 $(EXTRA_CXXFLAGS) \
           -Wall -Wno-sign-compare -Wno-unused-local-typedefs \
           -Wno-deprecated-declarations -Winit-self \
           -DKALDI_DOUBLEPRECISION=$(DOUBLE_PRECISION) \
           -DHAVE_EXECINFO_H=1 -DHAVE_CXXABI_H -DHAVE_OPENBLAS -I$(OPENBLASINC) \
           -msse -msse2 -pthread \
           -g

ifeq ($(KALDI_FLAVOR), dynamic)
CXXFLAGS += -fPIC
endif

ifeq ($(DEBUG_LEVEL), 0)
CXXFLAGS += -DNDEBUG
endif
ifeq ($(DEBUG_LEVEL), 2)
CXXFLAGS += -O0 -DKALDI_PARANOID
endif

# Compiler specific flags
COMPILER = $(shell $(CXX) -v 2>&1)
ifeq ($(findstring clang,$(COMPILER)),clang)
# Suppress annoying clang warnings that are perfectly valid per spec.
CXXFLAGS += -Wno-mismatched-tags
endif

LDFLAGS = $(EXTRA_LDFLAGS) $(OPENFSTLDFLAGS) -rdynamic
LDLIBS = $(EXTRA_LDLIBS) $(OPENFSTLIBS) $(OPENBLASLIBS) -lm -lpthread -ldl

# Environment configuration

CXXFLAGS += -DKALDI_NO_EXPF
