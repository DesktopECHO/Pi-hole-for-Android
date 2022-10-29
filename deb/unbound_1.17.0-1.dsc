Format: 3.0 (quilt)
Source: unbound
Binary: libunbound-dev, libunbound8, python3-unbound, unbound, unbound-anchor, unbound-host
Architecture: any
Version: 1.17.0-1
Maintainer: unbound packagers <unbound@packages.debian.org>
Uploaders:  Robert Edmonds <edmonds@debian.org>, Michael Tokarev <mjt@tls.msk.ru>,
Homepage: https://www.unbound.net/
Standards-Version: 4.6.0
Vcs-Browser: https://salsa.debian.org/dns-team/unbound
Vcs-Git: https://salsa.debian.org/dns-team/unbound.git
Testsuite: autopkgtest
Testsuite-Triggers: dns-root-data, udns-utils
Build-Depends: debhelper-compat (= 13), autoconf, bison, dh-apparmor <!pkg.unbound.libonly>, dh-sequence-python3 <!pkg.unbound.libonly>, dpkg-dev (>= 1.16.1~), flex, libbsd-dev (>= 0.8.1~) [!linux-any], libevent-dev, libexpat1-dev, libnghttp2-dev <!pkg.unbound.libonly>, libprotobuf-c-dev <!pkg.unbound.libonly>, libssl-dev <!pkg.unbound.libonly>, libsystemd-dev <!pkg.unbound.libonly>, libtool, nettle-dev, pkg-config, protobuf-c-compiler <!pkg.unbound.libonly>, python3-dev:any <!pkg.unbound.libonly>, libpython3-dev <!pkg.unbound.libonly>, swig <!pkg.unbound.libonly>
Package-List:
 libunbound-dev deb libdevel optional arch=any
 libunbound8 deb libs optional arch=any
 python3-unbound deb python optional arch=any profile=!pkg.unbound.libonly
 unbound deb net optional arch=any profile=!pkg.unbound.libonly
 unbound-anchor deb net optional arch=any profile=!pkg.unbound.libonly
 unbound-host deb net optional arch=any profile=!pkg.unbound.libonly
Checksums-Sha1:
 593952271ada337cbf92a9a0bb2dc396819e348d 6235060 unbound_1.17.0.orig.tar.gz
 7b429f4b85368cd4a41488d7d237b1d97306d102 833 unbound_1.17.0.orig.tar.gz.asc
 e6054b1ed2c5cd1a66e474864df6a23b622f65d4 28576 unbound_1.17.0-1.debian.tar.xz
Checksums-Sha256:
 dcbc95d7891d9f910c66e4edc9f1f2fde4dea2eec18e3af9f75aed44a02f1341 6235060 unbound_1.17.0.orig.tar.gz
 4b0bf5e596e24c7675a3a28e78adfb33c7716750e0d41b4172337e1d03eb859f 833 unbound_1.17.0.orig.tar.gz.asc
 32b7b36ac7de86d1155c38410eea76c1b7e344677c73eeaf03485eb34dfb2ce4 28576 unbound_1.17.0-1.debian.tar.xz
Files:
 79c863becb1934f6d467be74240e10b5 6235060 unbound_1.17.0.orig.tar.gz
 4aae6f67a05d84147c58d8a7d03c1a2b 833 unbound_1.17.0.orig.tar.gz.asc
 4228d62917b41bdd8dc65d8e71016a78 28576 unbound_1.17.0-1.debian.tar.xz
