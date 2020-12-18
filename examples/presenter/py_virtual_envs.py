from seleniumbase import BaseCase


class PythonVirtualEnvPresentation(BaseCase):

    def test_py_virtual_envs(self):
        self.create_presentation(theme="serif", transition="slide")
        self.add_slide(
            '<h2>Python Virtual Environments:</h2><br />\n'
            '<h2>What, Why, and How</h2><hr /><br />\n'
            '<h3>Presented by <b>Michael Mintz</b></h3>\n'
            '<p>Granite State Code Camp - Sat, Nov 14, 2020</p>')
        self.add_slide(
            '<p><b>About me:</b></p>\n'
            '<ul>'
            '<li>I created the <b>SeleniumBase</b> framework.</li>'
            "<li>I'm currently the DevOps Lead at <b>iboss</b>.</li>"
            '</ul>\n',
            image="https://seleniumbase.io/other/iboss_booth.png")
        self.add_slide(
            '<p><b>Topics & tools covered by this presentation:</b></p>'
            '<hr /><br />\n'
            '<ul>'
            '<li>Overview of Virtual Environments</li>'
            '<li>Python package management</li>'
            '<li>Python 3 "venv"</li>'
            '<li>virtualenv / virtualenvwrapper</li>'
            '<li>pip / "pip install"</li>'
            '<li>requirements.txt files</li>'
            '<li>setup.py files</li>'
            '</ul>')
        self.add_slide(
            '<p><b>Topics & tools that are NOT covered here:</b></p><hr />\n'
            '<br /><div><ul>'
            '<li>"conda"</li>'
            '<li>"pipenv"</li>'
            '<li>"poetry"</li>'
            '<li>"pipx"</li>'
            '</ul></div><br />'
            '<p>(Other Python package management tools)</p>')
        self.add_slide(
            '<p><b>What is a Python virtual environment?</b></p><hr /><br />\n'
            '<p>A Python virtual environment is a partitioned directory'
            ' where a Python interpreter, libraries/packages, and scripts'
            ' can be installed and isolated from those installed in other'
            ' virtual environments or the global environment.</p>')
        self.add_slide(
            '<p><b>Why should we use Python virtual environments?</b>'
            '</p><hr /><br />\n'
            '<p>We should use Python virtual environments because different'
            ' Python projects can have conflicting Python dependencies that'
            ' cannot coexist in the same env.</p>')
        self.add_slide(
            '<p><b>Why? - continued</b></p><hr /><br />\n'
            '<p>Example: Project A and Project B both depend on'
            ' different versions of the same Python library!</p>'
            '<p>Therefore, installing the second project requirements'
            ' would overwrite the first one, causing it to break.</p>',
            code=(
                '# Project A requirement:\n'
                'urllib3==1.25.3\n\n'
                '# Project B requirement:\n'
                'urllib3==1.26.2'))
        self.add_slide(
            '<p><b>Why? - continued</b></p><hr /><br />\n'
            '<p>It is also possible that Project A and Project B'
            ' require different versions of Python installed!</p>',
            code=(
                '# Project A requirement:\n'
                'Python-3.8\n\n'
                '# Project B requirement:\n'
                'Python-2.7'))
        self.add_slide(
            '<p><b>How do we create and use Python virtual envs?</b>'
            '</p><hr /><br />\n'
            '<div><b>There are tools/scripts we can use:</b></div><br />'
            '<ul>'
            '<li>The Python 3 "venv" command</li>'
            '<li>virtualenv / virtualenvwrapper</li>'
            '</ul>')
        self.add_slide(
            '<p><b>Python 3 "venv"</b></p><hr /><br />\n'
            '"venv" creates virtual environments in the location where run'
            ' (generally with Python projects).',
            code=(
                '# Mac / Linux\n'
                'python3 -m venv ENV_NAME\n'
                'source ENV_NAME/bin/activate\n\n'
                '# Windows\n'
                'py -m venv ENV_NAME\n'
                'call ENV_NAME\\Scripts\\activate\n\n'
                '# (Type "deactivate" to leave a virtual environment.)'))
        self.add_slide(
            '<p><b>"mkvirtualenv" (from virtualenvwrapper)</b></p><hr />\n'
            '<br />"mkvirtualenv" creates virtual environments in one place'
            ' (generally in your home directory).',
            code=(
                '# Mac / Linux\n'
                'python3 -m pip install virtualenvwrapper\n'
                'export WORKON_HOME=$HOME/.virtualenvs\n'
                'source `which virtualenvwrapper.sh`\n'
                'mkvirtualenv ENV_NAME\n\n'
                '# Windows\n'
                'py -m pip install virtualenvwrapper-win\n'
                'mkvirtualenv ENV_NAME\n\n'
                '# (Type "deactivate" to leave a virtual environment.)'))
        self.add_slide(
            '<p><b>List of commands from virtualenvwrapper</b></p>'
            '<hr /><br />',
            code=(
                '# Create a virtual environment:\n'
                'mkvirtualenv ENV_NAME\n\n'
                '# Exit your virtual environment:\n'
                'deactivate\n\n'
                '# Re-enter a virtual environment:\n'
                'workon ENV_NAME\n\n'
                '# List all virtual environments:\n'
                'workon\n\n'
                '# Delete a virtual environment:\n'
                'rmvirtualenv ENV_NAME'))
        self.add_slide(
            '<p><b>Determining if you are in a virtual env</b></p>'
            '<hr /><br />'
            '<p>When activated, the name of your virtual env'
            ' will appear in parentheses on the left side of your'
            ' command prompt.</p>',
            code=(
                '# Example of how it may look on a Windows machine:\n'
                'C:\\Users\\Michael\\github> mkvirtualenv my_env\n'
                '(my_env)  C:\\Users\\Michael\\github>'))
        self.add_slide(
            '<p><b>Installing packages with "pip install"</b></p><hr /><br />'
            '<p>Once you have created a Python virtual environment and are'
            ' inside, it is now safe to install packages from PyPI,'
            ' setup.py files, and/or requirements.txt files.</p>\n',
            code=(
                '# Install a package from PyPI:\n'
                'pip install seleniumbase\n\n'
                '# Install packages from a folder with setup.py:\n'
                'pip install .  # Normal installation\n'
                'pip install -e .  # Editable install\n\n'
                '# Install packages from a requirements.txt file:\n'
                'pip install -r requirements.txt\n'))
        self.add_slide(
            '<p><b>Other useful "pip" commands</b></p><hr /><br />',
            code=(
                '# See which Python packages are installed:\n'
                'pip list\n\n'
                '# See which installed Python packages are outdated:\n'
                'pip list --outdated\n\n'
                '# Create a requirements file from installed packages:\n'
                'pip freeze > my_requirements.txt'))
        self.add_slide(
            '<br /><br /><h2><b>Live Demo Time!</b></h2><hr /><br />',
            image="https://seleniumbase.io/other/python_3d_logo.png")
        self.add_slide(
            '<h2><b>The End. Questions?</b></h2><hr /><br />\n'
            '<h3>Where to find me:</h3>'
            '<ul>'
            '<li><a href="https://github.com/mdmintz">'
            'github.com/mdmintz</a></li>'
            '<li><a href="https://github.com/seleniumbase/SeleniumBase">'
            'github.com/seleniumbase/SeleniumBase</a></li>'
            '<li><a href="https://seleniumbase.io/">'
            'seleniumbase.io</a></li>'
            '</ul>')
        self.begin_presentation(
            filename="py_virtual_envs.html", show_notes=False, interval=0)
