FROM youske/alpine-conda:miniconda3

MAINTAINER Peter van Heusden <pvh@sanbi.ac.za>

RUN conda install -y click
RUN mkdir /script

RUN mkdir /data

VOLUME /data

WORKDIR /data

ADD tree_tool.py /script/tree_tool.py

ENTRYPOINT [ "/conda/bin/python", "/script/tree_tool.py" ]
