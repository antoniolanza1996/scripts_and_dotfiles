# see hidden files and folders
defaults write com.apple.finder AppleShowAllFiles true && killall Finder

# prevent Conda from activating the base environment by default
conda config --set auto_activate_base false

# auto-close Apple Terminal window after "exit" command
# Let's follow these instructions: https://stackoverflow.com/a/17910412
