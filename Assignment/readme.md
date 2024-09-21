pip install pandas requests numpy pydub pygame

Run the Script: python tidal_audio_visualization.py

Expected Output:
The audio will be played back automatically, with tones generated according to the tidal heights.
A particle system will visualize the tidal data in real time, with particles representing different heights dynamically moving on the screen.

Overview
Web Scraping: The script uses the requests library to fetch tidal data and pandas to process it into a usable format.
Audio Generation: The pydub library generates sound waves based on the tidal heights, with frequency modulation reflecting the height of the tides.
Visualization: The pygame library is used to create a graphical representation, where particles move vertically based on the tidal data.
