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
        -p : 安装依赖以及工具等(通常需要指定)
        -v : vim环境
        -e : emacs环境
        -s : shadowsocks
    仅在ubuntu server 18.04中测试通过.
