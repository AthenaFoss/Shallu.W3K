import os
import subprocess
import sqlite3

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        exit(1)

def create_directories():
    directories = [
        "databases/master",
        "databases/default_pipeline_vdb",
        "databases/support-ticket"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def setup_databases():
    # Setup master database
    conn = sqlite3.connect("databases/master/master.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_answer_pairs (
            id TEXT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Created master database")

    # Setup support ticket database
    conn = sqlite3.connect("databases/support-ticket/support-ticket.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id TEXT PRIMARY KEY,
            question TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Created support ticket database")

def main():
    print("\n========================")
    print("INSTALLING REQUIREMENTS...")
    print("========================")
    run_command("pip3 install -r requirements_base.txt")

    print("\n========================")
    print("INSTALLING PYTORCH WITH CUDA SUPPORT...")
    print("========================")
    run_command("pip install torch==2.3.1+cu118 torchvision==0.18.1+cu118 torchaudio==2.3.1+cu118 --index-url https://download.pytorch.org/whl/cu118")


    print("\n=====================")
    print("CREATING DIRECTORIES...")
    print("=====================")
    create_directories()

    print("\n======================")
    print("SETTING UP DATABASES...")
    print("======================")
    setup_databases()

    print("\n===========================")
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("===========================")
    

if __name__ == "__main__":
    main()
    print("""
          


███████ ██   ██  █████  ██      ██      ██    ██    ██     ██ ██████  ██   ██ 
██      ██   ██ ██   ██ ██      ██      ██    ██    ██     ██      ██ ██  ██  
███████ ███████ ███████ ██      ██      ██    ██    ██  █  ██  █████  █████   
     ██ ██   ██ ██   ██ ██      ██      ██    ██    ██ ███ ██      ██ ██  ██  
███████ ██   ██ ██   ██ ███████ ███████  ██████  ██  ███ ███  ██████  ██   ██   v1.0.1
                                                                                                                                                                                                           

                                               
""")