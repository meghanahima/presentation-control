import speech_recognition as sr
from utilities.overlay import show_caption
import re

# for semantic search of slides with command
from utilities.embeddings import get_best_matching_slide 

recognizer = sr.Recognizer()

def get_voice_command():
    with sr.Microphone() as source:
        show_caption("🎤 Waiting for wake word...")
        audio = recognizer.listen(source, phrase_time_limit=3)

        try:
            phrase = recognizer.recognize_google(audio).lower()
            if phrase.startswith("alexa"):
                show_caption("✅ Wake word detected! Say your command...")
                command_audio = recognizer.listen(source, phrase_time_limit=7)
                command_text = recognizer.recognize_google(command_audio).lower()

                match = re.search(r"slide\s*(\d+)", command_text)
                if match:
                    slide_num = int(match.group(1))
                    return f"goto {slide_num}"

                if "next" in command_text:
                    return "next"
                elif "previous" in command_text or "back" in command_text:
                    return "previous"
                elif command_text.startswith("contextual"):
                    query = command_text.replace("contextual", "").strip()
                    best_idx, best_score = get_best_matching_slide(query)
                    score_percent = round(best_score * 100)
                    show_caption(f"🎯 Moved to slide with {score_percent}% match")
                    return f"goto {best_idx+1}"
                else:
                    show_caption("⚠️ No valid command detected")
                    
            else:
                show_caption("❌ Wake word not detected")

        except sr.UnknownValueError:
            show_caption("😕 Could not understand audio")
        except sr.RequestError:
            show_caption("⚠️ Could not reach Google API")

    return None