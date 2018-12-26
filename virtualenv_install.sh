# Performs necessary setup steps to allow the use of
# virtualenv commands such as "mkvirtualenv [ENV_NAME]"
# for creating and using Python virtual environments.
#
# Run by using the following command: "source virtualenv_install.sh"

python -m pip install --upgrade virtualenv
python -m pip install --upgrade virtualenvwrapper
source `which virtualenvwrapper.sh`
export WORKON_HOME=$HOME/.virtualenvs
echo ""
echo ""
echo 'virtualenv commands will only work if you installed this using "source":'
echo '    ***  "source virtualenv_install.sh"  ***'
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
echo ""
