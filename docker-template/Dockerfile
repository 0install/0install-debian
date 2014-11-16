FROM debian:sid
RUN apt-get update

# Core build tools

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential lintian vim

# 0install build dependencies

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gettext ocaml-nox ocaml-findlib libyojson-ocaml-dev libxmlm-ocaml-dev camlp4-extra make liblwt-ocaml-dev libounit-ocaml-dev libextlib-ocaml-dev libcurl-ocaml-dev libssl-ocaml-dev libobus-ocaml-dev liblablgtk2-ocaml-dev liblwt-glib-ocaml-dev --no-install-recommends

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y devscripts fakeroot quilt dh-make less
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dh-ocaml

# Run-time utilities (needed for testing)
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xdg-utils

RUN useradd -U -u 1000 -m tal

USER tal
ENV EMAIL talex5@gmail.com
ENV GNUPGHOME /mnt/gnupg

WORKDIR /mnt