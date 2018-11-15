# Introduction to Machine Learning (presentation/code snippets)

## Repository content

- Presentation slides itself (in .pdf file or link to gdrive presentation).
- <i>facial_analysis_demo.py</i> - simple program that captures image from
computer camera. Once space is pressed, it detects faces and camera and displays
basic analysis (gender, age range, emotion) of faces found
(detailed results are printed as well). Another space press discards
last analysis and starts displaying live image from camera once again.
- <i>voice_synthesize_demo.py</i> command line script, that takes one
argument, text to be synthesized to voice and plays it.
- Jupyter notebook (<i>regression_example.ipynb</i>) with simple linear
 regression example (predicting salary based on years of experiance), together with used data.

## Getting Started

### Prerequisites

All examples are in Python - so it is mandatory. <br/>
List of required additional packages can be found in <i>requirements.txt</i>

###### Other requirements
- voice synthesis example require VLC installed to actually play .mp3
from response (https://www.videolan.org/vlc/).
- facial analysis example require working and enabled camera (for quite obivious reasons).
- <b><u>Important</u></b>: Code snippets also require AWS account set up,
along with user credentials/keys configured on local machine - this is
rather straightforward, but won't be described here.

### Installing

First step is to clone the code to the local machine using *git clone*:

```
git clone https://gitlab.com/Inteneural/Pipeline.git
```

After that, install required python packages using requirements.txt file:
```
pip install -r requirements.txt
```

Assuming that you fulfilled requirements from previous section you are
pretty much <br/>ready to go - just run scripts with python or notebook using
jupyter server.

Have fun :)