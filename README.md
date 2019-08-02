# INSTALL

测试系统版本: ubuntu server 18.04  

安装前先配置好网络环境(ip dns等)

手动安装python

```shell
apt-get install -y python
```

获取安装脚本   添加执行权限   执行安装

```shell
wget https://github.com/turn-this-all-to-ashes/ubuntu-env/raw/master/install.py -O - | cat > install.py
chmod +x install.py
./install.py -v --no-rust --no-golang
```

若使用费root用户安装  使用sudo执行安装脚本. 并在安装结束后手动执行以下命令, 其中user为当前用户:
```
sudo chown -R user:user /home/user
sudo chown -R ftp:ftp /home/user/nfs/ftp
chsh -s /usr/bin/zsh
```

| 使用命令行参数指定安装细节 |             |
| -------------------------- | ----------- |
| -v                         | vim         |
| -e                         | emacs       |
| -s                         | shadowsocks |
| --no-rust                  | 不安装rust  |
| --no-nfs                   | 不安装nfs   |
| --no-mysql                 | 不安装mysql |
| --no-golang                | 不安装golang|

默认则全部安装

大部分用户可以使用 ./install -v --no-rust --no-golang

安装后/root/nfs 文件夹作为nfs和ftp的根目录  建议保留.

# USAGE

| 命令                   | 介绍                                                        |
| ---------------------- | ----------------------------------------------------------- |
| j                      | <https://github.com/wting/autojump>                          |
| add-gitignore           | <https://github.com/fanny/add-gitignore> |
| fzf                     | <https://github.com/junegunn/fzf>                     |
| ctrl + p /ctrl + n     | <https://github.com/zsh-users/zsh-history-substring-search> |
| tarx(alias)         | tar zxvf                                                    |
| tarc(alias)            | tar zcvf                                                    |
| sctl(alias)         | systemctl                                                   |
| sctlstart(alias)       | systemctl start                                             |
| sctlreload(alias)      | systemctl reload                                            |
| sctlstop(alias)   | systemctl stop                                              |
| sctlrestart(alias)     | systemctl restart                                           |
| rmd(alias)             | rm -rf                                                      |
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
| /root/nfs              | nfs目录                                                    |
| /root/nfs              | ftp目录,可以再windows下直接挂载网络位置,或在linux下使用curlftpfs挂载  |
| netstats               | netstat -anp                                                |
| sshcopyid              | ssh-copy-id -i /root/.ssh/ip_rsa.pub root@$@                |
| s/g/dmark/l | <https://github.com/huyng/bashmarks> |
| ad | <https://github.com/tanrax/terminal-AdvancedNewFile> |
| autoenv | <https://github.com/kennethreitz/autoenv> |
| bd | <https://github.com/vigneshwaranr/bd> |
| , | <https://github.com/shyiko/commacd> |
| desk | <https://github.com/jamesob/desk> |
| direnv | <https://github.com/direnv/direnv> |
| fd | <https://github.com/sharkdp/fd> |
| percol | <https://github.com/mooz/percol> |
| googler | <https://github.com/jarun/googler> |
| cloc | <https://github.com/AlDanial/cloc> |
| ack | <https://github.com/petdance/ack2> |
| ag | <https://github.com/ggreer/the_silver_searcher> |
| curlftpfs | <http://curlftpfs.sourceforge.net/> |

