# Mus(ai)c

## Introduction

_Mus(ai)c_ is an AI-powered music application where users can create projects and input chord progressions, and the AI will generate a melody over it, allowing users to explore their musical ideas and compositions!

## Install and Deploy

Due to Mus(ai)c's nature as a web-app, since we are not currently hosting you can run a locally hosted version by cloning this repository, navigate to the `frontend-svelte` folder, and then execute `npm i`. Once everything is installed, execute `npm run dev`.

> ### Terminal Commands
> 1. `cd frontend-svelte`
> 2. `npm i`
> 3. `npm run dev`

After doing that, open a new terminal and `cd` into the `server` folder. Make a new file called `db.json` with empty curly braces. Create and activate a [virtual environment](https://python.land/virtual-environments/virtualenv) for Python or [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), and then execute `pip install -r requirements.txt`. After that, run `python app.py`. Open the `localhost` link in your browser.

> ### Terminal Commands
> 1. `cd server`
> 2. `conda create --name musaic python=3.11.2`
> 3. `conda activate musaic`
> 4. `pip install -r requirements.txt`
> 5. `python app.py`

<!-- ## Configuration (?) -->

<!-- ## Data Sets (?) -->

## AI Models

The `json` file will store a user's requested chord progression as a string separated by `|`. The frontend requests a melody by providing this string. The backend converts the string into a list of 12-length binary vectors that denote which pitches are played in each chord. This array acts as a "seed" for a Sequential model that predicts what the next note of a melody will be (since chords and melodies are highly correlated). There is another field in the `json` file that stores this melody sent by the backend.

There are libraries that can handle the conversion of chords as strings to pitches, particularly `music21`, which aids in music computation projects like this one.

The user can also listen to the melody directly in the browser with the `Tone.js` library, which abstracts the browser's audio context to work nicely with rhythmic sound, like music melodies. They will also have the option to download the melody as a `MIDI` file that can be opened in programs like MuseScore. `music21` supports this conversion.

## Features
- Account Manager
> - user login & signup
> - change account info
- Project Editor
> - create, edit, and delete projects
> - create, edit, and delete progressions
- AI Generation
> - generate melodies using the AI model
- Song Playback
> - playback the generated music
- Collaboration
> - export MIDI file to share
- Feedback Evaluation
> - form to receive feedback about the generated music