execute_command() {
    if ! "$@"; then
        echo "Error: Failed to execute $*"
        exit 1
    fi
}

execute_command pkg update -y -o Dpkg::Options::=--force-confnew
execute_command pkg upgrade -y -o Dpkg::Options::=--force-confnew
execute_command pkg install root-repo -y -o Dpkg::Options::=--force-confnew
execute_command pkg install sudo -y -o Dpkg::Options::=--force-confnew
execute_command pkg install python -y -o Dpkg::Options::=--force-confnew
execute_command pkg install wpa-supplicant -y -o Dpkg::Options::=--force-confnew
execute_command pkg install pixiewps -y -o Dpkg::Options::=--force-confnew
execute_command pkg install iw -y -o Dpkg::Options::=--force-confnew
execute_command pkg install openssl -y -o Dpkg::Options::=--force-confnew

execute_command curl -L -o oneshot.py https://raw.githubusercontent.com/sevcator/oneshot-termux/refs/heads/master/oneshot.py
