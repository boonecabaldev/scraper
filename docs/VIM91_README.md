```sh
# Remove any existing vim installations
sudo apt-get remove vim vim-runtime gvim

# Install dependencies
sudo apt-get install -y git libncurses5-dev \
    libgtk2.0-dev libatk1.0-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev \
    python3-dev ruby-dev lua5.1 lua5.1-dev libperl-dev git
    
# Clone Vim repository
cd ~
git clone https://github.com/vim/vim.git

# Navigate to the repository
cd vim

# Checkout the correct branch or tag for Vim 9
# As of now, Vim 9 is not released yet, so we checkout master
git checkout master

# Compile Vim
./configure --with-features=huge \
            --enable-multibyte \
            --enable-rubyinterp=yes \
            --enable-python3interp=yes \
            --with-python3-config-dir=$(python3-config --configdir) \
            --enable-perlinterp=yes \
            --enable-luainterp=yes \
            --enable-gui=gtk2 --enable-cscope --prefix=/usr
make VIMRUNTIMEDIR=/usr/share/vim/vim81

# Install Vim
sudo make install
```
