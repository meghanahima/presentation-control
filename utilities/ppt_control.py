import win32com.client
from utilities import overlay

powerpoint = win32com.client.Dispatch("Powerpoint.Application")
presentation = powerpoint.Presentations.Open(r"M:\presentation-control\demoPPT.pptx")
presentation.SlideShowSettings.Run()

totalSlides = presentation.Slides.Count
currentSlide = 1

def next_slide():
    global currentSlide

    if currentSlide < totalSlides:
        presentation.SlideShowWindow.View.Next()
        currentSlide += 1
        overlay.show_caption("moved to next slide")


def previous_slide():
    global currentSlide
    if currentSlide > 1:
        presentation.SlideShowWindow.View.Previous()
        currentSlide -= 1
        overlay.show_caption("moved to previous slide")

def goto_slide(slideNumber):
    global totalSlides, currentSlide
    if slideNumber <= totalSlides and slideNumber>0:
        presentation.SlideShowWindow.View.GotoSlide(slideNumber)
        currentSlide = slideNumber
    else:
        overlay.show_caption(f"Slide of {slideNumber} does not exist")


def close_presentation():
    print("close_presentation being called")
    if not presentation:
        return
    try:
        presentation.SlideShowWindow.View.Exit()
        presentation.Close()
        powerpoint.Quit()
    except Exception as e:
        print(f"⚠️ Error closing PowerPoint: {e}")