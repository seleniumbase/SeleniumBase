<h2><img src="https://seleniumbase.io/img/logo6.png" title="SeleniumBase" width="32" /> Info about hidden files on macOS</h2>

Depending on your macOS settings, some files may be hidden from view in your Finder window, such as ``.gitignore``. To view all files, run the following command and then reopen the Finder window:

```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
```

More info on that can be found here:<ul>
<li><a href="https://www.defaults-write.com/show-hidden-files-in-os-x-finder/">https://www.defaults-write.com/show-hidden-files-in-os-x-finder/</a></li>
<li><a href="https://www.macworld.co.uk/how-to/mac-software/hidden-files-mac-3520878/">https://www.macworld.co.uk/how-to/mac-software/hidden-files-mac-3520878/</a></li>
<li><a href="https://setapp.com/how-to/show-hidden-files-on-mac">https://setapp.com/how-to/show-hidden-files-on-mac</a></li>
</ul>
