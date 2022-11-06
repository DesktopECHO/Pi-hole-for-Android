#!/bin/sh
# xrdp X session start script (c) 2015, 2017, 2021 mirabilos
# published under The MirOS Licence

# Rely on /etc/pam.d/xrdp-sesman using pam_env to load both
# /etc/environment and /etc/default/locale to initialise the
# locale and the user environment properly.

xsetroot -solid Black

if test -r /etc/profile; then
        . /etc/profile
fi
export XDG_CONFIG_HOME=$HOME/.config
export XDG_RUNTIME_DIR=$HOME/.local
export XDG_CACHE_HOME=$HOME/.cache
export XDG_DATA_HOME=$HOME/.local/share
export CHROMIUM_FLAGS="--no-sandbox --disable-gpu --test-type"
export QTWEBENGINE_CHROMIUM_FLAGS="--single-process"
export QT_ACCESSIBILITY=0
export QT_X11_NO_MITSHM=1
export QT_QPA_PLATFORMTHEME=qt5ct
export QT_SCALE_FACTOR=1.5
export RUNLEVEL=3
export NO_AT_BRIDGE=1
export MOZ_FORCE_DISABLE_E10S=1
export MOZ_LAYERS_ALLOW_SOFTWARE_GL=1
export WEBKIT_DISABLE_COMPOSITING_MODE=1
export WEBKIT_FORCE_SANDBOX=0

exec /bin/sh /etc/X11/Xsession
