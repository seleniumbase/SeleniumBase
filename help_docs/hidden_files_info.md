### Info about hidden files on a Mac

Depending on your Mac settings, some files may be hidden from view in your Finder window, such as ``.gitignore``. To view all files, run the following command and then reopen the Finder window:
```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
```
