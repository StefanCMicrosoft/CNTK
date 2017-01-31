#!/usr/bin/env bash
set -e

rm -f *.java
swig -c++ -java -I/home/ratan/lib/cntk/Include -I/home/ratan/CNTK/bindings/common cntk_java.i
javac *.java
jar -cvf cntk.jar *.class
export OMPI_CXX=g++-4.8
mpic++ -shared -DCPUONLY -DNOSYNC -D_POSIX_SOURCE -D_XOPEN_SOURCE=600 -D__USE_XOPEN2K -std=c++11 -std=c++0x -fopenmp -fpermissive -fPIC -Werror -fcheck-new -DSWIG -I/home/ratan/lib/cntk/Include -I/home/ratan/lib/jdk/include -I/home/ratan/lib/jdk/include/linux cntk_java_wrap.cxx -L/home/ratan/lib/cntk/cntk/lib -L/home/ratan/lib/cntk/cntk/dependencies/lib -lcntkmath -lcntklibrary-2.0 -L/usr/local/protobuf-3.1.0/lib -lprotobuf -o libCNTKJava.so
