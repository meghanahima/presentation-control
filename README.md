# presentation-control
documentation - https://docs.google.com/document/d/1_VJ6UWcJNRdVt3eLA15h9HtA-SPrH26NXxdi8neYkLQ/edit?usp=sharing

1st version: https://github.com/meghanahima/presentation-control/tree/presentation-control-with-gestures

Gesture control module
Uses win32com to open powerpoint presentation
CV Zone - open CV (video capturing) + mediapipe (for detecting hands, face, pose)


2nd version: https://github.com/meghanahima/presentation-control/tree/voice-commands-and-gesture-controlled-ppt

Has main.py
And the utilities are gesture, voice, presentation_control
I have used speech recognition library and if wake word detected then taking commands like next, previous, and goto slide number

3rd version - Semantic search
https://github.com/meghanahima/presentation-control/tree/semantic-search-with-SBERT

Approach being used here: SBERT + cosine similarity
Extract Slide Content
Semantic Embedding of Slides using SBERT
Process Voice Command → Text → Embedding
cosine similarity to find best matching slide
Evaluating accuracy

Colab link for evaluating the accuracy and errors:
https://colab.research.google.com/drive/10wqCi495fUVeP1YqGqbnWNJM9rAS8TXS?usp=sharing

Libraries used: 
Python–pptx -> used for extracting text from slides, 
Sentence-transformers -> This library has models for generating embeddings and returns a tensor
