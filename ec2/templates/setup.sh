#!/usr/bin/env bash

apt-get update

# install pip and some libraries (for convenience and test scripts)
apt-get install -y \
    python \
    python-dev \
    python-distribute \
    python-pip \
    python-numpy \
    python-scipy \
    git

# python libraries (for convenience and test scripts)
pip install \
	requests==2.5.2 \
	boto

# tools for increased stability of docker volumes
apt-get install -y linux-image-extra-$(uname -r) aufs-tools  

# downloads and installs docker
curl -sSL https://get.docker.com/ubuntu/ | sh

# orchestrates docker containers
pip install docker-compose

# Build Emacs 24.4 From Source
apt-get -y install build-essential
sudo apt-get build-dep emacs24
wget http://ftp.gnu.org/gnu/emacs/emacs-24.4.tar.gz
tar -xzvf emacs-24.4.tar.gz
rm emacs-24.4.tar.gz
cd emacs-24.4
./configure --prefix=/opt/emacs
make
make install
cp src/emacs /usr/bin/emacs
chmod 755 /usr/bin/emacs

# Create Directory For Emacs Config
cd ~
mkdir .emacs.d

# Python Packages Required For Elpy
pip install \
    ipython \
    jedi \
    flake8 \
    importmagic \
    autopep8

# Create init.el
echo ";; Tell Init To Install Required Packages If Not Found
(load \"~/.emacs.d/init-packages\")
" >> .emacs.d/init.el

echo "
;; Auto Initialize Elpy
(package-initialize)
(elpy-enable)
" >> .emacs.d/init.el

echo "
;; Fixing a key binding bug in elpy
(define-key yas-minor-mode-map (kbd \"C-c k\") 'yas-expand)
;; Fixing another key binding bug in iedit mode
(define-key global-map (kbd \"C-c o\") 'iedit-mode)
(elpy-use-ipython)
" >> .emacs.d/init.el

# Create init-packages.el
echo "
(require 'package)

(add-to-list 'package-archives
             '(\"elpy\" . \"http://jorgenschaefer.github.io/packages/\"))

(add-to-list 'package-archives
             '(\"marmalade\" . \"http://marmalade-repo.org/packages/\"))

(add-to-list 'package-archives
             '(\"melpa-stable\" . \"http://melpa-stable.milkbox.net/packages/\") t)

(add-to-list 'load-path \"~/.emacs.d/site-lisp/\")


; list the packages you want
(setq package-list
    '(python-environment deferred epc 
        flycheck ctable jedi concurrent company cyberpunk-theme elpy 
        yasnippet pyvenv highlight-indentation find-file-in-project 
        sql-indent sql exec-path-from-shell iedit
        auto-complete popup let-alist magit
        minimap popup))


; activate all the packages
(package-initialize)

; fetch the list of packages available 
(unless package-archive-contents
  (package-refresh-contents))

; install the missing packages
(dolist (package package-list)
  (unless (package-installed-p package)
    (package-install package)))
" >> .emacs.d/init-packages.el

# Grant Permission To Emacs Config - may want to make priveledges less open
chmod 777 .emacs.d
