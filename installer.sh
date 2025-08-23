execute_command() {
    if ! "$@"; then
        echo "Error: Failed to execute $*"
        exit 1
    fi
}

execute_command pkg -y -o Dpkg::Options::=--force-confnew update
execute_command pkg -y -o Dpkg::Options::=--force-confnew upgrade
execute_command pkg -y -o Dpkg::Options::=--force-confnew install root-repo
execute_command pkg -y -o Dpkg::Options::=--force-confnew install tsu
execute_command pkg -y -o Dpkg::Options::=--force-confnew install python
execute_command pkg -y -o Dpkg::Options::=--force-confnew install wpa-supplicant
execute_command pkg -y -o Dpkg::Options::=--force-confnew install pixiewps
execute_command pkg -y -o Dpkg::Options::=--force-confnew install iw
execute_command pkg -y -o Dpkg::Options::=--force-confnew install openssl

execute_command curl -L -o oneshot.py https://raw.githubusercontent.com/sevcator/oneshot-termux/refs/heads/master/oneshot.py
