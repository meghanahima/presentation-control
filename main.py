import cv2
import sys
import threading
from utilities.gesture import detect_gesture
from utilities.ppt_control import next_slide, previous_slide, presentation, close_presentation, goto_slide
from utilities.voice import get_voice_command
from utilities.overlay import overlay

cap = cv2.VideoCapture(0)
exit_requested = False

def shutdown(reason):
    global exit_requested
    exit_requested = True
    print(f"❌ Fatal error: {reason}")
    try:
        overlay.root.quit()
    except:
        pass

def safe_enqueue_slide(action):
    if exit_requested:
        return
    try:
        if action == "next":
            overlay.push_command(lambda: next_slide())
        elif action == "previous":
            overlay.push_command(lambda: previous_slide())
        elif "goto" in action:
            arr = action.split(" ")
            overlay.push_command(lambda: goto_slide(int(arr[1])))
    except Exception as e:
        shutdown(f"PPT enqueue error in {action}: {e}")

def listen_to_voice():
    while not exit_requested:
        try:
            command = get_voice_command()
            if command:
                safe_enqueue_slide(command)
        except Exception as e:
            shutdown(f"Voice thread error: {e}")
            break

# debounce variables
gestureIdentified = False
delay = 50
counter = 0

def gesture_loop():
    global gestureIdentified, delay, counter
    while not exit_requested:
        try:
            success, frame = cap.read()
            if not success:
                shutdown("Could not access webcam")
                break
            if not gestureIdentified:
                gesture = detect_gesture(frame)
                if gesture:
                    safe_enqueue_slide(gesture)
                    gestureIdentified = True

            if gestureIdentified:
                counter+=1
                if counter>delay:
                    gestureIdentified = False
                    counter = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("👋 Exit requested by user")
                shutdown("User quit")
                break
        except Exception as e:
            shutdown(f"Gesture loop error: {e}")
            break

# Start threads
voice_thread = threading.Thread(target=listen_to_voice, daemon=True)
gesture_thread = threading.Thread(target=gesture_loop)

voice_thread.start()
gesture_thread.start()

# Start overlay (main thread)
try:
    overlay.run()
except Exception as e:
    print(f"❌ Overlay error: {e}")
finally:
    print("🧹 Main thread cleanup")
    try:
        close_presentation()
    except:
        pass
    try:
        cap.release()
    except:
        pass
    try:
        cv2.destroyAllWindows()
    except:
        pass
