### Info about hidden files on macOS

Depending on your macOS settings, some files may be hidden from view in your Finder window, such as ``.gitignore``. To view all files, run the following command and then reopen the Finder window:
```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
```

More info on that **[here](https://www.defaults-write.com/show-hidden-files-in-os-x-finder/)**.
