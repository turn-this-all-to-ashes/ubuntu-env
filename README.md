# INSTALL
    安装前先配置好网络环境(ip dns等)
    然后设置root用户密码 : sudo passwd root
    切换至root用户  : su - root
    手动安装python : apt-get install -y python
    然后执行以下3步安装:
        wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/install.py -O - | cat > install.py
        chmod +x install.py
        ./install.py
        使用命令行参数指定安装内容:
        -v : vim环境
        -e : emacs环境
        -s : shadowsocks
        --no-rust : 不安装rust
    仅在ubuntu server 18.04中测试通过.


# USAGE
    命令行历史搜索绑定按键: ctrl+p ctrl+n
    autojump : j
    使用sctlstart/sctlstop ssc开启/关闭shadowsocks(配置文件位置:/etc/shadowsocks/ss.json)
    git alias 位于 /root/.gitconfig 中
        co = checkout
        ss = status
        cm = commit -m
        br = branch
        bm = branch -m
        cb = checkout -b
        df = diff
        ls = log --stat
        lp = log -p
        plo = pull origin
        plod = pull origin dev
        pho = push origin

    命令行 alias 位于 /root/.zshrc 中
        alias tarx="tar zxvf"
        alias tarc="tar zcvf"
        alias sctl="systemctl"
        alias sctlstart="systemctl start"
        alias sctlreload="systemctl reload"
        alias sctlstop="systemctl stop"
        alias sctlrestart="systemctl restart"
        alias rmd="rm -rf"

    c -> cd & ls
    em -> 开启emacs server , 若server已开启 则使用client连接
    grepv -> grep $@ | grep -v "grep"
    gtext -> grep -rn $@
    pg -> ps -aux | grep $@ | grep -v "grep"
    finda -> find / -name $@
    findc -> find . -name $@
