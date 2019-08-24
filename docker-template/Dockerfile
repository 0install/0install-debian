FROM debian:sid
RUN apt-get update

# Core build tools

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y build-essential lintian vim

# 0install build dependencies

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
	gettext \
	ocaml-nox \
	ocaml-findlib \
	libyojson-ocaml-dev \
	libxmlm-ocaml-dev \
	cppo \
	make \
	liblwt-ocaml-dev \
	ocaml-dune \
	libounit-ocaml-dev \
	libcurl-ocaml-dev \
	libsha-ocaml-dev \
	libobus-ocaml-dev \
	liblablgtk2-ocaml-dev \
	liblwt-glib-ocaml-dev \
	devscripts \
	fakeroot \
	quilt \
	dh-make \
	less \
	dh-ocaml \
	--no-install-recommends

# Run-time utilities (needed for testing)
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xdg-utils python-gobject-2 ocaml-native-compilers

RUN useradd -U -u 1000 -m tal

USER tal
ENV EMAIL talex5@gmail.com
ENV GNUPGHOME /mnt/gnupg

WORKDIR /mnt
