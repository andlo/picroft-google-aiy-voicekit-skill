#!/bin/bash
echo "Installing Google AIY Voice HAT and microphone board (Voice Kit v1)"
# Get AIY drivers
if [ ! -f /etc/apt/sources.list.d/aiyprojects.list ]; then
    echo "adding aptsourses"
    echo "deb https://dl.google.com/aiyprojects/deb stable main" | sudo tee -a /etc/apt/sources.list.d/aiyprojects.list
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
fi
echo "Updating and upgrading..."
sudo apt-get -y update
sudo apt-get -y upgrade

echo "installing what is needed..."
# hack to get aiy-io-mcu-firmware to be installed
sudo mkdir /usr/lib/systemd/system

sudo apt-get -y install aiy-dkms aiy-io-mcu-firmware aiy-vision-firmware dkms raspberrypi-kernel-headers
sudo apt-get -y install aiy-dkms aiy-voicebonnet-soundcard-dkms aiy-voicebonnet-routes
# this does for the moment gives problems on Picroft, and we (maybe) dont need it
#sudo apt-get -y install aiy-python-wheels
sudo apt-get -y install leds-ktd202x-dkms

echo "Installing Pulse audio as it is needed..."
# we need pulseaudio
sudo apt-get -y install pulseaudio

echo "Make soundcard recognizable..."
# make soundcard recognizable
sudo sed -i \
    -e "s/^dtparam=audio=on/#\0/" \
    -e "s/^#\(dtparam=i2s=on\)/\1/" \
    /boot/config.txt
grep -q "dtoverlay=i2s-mmap" /boot/config.txt || \
sudo sh -c "echo 'dtoverlay=i2s-mmap' >> /boot/config.txt"
grep -q "dtoverlay=googlevoicehat-soundcard" /boot/config.txt || \
sudo sh -c "echo 'dtoverlay=googlevoicehat-soundcard' >> /boot/config.txt"
grep -q "dtparam=i2s=on" /boot/config.txt || \
sudo sh -c "echo 'dtparam=i2s=on' >> /boot/config.txt"

echo "Make changes to mycroft.conf"
# make changes to  mycroft.conf
sudo sed -i \
    -e "s/aplay -Dhw:0,0 %1/aplay %1/" \
    -e "s/mpg123 -a hw:0,0 %1/mpg123 %1/" \
    /etc/mycroft/mycroft.conf

echo "Install asound.conf..."
# Install asound.conf
#sudo cp AIY-asound.conf /etc/asound.conf
echo "defaults.ctl.card 0" | sudo tee --append /etc/asound.conf
echo "defaults.pcm.card 0" | sudo tee --append /etc/asound.conf
echo "defaults.pcm.device 0" |sudo tee --append /etc/asound.conf

echo "Rebuild venv..."
# rebuild venv
/home/pi/mycroft-core/dev_setup.sh

echo "We are done - Reboot is neded !"

