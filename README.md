# MUS(AI)C

## Introduction

Mus(ai)c is an AI-powered music application where users can create projects and input chord progressions, and the AI will generate a melody over it, allowing users to explore their musical ideas and compositions!

## Install

Due to Mus(ai)c's nature as a web-app, since we are not currently hosting you can run a locally hosted version by cloning this repo, navigating to "frontend-svelte", and then execute `npm i`. Once everything is installed, execute `npm run dev`.

After doing that, then open a new terminal and cd into the server folder. Make a new file called `db.json` with empty curly braces, and then run `python app.py`.

<!-- ## Configuration (?) -->

<!-- ## Data Sets (?) -->

## AI Models

The `json` file will store a user's requested chord progression as a string separated by `|`. The front end requests a melody by providing this string. The backend converts the string into a list of 12-length binary vectors that denote which pitches are played in each chord. This array acts as a "seed" for a Sequential model that predicts what the next note of a melody will be (since chords and melodies are highly correlated). There is another field in the json file that stores this melody sent by the backend.

There are libraries that can handle the conversion of chords as strings to pitches, particularly `music21`, which aids in music computation projects like this one.

The user can also listen to the melody directly in the browser with the `Tone.js` library, which abstracts the browser's audio context to work nicely with rhythmic sound, like music melodies. They will also have the option to download the melody as a `MIDI` file that can be opened in programs like MuseScore. `music21` supports this conversion.
