import os
import shutil
import subprocess

# Files to mutate
FILES = [
    "services/gemini_service.py",
    "audio_processing/recorder.py",
    "audio_processing/transcriber.py",
    "utils/text_loader.py"
]

MUTANT_DIR = "mutants"
REPORT_FILE = "reports/mutation_report.txt"

os.makedirs(MUTANT_DIR, exist_ok=True)
os.makedirs("reports", exist_ok=True)

# 🔥 STRONG MUTATIONS (carefully chosen to be killable)
mutations = [

    # ---- GEMINI (ONLY STRONG 5) ----
    ("all_key_points.extend", "pass"),
    ("all_action_items.extend", "pass"),
    # ("combined_text = \" \".join(all_summaries)", "combined_text = \"\""),
    # ("json.loads(raw_output)", "json.loads(\"{}\")"),
    ("return final_data", "return {\"summary\":\"\",\"key_points\":[],\"action_items\":[]}"),

    # ---- RECORDER (REMOVED weak mutants) ----
    ("if self.is_recording:", "if False:"),
    ("self.recording.append(indata.copy())", "pass"),
    ("self.is_recording = True", "self.is_recording = False"),
    ("np.concatenate(self.recording, axis=0)", "np.array([])"),
    ("np.clip(audio, -1, 1)", "audio"),
    ("return \"conversation.wav\"", "return \"\""),
    ("len(self.recording)", "0"),
    ("audio = np.concatenate", "audio = np.array"),
    # ❌ removed:
    # ("self.stream.stop()", "pass"),
    # ("self.stream.close()", "pass"),

    # ---- TRANSCRIBER ----
    ("return result[\"text\"]", "return \"\""),
    ("result = model.transcribe(file_path)", "result = {\"text\": \"\"}"),
    ("whisper.load_model", "None"),
    ("model.transcribe", "lambda x: {\"text\": \"\"}"),
    ("file_path", "\"\""),

    # ---- TEXT LOADER ----
    ("decode(\"utf-8\")", "decode(\"ascii\")"),
    ("uploaded_file.read()", "b\"\""),
    ("return uploaded_file.read().decode(\"utf-8\")", "return \"\""),
    # ❌ removed:
    # ("uploaded_file.read().decode", "str"),
    ("return uploaded_file.read()", "return b\"\""),
]

# 🔹 Backup all original files
backups = {}
for file in FILES:
    backup = file + ".bak"
    shutil.copy(file, backup)
    backups[file] = backup

mutant_files = []

# 🔹 Generate mutants
for file in FILES:
    with open(file, "r", encoding="utf-8") as f:
        original_code = f.read()

    base = os.path.basename(file).replace(".py", "")

    for i, (old, new) in enumerate(mutations):
        if old in original_code:
            mutated_code = original_code.replace(old, new, 1)

            mutant_name = f"{MUTANT_DIR}/{base}_mutant_{i}.py"

            with open(mutant_name, "w", encoding="utf-8") as f:
                f.write(mutated_code)

            mutant_files.append((mutant_name, file))

print(f"Generated {len(mutant_files)} mutants")

# 🔹 Run tests
killed = 0
survived = 0

try:
    for mutant, original_file in mutant_files:

        # Apply mutant temporarily
        shutil.copy(mutant, original_file)

        result = subprocess.run(
            ["pytest", "-q"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            killed += 1
            status = "KILLED"
        else:
            survived += 1
            status = "SURVIVED"

        print(f"{mutant} -> {status}")

        # Restore immediately
        shutil.copy(backups[original_file], original_file)

finally:
    # FINAL SAFETY RESTORE
    for file, backup in backups.items():
        shutil.copy(backup, file)

# 🔹 Calculate score
total = killed + survived
score = (killed / total) * 100 if total else 0

# 🔹 Save report
with open(REPORT_FILE, "w") as f:
    f.write(f"Total Mutants: {total}\n")
    f.write(f"Killed: {killed}\n")
    f.write(f"Survived: {survived}\n")
    f.write(f"Mutation Score: {score:.2f}%\n")

print("\n=== FINAL REPORT ===")
print(f"Total Mutants: {total}")
print(f"Killed: {killed}")
print(f"Survived: {survived}")
print(f"Mutation Score: {score:.2f}%")