# INSTALL

测试系统版本: ubuntu server 18.04  

安装前先配置好网络环境(ip dns等)

设置root用户密码 : 

```shell
sudo passwd root
```

切换至root用户

```shell
su - root
```

手动安装python

```shell
apt-get install -y python
```

获取安装脚本   添加执行权限   执行安装

```shell
wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/install.py -O - | cat > install.py
chmod +x install.py
./install.py
```

| 使用命令行参数指定安装细节 |             |
| -------------------------- | ----------- |
| -v                         | vim         |
| -e                         | emacs       |
| -s                         | shadowsocks |
| --no-rust                  | 不安装rust  |

默认则全部安装

# USAGE

| 命令                   | 介绍                                                        |
| ---------------------- | ----------------------------------------------------------- |
| j                      | autojump                                                    |
| ctrl + p /ctrl + n     | 命令行历史搜索                                              |
| tarx                   | tar zxvf                                                    |
| tarc                   | tar zcvf                                                    |
| sctl                   | systemctl                                                   |
| sctlstart              | systemctl start                                             |
| sctlreload             | systemctl reload                                            |
| sctlstop               | systemctl stop                                              |
| sctlrestart            | systemctl restart                                           |
| rmd                    | rm -rf                                                      |
| sctlstart/sctlstop ssc | 开启/关闭shadowsocks(配置文件位置:/etc/shadowsocks/ss.json) |
| git co                 | git checkout                                                |
| git ss                 | git status                                                  |
| git cm                 | git commit -m                                               |
| git br                 | git branch                                                  |
| git bm                 | git branch -m                                               |
| git cb                 | git checkout -b                                             |
| git df                 | git diff                                                    |
| git ls                 | git log --stat                                              |
| git lp                 | git log -p                                                  |
| git plo                | git pull origin                                             |
| git plod               | git pull origin dev                                         |
| git pho                | git push origin                                             |
| c                      | cd & ls                                                     |
| em                     | 开启emacs server 并且使用client连接                         |
| grepv                  | grep $@ \| grep -v "grep"                                   |
| gtext                  | grep -rn $@                                                 |
| pg                     | ps -aux \| grep $@ \| grep -v "grep"                        |
| finda                  | find / -name $@                                             |
| findc                  | find . -name $@                                             |
