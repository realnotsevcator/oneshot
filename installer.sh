execute_command() {
    if ! "$@"; then
        echo "Error: Failed to execute $*"
        exit 1
    fi
}

execute_command pkg update -y
execute_command pkg install -y root-repo
execute_command pkg install -y tsu
execute_command pkg install -y python
execute_command pkg install -y wpa-supplicant
execute_command pkg install -y pixiewps
execute_command pkg install -y iw
execute_command pkg install -y openssl
execute_command curl -L -o https://raw.githubusercontent.com/sevcator/oneshot-termux/refs/heads/master/oneshot.py
  
