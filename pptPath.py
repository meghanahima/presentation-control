import os

# Get absolute path to the PowerPoint file
base_dir = os.path.dirname(os.path.abspath(__file__))
ppt_path = os.path.join(base_dir, "my.pptx")

# Validate the path exists
if not os.path.exists(ppt_path):
    raise FileNotFoundError(f"PowerPoint file not found at: {ppt_path}")