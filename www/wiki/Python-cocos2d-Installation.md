# Python cocos2d Installation

Notes for installing the cocos2d game framework in Python, from the ground up.

# Mac OS X

This is a very low level, ground-up list of steps. Skip some if you've already gotten some of these out of the way before.

1. Install homebrew
2. Install Python: `brew install python`
3. Install cocos2d: `pip install cocos2d`

Install was surprisingly simple (no need to get OpenGL dependencies? I did have Xcode installed, though).

# Python 3

Works in Python 3! OS X instructions:

1. `brew install python3`
2. `mkdir ~/.venv`
3. `pyvenv ~/.venv/sandbox`
4. `pip install cocos2d`