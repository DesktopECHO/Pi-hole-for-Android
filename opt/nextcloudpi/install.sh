#!/bin/bash

# NextCloudPi installation script
#
# Copyleft 2017 by Ignacio Nunez Hernanz <nacho _a_t_ ownyourbits _d_o_t_ com>
# GPL licensed (see end of file) * Use at your own risk!
#
# Usage: ./install.sh
#
# more details at https://ownyourbits.com

# Move Pi-holl to Port 8080

[[ ${EUID} -ne 0 ]] && {
  printf "Must be run as root. Try 'sudo $0'\n\n"
  exit 1
}

cd /opt/nextcloudpi
CODE_DIR=$(pwd)

BRANCH="${BRANCH:-master}"
#DBG=x

set -e$DBG

TEMPDIR="$(mktemp -d /tmp/nextcloudpi.XXXXXX || (echo "Failed to create temp dir. Exiting" >&2 ; exit 1) )"
trap "rm -rf \"${TEMPDIR}\"" 0 1 2 3 15

export PATH="/usr/local/sbin:/usr/sbin:/sbin:${PATH}"

# check installed software
type mysqld &>/dev/null && echo ">>> WARNING: existing mysqld configuration will be changed <<<"
type mysqld &>/dev/null && mysql -e 'use nextcloud' &>/dev/null && { echo "The 'nextcloud' database already exists. Aborting"; exit 1; }

# get dependencies
apt-get install --no-install-recommends -y git ca-certificates sudo lsb-release wget

cd "${CODE_DIR}"

# install NCP
echo -e "\nInstalling NextCloudPi..."
source etc/library.sh

# check distro
check_distro etc/ncp.cfg || {
  echo "ERROR: distro not supported:";
  cat /etc/issue
  exit 1;
}

# indicate that this will be an image build
touch /.ncp-image

mkdir -p /usr/local/etc/ncp-config.d/
cp etc/ncp-config.d/nc-nextcloud.cfg /usr/local/etc/ncp-config.d/
cp etc/library.sh /usr/local/etc/
cp etc/ncp.cfg /usr/local/etc/

cp -r etc/ncp-templates /usr/local/etc/
install_app    lamp.sh
install_app    bin/ncp/CONFIG/nc-nextcloud.sh
run_app_unsafe bin/ncp/CONFIG/nc-nextcloud.sh
rm /usr/local/etc/ncp-config.d/nc-nextcloud.cfg    # armbian overlay is ro
install_app    ncp.sh
run_app_unsafe bin/ncp/CONFIG/nc-init.sh

# echo 'Moving data directory to a more sensible location'
# df -h
# mkdir -p /opt/ncdata
# [[ -f "/usr/local/etc/ncp-config.d/nc-datadir.cfg" ]] || {
#   should_rm_datadir_cfg=true
#   cp etc/ncp-config.d/nc-datadir.cfg /usr/local/etc/ncp-config.d/nc-datadir.cfg
# }
# DISABLE_FS_CHECK=1 NCPCFG="/usr/local/etc/ncp.cfg" run_app_unsafe bin/ncp/CONFIG/nc-datadir.sh
# [[ -z "$should_rm_datadir_cfg" ]] || rm /usr/local/etc/ncp-config.d/nc-datadir.cfg

rm /.ncp-image

# Pi Deploy
echo Installing SysV Initscripts
if [ -e /usr/sbin/unchroot ]; then
        # Copy SysV Init Scripts
        chmod -R 755 "${CODE_DIR}/build/pideploy"
        cp ${CODE_DIR}/build/pideploy/* /etc/init.d/

        # Enable Init Scripts
        update-rc.d -f notify_push defaults
        update-rc.d -f nc-automount-links defaults
        update-rc.d -f nc-provisioning defaults
        update-rc.d -f ncp-metrics-exporter defaults
        update-rc.d -f nextcloud-domain defaults
        update-rc.d -f notify_push defaults
	update-rc.d bootlogs      remove
	update-rc.d smartmontools remove
	update-rc.d rmnologin     remove
	update-rc.d ipmievd       remove
	service notify_push start
fi

bash /usr/local/bin/ncp-provisioning.sh

cd -
rm -rf "${TEMPDIR}"

IP="$(get_ip)"

echo "Done.

First: Visit https://$IP/  https://nextcloudpi.local/
(also https://nextcloudpi.lan/ or https://nextcloudpi/ on windows and mac)
to activate your instance of NC, and save the auto generated passwords.
You may review or reset them anytime by using nc-admin and nc-passwd.

Second: Type 'sudo ncp-config' to further configure
NCP, or access ncp-web on https://$IP:4443/

Note: You will have to add an exception, to bypass your browser warning when you
first load the activation and :4443 pages. You can run letsencrypt to get rid of
the warning if you have a (sub)domain available.
"

# License
#
# This script is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA
