include ../rocksdb-for-partial-compaction-analysis/make_config.mk

ifndef DISABLE_JEMALLOC
	ifdef JEMALLOC
		PLATFORM_CXXFLAGS += -DROCKSDB_JEMALLOC -DJEMALLOC_NO_DEMANGLE
	endif
	EXEC_LDFLAGS := $(JEMALLOC_LIB) $(EXEC_LDFLAGS) -lpthread
	PLATFORM_CXXFLAGS += $(JEMALLOC_INCLUDE)
endif

ifneq ($(USE_RTTI), 1)
	CXXFLAGS += -fno-rtti
endif

# CXXFLAGS += -lstdc++fs

CFLAGS += -Wstrict-prototypes

rocksdb_dir = ../rocksdb-for-partial-compaction-analysis

.PHONY: clean librocksdb

all: simple_runner

simple_runner: librocksdb simple_runner.cc
	$(CXX) $(CXXFLAGS) $@.cc -o$@ $(rocksdb_dir)/librocksdb.a -I$(rocksdb_dir)/include -I$(rocksdb_dir) -O2 -std=c++17 $(PLATFORM_LDFLAGS) $(PLATFORM_CXXFLAGS) $(EXEC_LDFLAGS) -lstdc++fs

clean:
	rm -rf ./simple_runner

librocksdb:
	cd $(rocksdb_dir) && $(MAKE) static_lib

tools:
	g++ -o check_finish_enumeration check_finish_enumeration.cpp -std=c++17
	g++ -o count_workload count_workload.cpp -std=c++17
	cd ../K-V-Workload-Generator && $(MAKE)
	cp ../K-V-Workload-Generator/load_gen .

new_strategy_test: librocksdb new_strategy_test.cc
	$(CXX) $(CXXFLAGS) -g $@.cc -o$@ ../librocksdb.a -I../include -I.. -O2 -std=c++17 $(PLATFORM_LDFLAGS) $(PLATFORM_CXXFLAGS) $(EXEC_LDFLAGS)
