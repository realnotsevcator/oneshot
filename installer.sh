execute_command() {
    if ! "$@"; then
        echo "Error: Failed to execute $*"
        exit 1
    fi
}

execute_command apt-get update
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install root-repo
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install tsu
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install python
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install wpa-supplicant
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install pixiewps
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install iw
execute_command apt-get -y -o Dpkg::Options::=--force-confnew install openssl

execute_command curl -L -o oneshot.py https://raw.githubusercontent.com/sevcator/oneshot-termux/refs/heads/master/oneshot.py
