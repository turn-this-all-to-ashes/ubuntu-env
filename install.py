#!/usr/bin/env python2

import sys
import commands
import os
import subprocess

class colors:
    BLACK         = '\033[0;30m'
    DARK_GRAY     = '\033[1;30m'
    LIGHT_GRAY    = '\033[0;37m'
    BLUE          = '\033[0;34m'
    LIGHT_BLUE    = '\033[1;34m'
    GREEN         = '\033[0;32m'
    LIGHT_GREEN   = '\033[1;32m'
    CYAN          = '\033[0;36m'
    LIGHT_CYAN    = '\033[1;36m'
    RED           = '\033[0;31m'
    LIGHT_RED     = '\033[1;31m'
    PURPLE        = '\033[0;35m'
    LIGHT_PURPLE  = '\033[1;35m'
    BROWN         = '\033[0;33m'
    YELLOW        = '\033[1;33m'
    WHITE         = '\033[1;37m'
    DEFAULT_COLOR = '\033[00m'
    RED_BOLD      = '\033[01;31m'
    ENDC          = '\033[0m'

def installPackage(pm , packages):
    for package in packages:
        print("")
        print(colors.YELLOW + str(pm+package)+ colors.ENDC)
        p = subprocess.Popen(str(pm+package) , shell = True )
        p.wait()
        if not p.returncode == 0:
            print(colors.RED +"install " + package+" failed"+colors.ENDC)
        print(colors.GREEN + "install " + package + " succeed" + colors.ENDC)
        print("")
    return 0

def runCommandE(command):
    print("")
    print(colors.YELLOW+ command+colors.ENDC)
    p = subprocess.Popen(command , shell = True )
    p.wait()
    if not p.returncode == 0:
        print(colors.RED+"run "+command + " failed"+colors.ENDC)
        print("")
        sys.exit()
    print(colors.GREEN + "run " + command + " succeed" + colors.ENDC)
    print("")
    return p.returncode

def runCommand(command):
    print("")
    print(colors.YELLOW + command + colors.ENDC)
    p = subprocess.Popen(command , shell = True )
    p.wait()
    if not p.returncode == 0:
        print(colors.RED + "run "+command + " failed" +colors.ENDC)
        print("")
    print(colors.GREEN + "run " + command + " succeed" + colors.ENDC)
    print("")
    return p.returncode

def zsh():
    #autojump
    runCommand("git clone git://github.com/wting/autojump.git")
    os.chdir("./autojump")
    (ret , output) = commands.getstatusoutput("./install.py")
    if not ret == 0:
        print(output)
        print("install autojump failed")
        sys.exit()
    output= output.split('\n')
    autojumpconf= []
    for line in output:
        if len(line) == 0:
            continue
        if '[[' in line or 'autoload' in line:
            autojumpconf.append(line)
    os.chdir(home + "/tmp")
    runCommandE("rm -rf ./autojump")
    
    #autosuggestions
    runCommand("git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions")
    #highlighting
    runCommand("git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting")
    #history-substring-search
    runCommand("git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search")
    #.zshrc
    runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/zshrc -O - | cat > " + home + "/.zshrc")
    file = open(home + "/.zshrc" , "a")
    file.write('\n')
    file.write(autojumpconf[0] + '\n')
    file.write(autojumpconf[1] + '\n')
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

    home = (os.environ['HOME']).strip()
    vim = 0
    emacs = 0
    shadowsocks = 0
    norust = 0
    nonfs = 0
    nogolang = 0
    nomysql = 0
    update = 0
    bashhub = 0

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
                if 'bashhub' in args:
                    bashhub = 1

    if len(sys.argv) == 1:
        emacs = 1
        vim =1
        shadowsocks = 1

    if update == 0:
        runCommandE("mkdir -p " +home + "/tmp")
        os.chdir(home+"/tmp")
        runCommandE("mkdir -p " + home + "/nfs/ftp")

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
    packages = ['wget' , 'curl' , 'gcc' , 'g++', 'gdb' ,'git', 'zsh' ,'vim' , 'screen' ,'tree' , 'manpages-posix manpages-posix-dev','htop','zip' , 'tmux','cmake' ,'automake' ,'autoconf'  , 'ctags' , 'global' , 'python-pip' , 'python' , 'python3' ,'python3-pip', 'perl' ,'rar' , 'p7zip' , 'sqlite' , 'curlftpfs' , 'vsftpd' , 'cloc' , 'ack-grep' , 'silversearcher-ag' , 'direnv' , 'googler']
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
        runCommandE("chown -R ftp:ftp " + home + "/nfs/ftp")

    #gitconfig
    if update == 0:
        (ret , output) = commands.getstatusoutput("hostname")
        if not ret == 0:
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/gitconfig -O - | cat > "+ home + "/.gitconfig")
        else:
            email = output.strip() + "@example.com"
            file = open("./tmpgitconfig.tmp" , "w")
            file.write("[user]\n")
            file.write(addtan("email = "+ email))
            file.write(addtan("name = " + output.strip()))
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
            runCommandE("mv ./tmpgitconfig.tmp " + home + "/.gitconfig")

    #zsh
    if update == 0:
        ohmyzsh = "wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh"
        runCommand(ohmyzsh)
        (ret , output) = commands.getstatusoutput("which zsh")
        if not ret == 0:
            runCommandE("chsh -s /usr/bin/zsh" )
        else:
            runCommandE("chsh -s " + output.strip())
        zsh()
        file = open(home + "/.zshrc" , "r")
        content = file.read()
        content = content.split("\n")
        file.close()
        file = open(home+ "/.zshrc" , "w")
        for line in content:
            if 'export ZSH="/root/.oh-my-zsh"' in line:
                file.write('export ZSH="' + home + '/.oh-my-zsh"\n')
                continue
            file.write(line + '\n')
        file.flush()
        file.close()

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
        file = open("/etc/vsftpd.conf" , "a")
        file.write("anon_root="+ home + "/nfs")
        file.flush()
        file.close()
        runCommandE("systemctl restart vsftpd")

    #percol
    if update == 0:
        runCommand("pip install percol")

    #add-gitignore
    if update == 0:
        runCommand("pip install add-gitignore")

    #ad
    if update == 0:
        runCommand("pip3 install advance-touch")

    #autoenv
    if update == 0:
        runCommand("pip install autoenv")
        runCommandE('echo "source `which activate.sh`" >> ~/.zshrc')

    #commandcd
    if update == 0:
        runCommand('curl -sSL https://github.com/shyiko/commacd/raw/v1.0.0/commacd.sh -o ~/.commacd.sh &&  echo "source ~/.commacd.sh" >> ~/.zshrc')
    #bashhub
    if bashhub == 1:
        runCommand("curl -OL https://bashhub.com/setup && zsh setup")
        runCommandE('rm -rf setup')

    #bashmark
    if update == 0:
        runCommand('git clone git://github.com/huyng/bashmarks.git')
        os.chdir('bashmarks')
        runCommand('make install')
        runCommandE('echo "source ~/.local/bin/bashmarks.sh" >> ~/.zprofile')
        os.chdir(home + '/tmp')
        runCommandE('rm -rf bashmarks')
        runCommandE("sed -i 's/function d {/function dmark {/g' ~/.local/bin/bashmarks.sh")

    #bd
    if update == 0:
        runCommandE('wget --no-check-certificate -O /usr/local/bin/bd https://raw.github.com/vigneshwaranr/bd/master/bd')
        runCommandE('chmod +rx /usr/local/bin/bd')
        runCommandE('''echo 'alias bd=". bd -si"' >> ~/.zshrc''')

    #desk
    if update == 0:
        runCommandE('curl https://raw.githubusercontent.com/jamesob/desk/master/desk > /usr/local/bin/desk')
        runCommandE('chmod +x /usr/local/bin/desk')

    #fd
    if update == 0:
        (ret , output) = commands.getstatusoutput("uname -a")
        if ret:
            if 'x86_64' in output:
                runCommandE('wget https://github.com/sharkdp/fd/releases/download/v7.3.0/fd_7.3.0_amd64.deb')
                runCommand('dpkg -i fd_7.3.0_amd64.deb')
                runCommandE('rm -rf fd_7.3.0_amd64.deb')

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
            file = open(home + "/.zprofile" , "a")
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
                network = 'echo "' + home + '/nfs ' + network[0] + "." + network[1]+ "." + network[2] + ".0/24" + '(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports'
            else:
                network = raw_input("input nfs network(e.g. 192.168.0.0/24) :\n")
                network = 'echo "'+ home + '/nfs ' + network + '(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports'
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
            runCommand("git clone https://github.com/purcell/emacs.d.git ~/.emacs.d")
            runCommandE("cp "+ home + "/.emacs.d/init.el "+home +"/.emacs.d/init.el.bak")
            with open(home + "/.emacs.d/init.el.bak" , "r") as file:
                lines = file.readlines()
                file = open(home + "/.emacs.d/init.el" , "w")
                for line in lines:
                    line = line.strip('\n')
                    if line == "(require 'init-xterm)":
                        line = ";;(require 'init-xterm)"
                    file.write(line + "\n")
                file.flush()
                file.close()
            runCommandE("mkdir -p "+ home + "/tmp/obj/")
            os.chdir("/usr/include")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir("/usr/src")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir("/usr/local/include")
            runCommandE("MAKEOBJDIRPREFIX=~/tmp/obj gtags --objdir")
            os.chdir(home + "/tmp")
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/init-local.el -O - | cat > " + home + "/.emacs.d/lisp/init-local.el")
        #em alias
            runCommandE("wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/emacsalias -O - | cat > /usr/local/bin/em")
            runCommandE("chmod +x /usr/local/bin/em")
            runCommandE('echo "" >> /etc/crontab')
            runCommandE('echo "0 0 * * * root killemacs > /dev/null 2>&1" >> /etc/crontab')

    #vim
    if vim == 1 and update == 0:
        runCommand("git clone https://github.com/DamZiobro/vim-ide")
        os.chdir("./vim-ide/")
        cmd = "./installVim.sh"
        p = subprocess.Popen(cmd , shell = True)
        p.wait()
        if p.returncode != 0 :
            print("set up vim failed")
        os.chdir(home + "/tmp/")
        runCommand("rm -rf ./vim-ide")

    #shadowsocks
    if shadowsocks == 1 and update == 0:
        runCommand("pip install shadowsocks")
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
        file = open(home + "/.zshrc" , "a")
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
