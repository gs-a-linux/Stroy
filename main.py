#!/usr/bin/env python3
import os
import json
import subprocess
import getpass
from openai import OpenAI

# The installer will replace this placeholder
API_KEY = "YOUR_GROQ_API_KEY_HERE"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# --- TRIAL DISCLAIMER ---
TRIAL_MSG = """
****************************************************
* STROY TERMINAL - AETHER OS v1.0 (TRIAL VERSION)  *
* Warning: This version may not work as expected.  *
* Use with caution. Do not run destructive commands.*
****************************************************
"""

MEMORY_FILE = "aether_memory.json"
history = []

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f: return json.load(f)
    return {"notes": []}

print(TRIAL_MSG)
SYSTEM_PASS = getpass.getpass(prompt="System Password (for sudo): ")
long_term_memory = load_memory()

def execute_stroy(user_input):
    global history
    print("*#@ [TRIAL] Analyzing...")

    system_prompt = f"""
    You are the trial intelligence of Aether OS. 
    Memory: {json.dumps(long_term_memory)}
    Protocol: Output ONLY raw bash code. Use 'sudo -S' for root.
    If unsure, output a comment: # TRIAL_WARNING: Command might be unstable.
    """

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-6:]) # Last 3 turns
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.2 # Slight randomness for trial variety
        )

        full_output = response.choices[0].message.content.strip()
        
        # Execute only if it's not just a warning
        cmd = "\n".join([l for l in full_output.split('\n') if not l.startswith('#')])
        
        if cmd:
            if "sudo " in cmd:
                final_cmd = f"echo '{SYSTEM_PASS}' | {cmd.replace('sudo ', 'sudo -S ')}"
            else:
                final_cmd = cmd

            proc = subprocess.run(final_cmd, shell=True, capture_output=True, text=True)

            if proc.returncode == 0:
                print("*()( SUCCESS")
                if proc.stdout: print(proc.stdout)
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": f"Ran: {cmd}"})
            else:
                print(f"!!!! FAILED (Code {proc.returncode})")
                print(proc.stderr)
    except Exception as e:
        print(f"!!!! TRIAL ERROR: {e}")

if __name__ == "__main__":
    while True:
        query = input("Aether[Trial]@Shock:~$ ")
        if query.lower() in ['exit', 'quit']: break
        execute_stroy(query)