# Pi-hole for Android
**Pi-hole for ARMv7 (2011 and newer) Android devices.**

![IMG_2229](https://user-images.githubusercontent.com/33142753/133272103-28c6eba3-d1f7-4e29-9c5b-7d96d9f94e9e.jpg)

**Note:** There is no endorsement or partnership between this page and [Pi-hole© LLC](https://pi-hole.net/). They deserve [your support](https://pi-hole.net/donate/) if you find this useful.

Pi-hole is a network-level advertisement and Internet tracker blocking application for Linux which acts as a DNS sinkhole intended for use on a private network. It is designed for low-power embedded devices with network capability, focusing on the Raspberry Pi as its 'reference' hardware platform.

Pi-hole for Android is a CentOS disk image for [Linux Deploy](https://play.google.com/store/apps/details?id=ru.meefik.linuxdeploy&hl=en_US&gl=US) that is tuned to work with the Pi-hole installer.  It can be used on **any** rooted Android device with an **ARMv7 or newer CPU**; this includes almost any Android device made in the past 10+ years. Form factor is not important; it could be a phone, tablet, HDMI stick or **any device running Android**.

**Requirements:**

- Android device that has been rooted
- Developer Options -> Root Access -> **Enabled for Apps**

**Instructions:**

- Open web browser on device and download+install the Linux Deploy APK.  You can also download this from the Play Store if preferred:

  - Get the latest version at: **https://github.com/meefik/linuxdeploy/releases**
  - Android 4.x requires an older release: **https://github.com/meefik/linuxdeploy/releases/tag/2.5.1**

-  Download the latest Pi-hole for Android disk image: 
   - **[Release v1.7 - October 5, 2022](https://github.com/DesktopECHO/Pi-hole-for-Android/releases/download/v1.7/p4a17.tgz)**

- Open **Linux Deploy** and change ONLY these settings:
     -  Open the 'Hamburger menu' (Symbol with three dashes at top left of screen) then touch **Settings**.  Place a checkmark on these options:
        -  **Lock Screen** (If you want to keep display always on)
        -  **Lock Wi-Fi** (If your device has Wi-Fi)
        -  **Wake Lock** 
        -  **Autostart**
        -  **Debug Mode** (Provides console output for Pi-hole status)
     -  Open **Properties Menu** (To the right of the 'Stop' button)
        -  Distribution: **rootfs.tar**
        -  Source Path - This varies depending on the device, ie: **${EXTERNAL_STORAGE}/Download/p4a17.tgz**
        -  Image size (MB): **4000** (Recommmended, for smaller devices minimum is 2000 MB)
        -  Set password for user **android**
        -  Init -> **Enable**
     -  Open **Options** Menu (Three dots at top right of screen)
        -  Select **Install** and "OK" to confirm. 
        -  Wait a few minutes for the image to install.
          
     -  When install is complete, the Linux Deploy console window will show the following at the end of the console output: 

        `````[HH:mm:ss] >>> :: Configuring core/profile ...`````
        
        `````[HH:mm:ss] >>> :: Configuring core/sudo ...`````
        
        `````[HH:mm:ss] >>> :: Configuring core/unchroot ...`````
        
        `````[HH:mm:ss] >>> deploy`````
        
    -  **Before you continue, make sure the Linux Deploy Console is free of error messages.**  If there are errors, troubleshoot by verifying the location of **p4a17.tgz** using a [file manager](https://github.com/DesktopECHO/Pi-hole-for-Android/wiki/Trouble-finding-path-where-Pi%E2%80%90hole-image-is-downloaded,-or-errors-are-reported-during-creation-of-Pi%E2%80%90hole-disk-image.) as the path can vary by device.  If you have trouble installing the image in Linux Deploy it may be because of SELinux.  See this [post on XDA](https://forum.xda-developers.com/t/app-tool-2-0-official-the-selinux-switch.3656502/) for an APK to disable SELinux.  
  
Touch the **[ ▸ START ]** button, and "OK" to confirm - The instance takes a few seconds to "boot" 

-----------------------------------------------------------
**INSTALLATION COMPLETE - PI-HOLE IS RUNNING ON YOUR ANDROID DEVICE!**

-----------------------------------------------------------
The Android device's IP is shown at the top of the Linux Deploy main window.  You can interact with Pi-hole in several ways, the examples below use IP **_10.13.12.11_** 

 - From a Windows desktop, connect via RDP **->** **```mstsc.exe /v:10.13.12.11```**

 - From a computer running Linux, connect via SSH **->** **```ssh android@10.13.12.11```**

 - Pi-hole administration is accessible from any browser on your network **->** **```http://10.13.12.11/admin```**

 - If your Android device has a display, you can RDP into the Pi-hole instance (as localhost) by installing the [Microsoft Remote Desktop](https://play.google.com/store/apps/details?id=com.microsoft.rdc.androidx) client.

![image](https://user-images.githubusercontent.com/33142753/147254465-26443e85-6695-46e6-83f4-4c3ff1749804.png)

**Pi-hole for Android wiki topics:**

- [PADD is missing information / How to update](https://github.com/DesktopECHO/Pi-hole-for-Android/wiki/PADD-is-missing-information)
- [Setting custom disk/shmem alert thresholds](https://github.com/DesktopECHO/Pi-hole-for-Android/wiki/Setting-custom-alert-thresholds-for-disk-and-shmem-monitoring)
- [Linux Deploy - Trouble finding disk image or install location](https://github.com/DesktopECHO/Pi-hole-for-Android/wiki/Trouble-finding-path-where-Pi%E2%80%90hole-image-is-downloaded,-or-errors-are-reported-during-creation-of-Pi%E2%80%90hole-disk-image.)

**Additional Info:**

RDP Sessions launch the Openbox window manager with QTerminal in fullscreen mode.  To open a new tab hit **[Ctrl-Shift-T]** and to un-hide the menubar hit **[Ctrl-Shift-M]**

You can restart (or "bounce") the Pi-hole instance in Linux Deploy by pressing **[ ■ STOP ]** and waiting a few seconds for the instance to indicate all services are stopped.  Restart the instance by pressing **[ ▸ START ]**

When a Pi-hole instance starts up, the default setting is to let it automagically configure networking.  If you change networks on the Android device simply restart the instance for Pi-hole to pick up the new settings.

Alternatively, set a static assignment by commenting-out two lines in ```/etc/rc.local``` (You will see which ones when you open the file in an editor.)  After the lines are commented out with a hash "#" you can manually add your IP, subnet and interface name to ```/etc/pihole/setupVars.conf```

Added [Unbound](https://www.nlnetlabs.nl/projects/unbound/about) to provide encrypted DNS by default; no addional configuration is necessary.

The Pi-hole instance on Android otherwise behaves like it is running on a 'real' Raspberry-Pi or a standard PC.  Consult the extensive documentation online to learn how to fully leverage Pi-hole's functionality.

Adjust QT display scaling: ```~/startwm.sh``` 

Change the font size in QTerminal: ```~/.config/qterminal.org/qterminal.ini```

**If your Android device has a battery and was unused for months or years, replace its battery.**  Old, worn, or abused Li-ion batteries can fail when pushed back into service.  Failure appears as a bulge in the battery, or worse a [**_thermal event_**](https://www.urbandictionary.com/define.php?term=unexpected+thermal+event).  A good battery provides [UPS](https://en.wikipedia.org/wiki/Uninterruptible_power_supply) protection for your newly-provisioned Pi-hole.
