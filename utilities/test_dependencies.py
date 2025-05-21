def verify_dependencies():
    dependencies = {
        'cv2': 'OpenCV',
        'mediapipe': 'Mediapipe',
        'win32com.client': 'PyWin32',
        'cvzone': 'CVZone',
        'pyaudio': 'PyAudio',
        'speech_recognition': 'Speech Recognition',
        'numpy': 'NumPy',
        'pptx': 'python-pptx',
        'PIL': 'Pillow',
        'sentence_transformers': 'sentence-transformers'
    }
    
    missing_deps = []
    print("Checking dependencies...")
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError as e:
            print(f"❌ {name} not installed")
            missing_deps.append(name)
    
    if missing_deps:
        print("\nMissing dependencies:")
        print("Run these commands to install:")
        print("pip install -r requirements.txt")
        if 'PyAudio' in missing_deps:
            print("\nIf PyAudio fails to install, try:")
            print("pip install pipwin")
            print("pipwin install pyaudio")
        return False
    
    return True

if __name__ == "__main__":
    if verify_dependencies():
        print("\n✅ All dependencies installed")
    else:
        print("\n❌ Some dependencies missing")