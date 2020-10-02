# Performs necessary setup steps to allow the use of
# virtualenv commands such as "mkvirtualenv [ENV_NAME]"
# for creating and using Python virtual environments.
#
# Run by using the following command: "source virtualenv_install.sh"

[[ $0 != "$BASH_SOURCE" ]] && sourced=1 || sourced=0
if [ $sourced = 1 ]
then
  python3 -m pip install virtualenvwrapper --force-reinstall
  export WORKON_HOME=$HOME/.virtualenvs
  source `which virtualenvwrapper.sh`
  echo ""
  echo ""
  echo "*** You may now use virtualenv commands in your command shell. ***"
  echo ""
  echo "virtualenv commands:"
  echo '  *  "mkvirtualenv [ENV_NAME]"  -  Create a Python virtual environment'
  echo '  *  "deactivate"               -  Exit the current virtual environment'
  echo '  *  "workon [ENV_NAME]"        -  Enter an existing virtual environment'
  echo '  *  "lsvirtualenv" OR "workon" -  List all virtual environments'
  echo '  *  "rmvirtualenv [ENV_NAME]"  -  Delete a virtual environment'
  echo ""
  echo "Example:"
  echo "      mkvirtualenv seleniumbase "
  echo "      mkvirtualenv seleniumbase --python=[PATH_TO_PYTHON]"
  echo ""
else
  echo ""
  echo "--------------------"
  echo '*** - WARNING! - ***'
  echo "--------------------"
  echo ""
  echo 'You need to "source" this file for virtualenv commands to work!'
  echo ""
  echo '*** USE:  source virtualenv_install.sh'
  echo "          ----------------------------"
  echo ""
fi
