import win32com.client
import os
from utilities import overlay
from pptPath import ppt_path

powerpoint = None
presentation = None
totalSlides = 0
currentSlide = 1

def initialize_powerpoint():
    global powerpoint, presentation, totalSlides
    try:
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        if not os.path.exists(ppt_path):
            raise FileNotFoundError(f"PowerPoint file not found: {ppt_path}")
            
        presentation = powerpoint.Presentations.Open(os.path.abspath(ppt_path))
        presentation.SlideShowSettings.Run()
        totalSlides = presentation.Slides.Count
        return True
    except Exception as e:
        print(f"PowerPoint initialization error: {e}")
        raise

initialize_powerpoint()

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