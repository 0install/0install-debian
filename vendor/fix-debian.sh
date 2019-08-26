#!/bin/bash
set -eux
export DESTDIR=/tmp/0install-build-vendor
rm -rf $DESTDIR
export OCAMLFIND_DESTDIR=$DESTDIR/usr/lib/ocaml
export OCAMLPATH=$DESTDIR/usr/lib/ocaml
export PATH=$DESTDIR/usr/bin:$PATH
mkdir -p $DESTDIR/usr/bin
tar xf camlp4-4.05+2.tar.gz
tar xf lwt_camlp4-2018-03-25.bz2
tar xf type_conv-113.00.02.tar.gz
tar xf obus-1.1.7.tar.gz
tar xf lwt_glib-1.1.1.tar.gz
(cd camlp4-4.05-2 && sed -i '/+camlp4/d' camlp4/META.in && ./configure && make all && make install install-META DESTDIR=$DESTDIR)
(cd lwt_camlp4 && jbuilder build @install && jbuilder install)
(cd type_conv-113.00.02 && ./configure --prefix $DESTDIR && make && make install)
(cd obus-1.1.7 &&
	sed -i 's/lwt.syntax/lwt_camlp4/g' _tags && \
	sed -i 's/lwt.syntax/lwt_camlp4/g' setup.ml && \
	./configure --prefix $DESTDIR && make && make install)
(cd lwt_glib && make && dune install)
