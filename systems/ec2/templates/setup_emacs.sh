#!/usr/bin/env bash

# Build Emacs 24.4 From Source
#apt-get -y install build-essential
#sudo apt-get build-dep emacs24
#wget http://ftp.gnu.org/gnu/emacs/emacs-24.4.tar.gz
#tar -xzvf emacs-24.4.tar.gz
#rm emacs-24.4.tar.gz
#cd emacs-24.4
#./configure --prefix=/opt/emacs
#make
#make install
#cp src/emacs /usr/bin/emacs
#chmod 755 /usr/bin/emacs

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

echo "
;; create an emacs server upon startup
;;(server-start)
;;(setq server-socket-dir (format \"/tmp/emacs%d\" (user-uid)))
" >> .emacs.d/init.el

echo "
;; Used in IntelliJ External Tools Open in Emacs - Certified
(set-default 'server-socket-dir \"~/.emacs.d/server\")
(if (functionp 'window-system)
    (when (and (window-system)
		 (>= emacs-major-version 24))
	 (server-start)))
" >> .emacs.d/init.el

echo "
;; Added For Latex
(setq TeX-PDF-mode t)  ;; Automatically compile to PDF
;; (require 'tex)
;; (TeX-global-PDF-mode t)
" >> .emacs.d/init.el

echo "
;; LaTeX Listing for scheme from : https://github.com/stuhlmueller/scheme-listings
(setenv \"TEXINPUTS\" (concat \"/Users/ikinsella/Code/LaTeX/scheme-listings/:\" (getenv \"TEXINPUTS\")))  
" >> .emacs.d/init.el

echo "
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-faces-vector
   [default default default italic underline success warning error])
 '(ansi-color-names-vector
   [\"#212526\" \"#ff4b4b\" \"#b4fa70\" \"#fce94f\" \"#729fcf\" \"#e090d7\" \"#8cc4ff\" \"#eeeeec\"])
 '(custom-enabled-themes (quote (wheatgrass))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
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

(add-to-list 'package-archives
	     '(\"melpa\" . \"http://melpa.org/packages/\") t)

(add-to-list 'load-path \"~/.emacs.d/site-lisp/\")


; list the packages you want
(setq package-list
    '(ac-math auctex auctex-latexmk auto-complete async
       blank-mode
       cdlatex company concurrent context-coloring csv-mode ctable cyberpunk-theme
       dash deferred 
       electric-spacing elpy ein epc exec-path-from-shell
       f find-file-in-project flycheck flylisp
       heap helm highlight-indentation
       idomenu iedit
       jedi js2-mode
       latex-extra latex-preview-pane let-alist
       magit math-symbols math-symbol-lists memory-usage minimap
       popup pyvenv python-environment
       queue
       rainbow-mode request
       s serverspec sql-indent sql 
       undo-tree
       vlf
       w3 websocket
       yasnippet))



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
chmod 755 .emacs.d
