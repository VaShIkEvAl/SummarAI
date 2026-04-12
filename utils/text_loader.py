def load_text_from_file(uploaded_file):
    print("📂 Processing uploaded .txt file...")  # Console log
    return uploaded_file.read().decode("utf-8")