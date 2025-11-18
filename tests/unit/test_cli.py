import subprocess

def test_cli_save_and_history():
    cmd = [
        "python", "cli/main.py", 
        "save",
        "--repo=https://github.com/demo",
        "--status=FAILED",
        "--log=SampleLog"
    ]
    subprocess.run(cmd, check=True)

    result = subprocess.run(
        ["python", "cli/main.py", "history"],
        capture_output=True,
        text=True
    )

    assert "https://github.com/demo" in result.stdout
