# Pi-hole for Android APK Installer

![IMG_2229](https://user-images.githubusercontent.com/33142753/133272103-28c6eba3-d1f7-4e29-9c5b-7d96d9f94e9e.jpg)

**Note:** There is no endorsement or partnership between this page and [Pi-hole© LLC](https://pi-hole.net/). They deserve [your support](https://pi-hole.net/donate/) if you find this useful.

Pi-hole is a network-level advertisement and Internet tracker blocking application for Linux which acts as a DNS sinkhole intended for use on a private network. It is designed for low-power embedded devices with network capability, focusing on the Raspberry Pi as its 'reference' hardware platform.

Pi-hole for Android is a Raspbian disk image tuned to work with the Pi-hole installer on Pi Deploy (a fork of Linux Deploy).  It can be used on **any** rooted Android device with an **ARMv7 or newer CPU** running Android 5.0 (Lolipop) or newer.  Form factor is not important; it could be a phone, tablet, HDMI stick or **any device running Android**.  For very old devices running Android 4.x, see the [Legacy branch](https://github.com/DesktopECHO/Pi-hole-for-Android/tree/legacy)

### Requirements:

- Android device that has been rooted

### Note to users of previous builds:

- Uninstall any previous versions of Linux Deploy or Pi Deploy and reboot your device.
- Failure to heed this advice will cause issues!

### Installation:

- Download and Install the latest [Pi Deploy APK](https://github.com/DesktopECHO/Pi-hole-for-Android/releases/latest/download/pideploy.apk)
- Tap the main menu (**Three dots** at the top right of screen)
- Tap **New Deployment**
- In a few minutes, the [Raspbian Image](https://github.com/DesktopECHO/linuxdeploy-images/releases/latest/download/raspbian.tgz) will be downloaded and installed on your device.
- When deployment is complete, tap **[  ▷ START ]**  to launch the instance.
- The instance will provide you with a password for Pi-hole admin, SSH and RDP access (Username: _android_, see screenshot below)
- **Note**: The password appears only once when the image is deployed, make sure you record this information.
- **Hint**:  The password text can be copy/pasted to other Android apps (like Remote Desktop) 
- _(Optional, post-install)_ To install PIXEL Desktop run `pideploy-gui-install` and restart the instance.  Next time you login via RDP you will have a full desktop session with audio support.

-----------------------------------------------------------
**INSTALLATION COMPLETE    ·    Pi-Hole is running on your Android Device**

-----------------------------------------------------------
The Android device's IP is shown at the top of the Linux Deploy main window.  You can interact with Pi-hole in several ways, the examples below use IP **_10.73.0.31_** 

 - From a Windows desktop, connect via RDP **->** **```mstsc.exe /v:10.73.0.31```**

 - From a computer running Linux, connect via SSH **->** **```ssh android@10.73.0.31```**

 - Pi-hole administration is accessible from any browser on your network **->** **```http://10.73.0.31/admin```**

 - If your Android device has a display, you can RDP into the Pi-hole instance (as localhost) by installing the [Microsoft Remote Desktop](https://play.google.com/store/apps/details?id=com.microsoft.rdc.androidx) client.

<img width="1586" alt="image" src="https://user-images.githubusercontent.com/33142753/200673465-dca797d6-04b3-4b39-bfd1-56c472c7cff7.png">

<img width="1508" alt="image" src="https://user-images.githubusercontent.com/33142753/200677147-bd8230bb-39df-4aab-b4da-ef64e5d00f08.png">

<img width="1364" alt="image" src="https://user-images.githubusercontent.com/33142753/200670602-647fa8d3-5750-4d21-8c0c-c059e011fe6f.png">

**Pi-hole for Android wiki topics:**

- [Pi/Linux Deploy - Trouble finding disk image or install location](https://github.com/DesktopECHO/Pi-hole-for-Android/wiki/Trouble-finding-path-where-Pi%E2%80%90hole-image-is-downloaded,-or-errors-are-reported-during-creation-of-Pi%E2%80%90hole-disk-image.)

**Additional Info:**

RDP Sessions launch the Openbox window manager with QTerminal in fullscreen mode.  To open a new tab hit **[Ctrl-Shift-T]** and to un-hide the menubar hit **[Ctrl-Shift-M]**

You can restart (or "bounce") the Pi-hole instance in Pi Deploy by pressing **[ ■ STOP ]** and waiting a few seconds for the instance to indicate all services are stopped.  Restart the instance by pressing **[ ▸ START ]**

When a Pi-hole instance starts up, the default setting is to let it automagically configure networking.  If you change networks on the Android device simply restart the instance for Pi-hole to pick up the new settings.

Alternatively, set a static assignment by commenting-out two lines in ```/etc/init.d/android-init``` (You will see which ones when you open the file in an editor.)  After the lines are commented out with a hash "#" you can manually add your IP, subnet and interface name to ```/etc/pihole/setupVars.conf```

Added latest release of [Unbound 1.17](https://www.nlnetlabs.nl/projects/unbound/about) to provide encrypted DNS by default; no addional configuration is necessary but you may customize to preference.

The Pi-hole instance on Android otherwise behaves like it is running on a 'real' Raspberry-Pi or a standard PC.  Consult the extensive documentation online to learn how to fully leverage Pi-hole's functionality.

Adjust QT display scaling: ```~/startwm.sh``` 

Change the font size in QTerminal: ```~/.config/qterminal.org/qterminal.ini```

**If your Android device has a battery and was unused for months or years, replace its battery.**  Old, worn, or abused Li-ion batteries can fail when pushed back into service.  Failure appears as a bulge in the battery, or worse a [**_thermal event_**](https://www.urbandictionary.com/define.php?term=unexpected+thermal+event).  A good battery provides [UPS](https://en.wikipedia.org/wiki/Uninterruptible_power_supply) protection for your newly-provisioned Pi-hole.
