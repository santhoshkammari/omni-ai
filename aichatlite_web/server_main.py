import subprocess
import time

def serve():
    print("🚀 Starting OmniAI Chat App...")
    print("🔧 Initializing...")

    # Start the Streamlit server using subprocess
    process = subprocess.Popen(
        ["streamlit", "run", "core/streamlit_app.py", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="aichatlite"  # Ensure the current working directory is correct
    )

    print("🌐 Starting Streamlit server...")

    # Capture and print the output from the subprocess
    try:
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is None:
                break
            if output:
                print(output.decode().strip())
    except KeyboardInterrupt:
        print("Shutting down the server...")
        process.terminate()
        process.wait()
        print("Server has been shut down.")

    # Capture and print any errors
    error_output = process.stderr.read()
    if error_output:
        print("Error output from Streamlit server:")
        print(error_output.decode().strip())

    # Ensure the process continues to run
    process.communicate()