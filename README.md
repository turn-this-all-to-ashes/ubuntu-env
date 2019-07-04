# INSTALL
    安装前先配置好网络环境(ip dns等)
    然后设置root用户密码 : sudo passwd root
    切换至root用户  : su - root
    手动安装python : apt-get install -y python
    然后执行以下3步安装:
        wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/install.py -O - | cat > install.py
        chmod +x install.py
        ./install.py
    仅在ubuntu server 18.04中测试通过.
