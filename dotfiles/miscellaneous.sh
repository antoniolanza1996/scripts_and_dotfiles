# see hidden files and folders
defaults write com.apple.finder AppleShowAllFiles true && killall Finder

# prevent Conda from activating the base environment by default
conda config --set auto_activate_base false