#!/usr/bin/env python2

import sys
import commands
import os
import subprocess


def installPackage(pm , packages):
    for package in packages:
        print("")
        print(str(pm+package))
        p = subprocess.Popen(str(pm+package) , shell = True )
        p.wait()
        if not p.returncode == 0:
            print("install " + package+" failed")
        print("")
    return 0

def runCommandE(command):
    print("")
    print(command)
    p = subprocess.Popen(command , shell = True )
    p.wait()
    if not p.returncode == 0:
        print("run "+command + " failed")
        print("")
        sys.exit()
    print("")
    return p.returncode

def runCommand(command):
    print("")
    print(command)
    p = subprocess.Popen(command , shell = True )
    p.wait()
    if not p.returncode == 0:
        print("run "+command + " failed")
        print("")
    print("")
    return p.returncode

def zsh():
    #autojump
    runCommandE("git clone git://github.com/wting/autojump.git")
    os.chdir("./autojump")
    (ret , output) = commands.getstatusoutput("./install.py")
    if not ret == 0:
        print(output)
        print("install autojump failed")
        sys.exit()
    output= output.split('\n')
    autojumpconf= []
    for line in output:
        if not line[0] == ' ':
            continue
        if line[8] == '[' or line[8] == 'a':
            autojumpconf.append(line)
    os.chdir("/root/tmp")
    runCommandE("rm -rf ./autojump")
    
    #autosuggestions
    runCommandE("git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions")
    #highlighting
    runCommandE("git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting")
    #history-substring-search
    runCommandE("git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search")
    #.zshrc
    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/zshrc -O - | cat > /root/.zshrc")
    file = open("/root/.zshrc" , "a")
    file.write(autojumpconf[1] + '\n')
    file.write(autojumpconf[0] + '\n')
    file.flush()
    file.close()
    runCommandE("git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf")
    runCommandE("~/.fzf/install")

def addtan(input):
    return "\t" + str(input)+"\n"

if __name__ == "__main__" :

    (ret , output )  = commands.getstatusoutput("lsb_release -a")
    if not ret == 0:
        print("get distributor failed")
        sys.exit()
    output = output.split("\n")
    distributorID = ''
    release = ''
    for line in output:
        if "Distributor ID" in line:
            distributorID = (line.split(":"))[1].strip()
        if "Release" in line:
            release = (line.split(":"))[1].strip()

    if distributorID == '' or release == '':
        print("get distributor failed")
        sys.exit()

    if distributorID == 'Ubuntu':
        release = float(release)
        if release < 18.04:
            print('ubuntu ' + str(release) + 'are not supported')
            sys.exit()
        pm = 'apt-get install -y '

    vim = 0
    emacs = 0
    shadowsocks = 0
    norust = 0
    nonfs = 0
    nogolang = 0
    nomysql = 0
    update = 0

    for args in sys.argv:
        if args[0] == '-':
            if args[1] != '-':
                if 'e' in args :
                    emacs = 1
                if 'v' in args:
                    vim =1
                if 's' in args :
                    shadowsocks = 1
                if 'u' in args :
                    update = 1
            elif args[1] == '-':
                if 'emacs' in args:
                    emacs =1
                if 'vim' in args:
                    vim = 1
                if 'shadowsocks' in args:
                    shadowsocks = 1
                if 'no-rust' in args:
                    norust = 1
                if 'no-nfs' in args:
                    nonfs = 1
                if 'no-golang' in args:
                    nogolang = 1
                if 'no-mysql' in args :
                    nomysql = 1
    if len(sys.argv) == 1:
        emacs = 1
        vim =1
        shadowsocks = 1

    if update == 0:
        runCommandE("mkdir -p /root/tmp")
        os.chdir("/root/tmp")
        runCommandE("mkdir -p /root/nfs/ftp")

    #ssh
    if update == 0:
        packages = ['openssh-server' ,]
        installPackage(pm , packages)
        runCommandE("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
        with open("/etc/ssh/sshd_config.bak" , "r") as file:
            lines = file.readlines()
            file = open("/etc/ssh/sshd_config" ,"w")
            for line in lines:
                line = line.strip('\n')
                if line[:15] == "PermitRootLogin" or line[:16] == "#PermitRootLogin":
                    line = "PermitRootLogin yes"
                file.write(line + "\n")
            file.flush()
            file.close()

    #packages
    packages = ['wget' , 'curl' , 'gcc' , 'g++', 'gdb' ,'git', 'zsh' ,'vim' , 'screen' ,'tree' , 'manpages-posix manpages-posix-dev','htop','zip' , 'tmux','cmake' ,'automake' ,'autoconf'  , 'ctags' , 'global' , 'python-pip' , 'python' , 'python3' , 'perl' ,'rar' , 'p7zip' , 'sqlite' , 'curlftpfs' , 'vsftpd' , 'cloc']
    installPackage( pm , packages)
    if emacs == 1:
        packages = ['emacs-nox' ,]
        installPackage(pm , packages)
    if not nonfs == 1:
        packages = ['nfs-kernel-server' ,]
        installPackage(pm , packages)
    if not nogolang == 1:
        packages = ['golang' ,]
        installPackage(pm , packages)
    if not nomysql == 1:
        packages = ['mysql-server' , ]
        runCommand('apt-get update')
        installPackage(pm , packages )

    #chown nfs/ftp
    if update == 0:
        runCommandE("chown -R ftp:ftp /root/nfs/ftp")

    #gitconfig
    if update == 0:
        (ret , output) = commands.getstatusoutput("hostname")
        if not ret == 0:
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/gitconfig -O - | cat > /root/.gitconfig")
        else:
            email = output.strip() + "@example.com"
            file = open("./tmpgitconfig.tmp" , "w")
            file.write("[user]\n")
            file.write(addtan(email))
            file.write(addtan(output.strip()))
            file.write("[alias]\n")
            file.write(addtan("co = checkout"))
            file.write(addtan("ss = status"))
            file.write(addtan("cm = commit -m"))
            file.write(addtan("br = branch"))
            file.write(addtan("bm = branch -m"))
            file.write(addtan("cb = checkout -b"))
            file.write(addtan("df = diff"))
            file.write(addtan("ls = log --stat"))
            file.write(addtan("lp = log -p"))
            file.write(addtan("plo = pull origin"))
            file.write(addtan("plod = pull origin dev"))
            file.write(addtan("pho = push origin"))
            file.flush()
            file.close()
            runCommandE("mv ./tmpgitconfig.tmp /root/.gitconfig")

    #zsh
    if update == 0:
        ohmyzsh = "wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh"
        runCommandE(ohmyzsh)
        (ret , output) = commands.getstatusoutput("which zsh")
        if not ret == 0:
            runCommandE("chsh -s /usr/bin/zsh" )
        else:
            runCommandE("chsh -s " + output.strip())
        zsh()

    #alias
    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/cdls -O - | cat > /usr/local/bin/cdls")
    runCommandE("chmod +x /usr/local/bin/cdls")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/grepv -O - | cat > /usr/local/bin/grepv")
    runCommandE("chmod +x /usr/local/bin/grepv")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/gtext -O - | cat > /usr/local/bin/gtext")
    runCommandE("chmod +x /usr/local/bin/gtext")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/finda -O - | cat > /usr/local/bin/finda")
    runCommandE("chmod +x /usr/local/bin/finda")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/findc -O - | cat > /usr/local/bin/findc")
    runCommandE("chmod +x /usr/local/bin/findc")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/pg -O - | cat > /usr/local/bin/pg")
    runCommandE("chmod +x /usr/local/bin/pg")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/killemacs -O - | cat > /usr/local/bin/killemacs")
    runCommandE("chmod +x /usr/local/bin/killemacs")

    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/sshcopyid -O - | cat > /usr/local/bin/sshcopyid")
    runCommandE("chmod +x /usr/local/bin/sshcopyid")

    #vsftpd
    if update == 0:
        runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/vsftpd -O - | cat > /etc/vsftpd.conf")
        runCommandE("systemctl restart vsftpd")

    #percol
    if update == 0:
        runCommandE("pip install percol")

    #add-gitignore
    if update == 0:
        runCommandE("pip install add-gitignore")

    #ssh key
    if update == 0:
        runCommandE("ssh-keygen -t rsa")

    #rust
    if update == 0:
        if not norust == 1:
            cmd = "curl https://sh.rustup.rs -sSf | sh"
            p = subprocess.Popen(cmd,shell = True)
            p.wait()
            if p.returncode != 0 :
                print("install rust failed")
            file = open("/root/.zprofile" , "a")
            file.write('export PATH="$HOME/.cargo/bin:$PATH"\n')
            file.flush()
            file.close()

    #nfs
    if update == 0:
        if not nonfs == 1:
            (ret , output) = commands.getstatusoutput("ifconfig")
            auto = 0
            network = ''
            if not ret == 0:
                auto = 0
            else:
                output  = output.split('\n\n')
                for s in output:
                    networktmp = s.split('\n')
                    networktmp = (networktmp[1]).strip()
                    networktmp = networktmp.split(' ')
                    networktmp = networktmp[1]
                    if '192.' in network :
                        auto = 1
                        network= networktmp
            if auto == 1:
                network = network.split('.')
                network = 'echo "/root/nfs ' + network[0] + "." + network[1]+ "." + network[2] + ".0/24" + '(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports'
            else:
                network = raw_input("input nfs network(e.g. 192.168.0.0/24) :\n")
                network = 'echo "/root/nfs ' + network + '(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports'
            runCommandE(network)
            runCommandE("exportfs -a")
            runCommandE("systemctl restart nfs-kernel-server")

    #mysql
    if update == 0 :
        if not nomysql == 1:
            runCommand("mysql_secure_installation")
            runCommandE("systemctl restart mysql.service")

    #emacs
    if update == 0:
        if emacs == 1:
            runCommandE("git clone https://github.com/purcell/emacs.d.git ~/.emacs.d")
            runCommandE("cp /root/.emacs.d/init.el /root/.emacs.d/init.el.bak")
            with open("/root/.emacs.d/init.el.bak" , "r") as file:
                lines = file.readlines()
                file = open("/root/.emacs.d/init.el" , "w")
                for line in lines:
                    line = line.strip('\n')
                    if line == "(require 'init-xterm)":
                        line = ";;(require 'init-xterm)"
                    file.write(line + "\n")
                file.flush()
                file.close()
            runCommandE("mkdir -p /root/tmp/obj/")
            os.chdir("/usr/include")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir("/usr/src")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir("/usr/local/include")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir("/root/tmp")
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/init-local.el -O - | cat > /root/.emacs.d/lisp/init-local.el")
        #em alias
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/emacsalias -O - | cat > /usr/local/bin/em")
            runCommandE("chmod +x /usr/local/bin/em")
            runCommandE('echo "" >> /etc/crontab')
            runCommandE('echo "0 0 * * * root killemacs > /dev/null 2>&1" >> /etc/crontab')

    #vim
    if vim == 1 and update == 0:
        runCommandE("git clone https://github.com/DamZiobro/vim-ide")
        os.chdir("./vim-ide/")
        cmd = "./installVim.sh"
        p = subprocess.Popen(cmd , shell = True)
        p.wait()
        if p.returncode != 0 :
            print("set up vim failed")
        os.chdir("/root/tmp/")
        runCommands("rm -rf ./vim-ide")

    #shadowsocks
    if shadowsocks == 1 and update == 0:
        runCommandE("pip install shadowsocks")
        runCommandE("mkdir -p /etc/shadowsocks/")
        print("plz input server , port , passwd of ss(/etc/shadowsocks/ss.json)")
        server = raw_input("server address:\n")
        port = raw_input("server port:\n")
        passwd = raw_input("server passwd:\n")
        content = '''{
    "server":"''' + server.strip() + '''",
    "server_port":''' + port.strip() + ''',
    "local_port":1080,
    "password":"''' + passwd.strip()+'''",
    "timeout":600,
    "method":"aes-256-cfb"
}
'''

        file = open("/etc/shadowsocks/ss.json", "w")
        file.write(content)
        file.flush()
        file.close()
        runCommandE("cp /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py.bak")
        runCommandE('perl -p -i -e "s/cleanup/reset/g" /usr/local/lib/python2.7/dist-packages/shadowsocks/crypto/openssl.py')
        file = open("/lib/systemd/system/ssc.service" , "w")
        content = """[Unit]
Description=shadowsocks

[Service]
Type=forking
ExecStart=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d start
ExecReload=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d restart
ExecStop=/usr/local/bin/sslocal -c /etc/shadowsocks/ss.json -d stop

[Install]
WantedBy=multi-user.target"""
        file.write(content)
        file.flush()
        file.close()
        runCommandE("systemctl daemon-reload")

        print("usage:systemctl start/stop/reload ssc")

    if update == 0:
        #default editor
        file = open("/root/.zshrc" , "a")
        while 1:
            editor = raw_input("""default editor:
1)vim
2)emacs
> """)
            if editor == '1' or editor == 'vim':
                runCommandE("git config --global core.editor vim")
                file.write('export EDITOR="vim"')
                break
            elif editor == '2' or editor == 'emacs':
                runCommandE("git config --global core.editor em")
                file.write('export EDITOR="em"')
                break
            elif editor == '\n' or editor == '':
                print("keep default")
                break
            else:
                print("input error")
                continue
        file.flush()
        file.close()

        runCommandE("systemctl restart cron")
        runCommand("systemctl restart ssh")
