import os
import sys
import tempfile
import shutil
import yaml


def test_mkdir_with_gha_flag():
    from seleniumbase.console_scripts import sb_mkdir
    import sys as sys_module
    
    original_argv = sys_module.argv
    original_cwd = os.getcwd()
    
    temp_dir = tempfile.mkdtemp()
    try:
        os.chdir(temp_dir)
        
        test_dir = "test_gha_dir"
        sys_module.argv = ["sbase", "mkdir", test_dir, "--gha"]
        
        sb_mkdir.main()
        
        workflow_file = os.path.join(test_dir, ".github", "workflows", "seleniumbase.yml")
        assert os.path.exists(workflow_file), "Workflow file should be created"
        
        with open(workflow_file, "r") as f:
            content = f.read()
        
        assert "name: SeleniumBase Tests" in content
        assert "on:" in content
        assert "push:" in content
        assert "pull_request:" in content
        assert "jobs:" in content
        assert "test:" in content
        assert "runs-on: ${{ matrix.os }}" in content
        assert "strategy:" in content
        assert "matrix:" in content
        assert "python-version:" in content
        assert "browser:" in content
        assert "os:" in content
        assert "actions/checkout@v3" in content
        assert "actions/setup-python@v4" in content
        assert "cache: 'pip'" in content
        assert "pip install -r requirements.txt" in content
        assert "pytest --browser=${{ matrix.browser }} --headless" in content
        assert "actions/upload-artifact@v3" in content
        assert "latest_logs/**" in content
        
        workflow_data = yaml.safe_load(content)
        assert "on" in workflow_data
        assert "jobs" in workflow_data
        assert "test" in workflow_data["jobs"]
        assert "steps" in workflow_data["jobs"]["test"]
        
    finally:
        os.chdir(original_cwd)
        sys_module.argv = original_argv
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_mkdir_with_gha_custom_params():
    from seleniumbase.console_scripts import sb_mkdir
    import sys as sys_module
    
    original_argv = sys_module.argv
    original_cwd = os.getcwd()
    
    temp_dir = tempfile.mkdtemp()
    try:
        os.chdir(temp_dir)
        
        test_dir = "test_gha_custom"
        sys_module.argv = [
            "sbase", "mkdir", test_dir, "--gha",
            "--gha-browsers=chrome,firefox",
            "--gha-python=3.10,3.11",
            "--gha-os=ubuntu-latest,windows-latest"
        ]
        
        sb_mkdir.main()
        
        workflow_file = os.path.join(test_dir, ".github", "workflows", "seleniumbase.yml")
        assert os.path.exists(workflow_file), "Workflow file should be created"
        
        with open(workflow_file, "r") as f:
            content = f.read()
        
        assert '"chrome"' in content
        assert '"firefox"' in content
        assert '"3.10"' in content
        assert '"3.11"' in content
        assert '"ubuntu-latest"' in content
        assert '"windows-latest"' in content
        
        workflow_data = yaml.safe_load(content)
        matrix = workflow_data["jobs"]["test"]["strategy"]["matrix"]
        assert "chrome" in matrix["browser"]
        assert "firefox" in matrix["browser"]
        assert "3.10" in matrix["python-version"]
        assert "3.11" in matrix["python-version"]
        assert "ubuntu-latest" in matrix["os"]
        assert "windows-latest" in matrix["os"]
        
    finally:
        os.chdir(original_cwd)
        sys_module.argv = original_argv
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_mkdir_with_basic_and_gha():
    from seleniumbase.console_scripts import sb_mkdir
    import sys as sys_module
    
    original_argv = sys_module.argv
    original_cwd = os.getcwd()
    
    temp_dir = tempfile.mkdtemp()
    try:
        os.chdir(temp_dir)
        
        test_dir = "test_basic_gha"
        sys_module.argv = ["sbase", "mkdir", test_dir, "--basic", "--gha"]
        
        sb_mkdir.main()
        
        workflow_file = os.path.join(test_dir, ".github", "workflows", "seleniumbase.yml")
        assert os.path.exists(workflow_file), "Workflow file should be created with --basic --gha"
        
        requirements_file = os.path.join(test_dir, "requirements.txt")
        assert os.path.exists(requirements_file), "requirements.txt should exist in basic mode"
        
        pytest_ini_file = os.path.join(test_dir, "pytest.ini")
        assert os.path.exists(pytest_ini_file), "pytest.ini should exist in basic mode"
        
        test_files_exist = any(
            f.endswith("_test.py") or f.startswith("test_")
            for f in os.listdir(test_dir)
            if os.path.isfile(os.path.join(test_dir, f))
        )
        assert not test_files_exist, "No test files should exist in basic mode"
        
    finally:
        os.chdir(original_cwd)
        sys_module.argv = original_argv
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_mkdir_gha_workflow_already_exists_error():
    from seleniumbase.console_scripts import sb_mkdir
    import sys as sys_module
    
    original_argv = sys_module.argv
    original_cwd = os.getcwd()
    
    temp_dir = tempfile.mkdtemp()
    try:
        os.chdir(temp_dir)
        
        test_dir = "test_gha_exists"
        os.makedirs(test_dir)
        workflow_dir = os.path.join(test_dir, ".github", "workflows")
        os.makedirs(workflow_dir, exist_ok=True)
        workflow_file = os.path.join(workflow_dir, "seleniumbase.yml")
        with open(workflow_file, "w") as f:
            f.write("existing workflow")
        
        sys_module.argv = ["sbase", "mkdir", test_dir, "--gha"]
        try:
            sb_mkdir.main()
            assert False, "Should raise an error when directory already exists"
        except Exception as e:
            assert "already exists" in str(e).lower() or "ERROR" in str(e)
        
    finally:
        os.chdir(original_cwd)
        sys_module.argv = original_argv
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

