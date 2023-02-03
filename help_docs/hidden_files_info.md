<!-- SeleniumBase Docs -->

## Showing hidden files on macOS

Depending on your macOS settings, some files may be hidden from view in your Finder window, such as ``.gitignore``.

* On newer versions of macOS, use the following in a Finder window to view hidden files:

Press the **“Command” + “Shift” + “.” (period)** keys at the same time.

(The hidden files will show up as translucent in the folder. If you want to obscure the files again, press the same “Command” + “Shift” + “.” (period) combination.)

* On older versions of macOS, use the following command in a Terminal window to view hidden files, and then reopen the Finder window:

```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
```

More info on that can be found here:<ul>
<li><a href="https://www.defaults-write.com/show-hidden-files-in-os-x-finder/">https://www.defaults-write.com/show-hidden-files-in-os-x-finder/</a></li>
<li><a href="https://www.macworld.co.uk/how-to/mac-software/hidden-files-mac-3520878/">https://www.macworld.co.uk/how-to/mac-software/hidden-files-mac-3520878/</a></li>
<li><a href="https://setapp.com/how-to/show-hidden-files-on-mac">https://setapp.com/how-to/show-hidden-files-on-mac</a></li>
</ul>
