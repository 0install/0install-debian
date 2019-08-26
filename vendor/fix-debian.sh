#!/bin/bash
set -eux
export DESTDIR=/tmp/0install-build-vendor
export OCAMLFIND_DESTDIR=$DESTDIR/usr/lib/ocaml
export OCAMLPATH=$DESTDIR/usr/lib/ocaml
export PATH=$DESTDIR/usr/bin:$PATH
export CAMLP4LIB=$DESTDIR/usr/lib/ocaml/camlp4
rm -rf $DESTDIR
mkdir -p $DESTDIR/usr/bin
SRCDIR=$(pwd)
cd $DESTDIR
tar xf $SRCDIR/camlp4-4.05+2.tar.gz
tar xf $SRCDIR/lwt_camlp4-2018-03-25.bz2
tar xf $SRCDIR/type_conv-113.00.02.tar.gz
tar xf $SRCDIR/obus-1.1.7.tar.gz
tar xf $SRCDIR/lwt_glib-1.1.1.tar.gz
(cd camlp4-4.05-2 && sed -i '/+camlp4/d' camlp4/META.in && \
	./configure --bindir=$DESTDIR/usr/bin --libdir=$OCAMLPATH --pkgdir=$OCAMLPATH && \
	make all && make install install-META)
(cd lwt_camlp4-2018-03-25 && jbuilder build @install && jbuilder install)
(cd type_conv-113.00.02 && ./configure --prefix $DESTDIR && make && make install)
(cd obus-1.1.7 &&
	sed -i 's/lwt.syntax/lwt_camlp4/g' _tags && \
	sed -i 's/lwt.syntax/lwt_camlp4/g' setup.ml && \
	./configure --prefix $DESTDIR && make && make install)
(cd lwt_glib-1.1.1 && make && dune install)
