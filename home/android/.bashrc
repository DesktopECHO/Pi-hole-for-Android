# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
alias          padd='sudo padd'
alias       service='sudo service'
alias   p4a-install='sudo /usr/local/bin/p4a-install'
alias p4a-uninstall='sudo /usr/local/bin/p4a-uninstall'

[ -f /usr/local/bin/pihole ] && echo
[ -f /usr/local/bin/pihole ] && echo "    Pi-hole Stats -> padd"
[ -f /usr/local/bin/pihole ] && echo "   Pi-hole Update -> pihole -up"
[ -f /usr/local/bin/pihole ] && echo "  Pi-hole Install -> p4a-install"
[ -f /usr/local/bin/pihole ] && echo "Pi-hole Uninstall -> p4a-uninstall"
[ -f /usr/local/bin/pihole ] && echo
[ -f /usr/local/bin/pihole ] && /usr/local/bin/pihole status
[ -f /usr/local/bin/pihole ] && echo
