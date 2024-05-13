<<<<<<< HEAD
[catalog](https://newtrade6699.x.yupoo.com/albums)
=======
- [catalog](https://newtrade6699.x.yupoo.com/albums)
- [other catalog](https://www.alibaba.com/product-detail/Factory-Whole-Sale-Acrylic-Shield-Black_1600133321560.html)

```sh
sudo apt-get install -y git libncurses5-dev libgnome2-dev libgnomeui-dev \
    libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev \
    python3-dev ruby-dev lua5.1 lua5.1-dev libperl-dev git

sudo apt-get remove vim vim-runtime gvim

git clone https://github.com/vim/vim.git

cd vim

./configure --with-features=huge \
            --enable-multibyte \
            --enable-rubyinterp=yes \
            --enable-python3interp=yes \
            --with-python3-config-dir=$(python3-config --configdir) \
            --enable-perlinterp=yes \
            --enable-luainterp=yes \
            --enable-gui=gtk2 --enable-cscope --prefix=/usr
make VIMRUNTIMEDIR=/usr/share/vim/vim82

sudo make install

vim --version
```
>>>>>>> 163d6fe (init commit)
