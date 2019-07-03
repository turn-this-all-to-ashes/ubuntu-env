#!/usr/bin/env python

import sys
import commands
import os
import subprocess


def installPackage(pm , packages):
    for package in packages:
        p = subprocess.Popen(str(pm+package) , shell = True , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        if not p.returncode == 0:
            print("install " + package+" failed:")
            for line in p.stdout.readlines():
                print(line)
    return 0

def runCommandE(command):
    p = subprocess.Popen(command , shell = True , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    if not p.returncode == 0:
        print("run "+command + " failed: ")
        for line in p.stdout.readlines():
            print(line)
        sys.exit()
    return (0 , p.stdout.readlines())

def zsh():
    #autojump
    runCommandE("git clone git://github.com/wting/autojump.git")
    runCommandE("./autojump/install.py")
    #autosuggestions
    runCommandE("git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions")
    #highlighting
    runCommandE("git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting")
    #history-substring-search
    runCommandE("git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search")

    #.zshrc
    runCommandE("cp ~/.zhsrc ~/.zshrc.bak")
    with open("/root/.zshrc.bak" , "r") as file:
        lines = file.readlines()
        num = 0
        for line in lines:
            line = line.strip('\n')
            if line[:8] == "plugins=":
                line = "plugins=(git heroku pip lein command-not-found zsh-syntax-highlighting zsh-autosuggestions history-substring-search)"
            if num == 0 :
                runCommandE(str('echo "' + line + '" > ~/.zshrc'))
                num = 1
            else:
                runCommandE(str('echo "' + line + '" >> ~/.zshrc'))
    runCommandE('echo "[[ -s /root/.autojump/etc/profile.d/autojump.sh ]] && source /root/.autojump/etc/profile.d/autojump.sh" >> ~/.zshrc')
    runCommandE('echo "autoload -U compinit && compinit -u" >> ~/zshrc')
    runCommandE('echo "bindkey \'^P\' history-substring-search-up" >> ~/.zshrc')
    runCommandE('echo "bindkey \'^N\' history-substring-search-down" >> ~/.zshrc')

if __name__ == "__main__" :
    runCommandE("mkdir -p /root/tmp")
    os.chdir("/root/tmp")
    pi = 0
    vim = 0
    emacs = 0
    shadowsocks = 0
    for args in sys.argv:
        if args[0] == '-':
            if args[1] != '-':
                if 'p' in args:
                    pi = 1
                if 'e' in args :
                    emacs = 1
                if 'v' in args:
                    vim =1
                if 's' in args :
                    shadowsocks = 1
            elif args[1] == '-':
                if 'package' in args:
                    pi = 1
                if 'emacs' in args:
                    emacs =1
                if 'vim' in args:
                    vim = 1
                if 'shadowsocks' in args:
                    shadowsocks = 1
    if len(sys.argv) == 1:
        pi = 1
        emacs = 1
        vim =1
        shadowsocks = 1

    if pi == 1:
        #ssh
        pm = 'apt-get install -y '
        packages = ['openssh-server' ,]
        installPackage(pm , packages)
        runCommandE("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
        with open("/etc/ssh/sshd_config.bak" , "r") as file:
            lines = file.readlines()
            num = 0
            for line in lines:
                line = line.strip('\n')
                if line[:15] == "PermitRootLogin" or line[:16] == "#PermitRootLogin":
                    line = "PermitRootLogin yes"
                if num == 0 :
                    runCommandE(str('echo "' + line + '" > /etc/ssh/sshd_config'))
                    num = 1
                else:
                    runCommandE(str('echo "' + line + '" >> /etc/ssh/sshd_config'))
        runCommandE("systemctl reload ssh")

        #packages
        packages = ['wget' , 'curl' , 'gcc' , 'g++', 'gdb' ,'git', 'zsh' , 'emacs-nox' ,'vim' , 'screen' ,'tree' , 'manpages-posix manpages-posix-dev','htop','zip' , 'tmux','cmake' ,'automake' ,'autoconf'  , 'ctags' , 'global' , 'python-pip' , 'python' , 'python3' , 'perl' ]
        installPackage( pm , packages)

        #zsh
        ohmyzsh = "wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh"
        runCommandE(ohmyzsh)
        (ret , output) = runCommandE("which zsh")
        output = output[0]
        runCommandE(str("chsh -s " + output.strip()))
        zsh()

        #percol
        runCommandE("pip install percol")

        #rust
        cmd = "curl https://sh.rustup.rs -sSf | sh"
        p = subprocess.Popen(cmd,shell = True)
        p.wait()
        if p.returncode != 0 :
            print("install rust failed")

    #emacs
    if emacs == 1:
        runCommandE("git clone https://github.com/purcell/emacs.d.git ~/.emacs.d")
        runCommandE("cp /root/.emacs.d/init.el /root/.emacs.d/init.el.bak")
        with open("/root/.emacs.d/init.el.bak" , "r") as file:
            lines = file.readlines()
            num = 0
            for line in lines:
                line = line.strip('\n')
                if line == "(require 'init-xterm)":
                    line = ";;(require 'init-xterm)"
                if num == 0 :
                    runCommandE(str('echo "' + line + '" > /etc/ssh/sshd_config'))
                    num = 1
                else:
                    runCommandE(str('echo "' + line + '" >> /etc/ssh/sshd_config'))
        runCommandE("mkdir -p /root/tmp/obj/")
        os.chdir("/usr/include")
        runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
        os.chdir("/usr/src")
        runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
        os.chdir("/usr/local/include")
        runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
        os.chdir("/root/tmp")
        runCommandE("curl -s https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/init-local.el > /root/.emacs.d/lisp/init-local.el")
        #em alias
        runCommandE("touch em")
        runCommandE('echo "#!/bin/sh" > em')
        runCommandE('echo "emacsclient -t $@ || (emacs --daemon && emacsclient -t $@)" >> em')
        runCommandE('chmod +x em')
        runCommandE('mv em /usr/local/bin/')

    #vim
    if vim == 1:
        runCommandE("git clone https://github.com/DamZiobro/vim-ide")
        cmd = "./vim-ide/installVim.sh"
        p = subprocess.Popen(cmd , shell = True)
        p.wait()
        if p.returncode != 0 :
            print("set up vim failed")

    #shadowsocks
    if shadowsocks == 1:
        runCommandE("pip install shadowsocks")
        runCommandE("mkdir -p /etc/shadowsocks/")
        print("plz input server , port , passwd of ss(/etc/shadowsocks/ss.json)")
        server = input("server address:\n")
        port = input("server port:\n")
        passwd = input("server passwd:\n")
        content = '''{
    "server":"''' + str(server).strip() + '''",
    "server_port":''' + str(port).strip() + ''',
    "local_port":1080,
    "password":"''' + str(passwd).strip()+'''",
    "timeout":600,
    "method":"aes-256-cfb"
}
'''

        file = open("/etc/shadowsocks/ss.json", "w")
        file.write(content)
        file.close()
        runCommandE("cp /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py.bak")
        runCommandE('perl -p -i -e "s/cleanup/reset/g" /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py')
        file = open("/lib/systemd/system/ssc.service" , "w")
        content = """[Unit]
Description=test

[Service]
Type=forking
ExecStart=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d start
ExecReload=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d restart
ExecStop=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d stop

[Install]
WantedBy=multi-user.target"""
        file.write(content)
        file.close
        runCommandE("systemctl daemon-reload")

        print("usage:systemctl start/stop/reload ssc")
