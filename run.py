import os
import sys
import subprocess

def main():
    # Base directory of the project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to Python executable inside virtual environment
    if sys.platform == "win32":
        venv_python = os.path.join(base_dir, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(base_dir, "venv", "bin", "python")
        
    if not os.path.exists(venv_python):
        print(f"[ERROR] Virtual environment Python not found at: {venv_python}")
        print("Please check if the 'venv' directory exists.")
        sys.exit(1)
        
    manage_py = os.path.join(base_dir, "manage.py")
    
    # Default to 'runserver' if no extra arguments are passed
    args = sys.argv[1:] if len(sys.argv) > 1 else ["runserver"]

    if args[0].endswith(".py") and os.path.exists(os.path.join(base_dir, args[0])):
        cmd = [venv_python] + args
        print(f"--> Executing Python script using virtual environment: {' '.join(cmd)}\n")
    else:
        cmd = [venv_python, manage_py] + args
        print(f"--> Executing Django command using virtual environment: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n--> Execution stopped.")

if __name__ == '__main__':
    main()
