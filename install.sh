#!/bin/bash

sudo apt install psmisc dbus libdbus-glib-1-dev libdbus-1-dev python3-dbus git tor -y
git clone https://github.com/emlid/systemd-manager
cd systemd-manager
sudo python3 setup.py install
cd ..
sudo python3 -m pip install -U -r requirements.txt
# sudo python3 setup.py install

cmd="sudo service tor status"
echo -e "\n\n$cmd  # You might use start instead :)\n\n"
$($cmd)

# You might add the following lines on your `torrc`, it's your choice though (Rate limites are annoying..)
# CircuitBuildTimeout 10
# LearnCircuitBuildTimeout 0
# MaxCircuitDirtiness 10
