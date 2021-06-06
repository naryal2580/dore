#!/bin/bash

echo "INFO: This script needs su sccess."
sudo whoami > /dev/null

unams="$(uname -s)"
case "$unams" in
    Linux*)     machine="Linux";;
    Darwin*)    machine="OSX";;
    *)          machine="$unams"
esac


if [[ $machine == "Linux" ]]; then
    # CAUTION: TESTED ON Kali, Arch Linux with AUR and yay

    deps="psmisc dbus libdbus-glib-1-dev libdbus-1-dev python3-dbus git tor"

    if command -v apt &> /dev/null; then
	    sudo apt update
	    sudo apt install $deps -y

    elif command -v yay &> /dev/null; then  # if it's an Arch, then you MUST have yay.
	    sudo pacman -Syu
	    yay -S $deps --needed

    elif [[ $1 == "--force" ]]; then
	    echo -e "I assumed that you've managed to install a few dependencies: $deps\n"
	    echo -n "Are you sure, you wanna still continue? [y/N]: "
	    read prompt
	    if [[ $prompt == "y" ]]; then
		    echo "Yes, master as you wish!"
	    else
		    echo "Terminating."
		    exit 0
	    fi
    else
	    echo -e "Please make sure, you've a few dependencies: $deps\n"
	    echo "After it's done, run the same \`$0\` (me) script with \`--force\` flag."
	    exit 1
    fi

    git clone https://github.com/emlid/systemd-manager
    cd systemd-manager
    sudo python3 setup.py install
    cd -

    cmd="sudo systemctl status tor"
    echo -e "\n\n$cmd  # You might use start instead :)\n\n"
    echo $($cmd)

elif [[ $machine == "OSX" ]]; then
    if command -v brew &> /dev/null; then
        brew install tor
        sudo brew services start tor
        echo "This is your sample torrc: /usr/local/etc/tor/torrc.sample"
    elif command -v port &> /dev/null; then
        sudo port install tor
        echo "Make sure you've enabled tor service."
        echo "This is your sample torrc: /opt/local/etc/tor/torrc.sample"
    fi
else
    echo "Unknown device: $machine"
    echo "Please install the dependencies yourself."
fi

sudo python3 -m pip install -U -r requirements.txt
# sudo python3 setup.py install

# You might add the following lines on your `torrc`, it's your choice though (Rate limites are annoying..)
# CircuitBuildTimeout 10
# LearnCircuitBuildTimeout 0
# MaxCircuitDirtiness 10
