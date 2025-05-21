import pyaudio
import speech_recognition as sr

def test_audio_setup():
    print("Testing audio setup...")
    
    # Test PyAudio
    try:
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"\n✅ PyAudio initialized - Found {device_count} audio devices:")
        
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            print(f"  Device {i}: {device_info['name']}")
            
        p.terminate()
    except Exception as e:
        print(f"❌ PyAudio error: {str(e)}")
        return False
    
    # Test Speech Recognition
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\n✅ Speech recognition initialized")
            print("Testing microphone...")
            r.adjust_for_ambient_noise(source)
            print("✅ Microphone working")
    except Exception as e:
        print(f"❌ Speech recognition error: {str(e)}")
        return False
        
    return True

if __name__ == "__main__":
    if test_audio_setup():
        print("\n✅ All audio systems ready")
    else:
        print("\n❌ Audio setup failed")