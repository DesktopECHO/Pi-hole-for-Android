# .bashrc
# Source global definitions
if [ -f /etc/bashrc ]; then
      . /etc/bashrc
fi

# User specific aliases and functions
alias          padd='sudo padd'
alias       service='sudo service'
alias     systemctl='sudo systemctl'
alias   p4a-install='sudo /usr/local/bin/p4a-install'
alias p4a-uninstall='sudo /usr/local/bin/p4a-uninstall'

[ -f /usr/local/bin/pihole ] && /usr/local/bin/pihole status ; echo
