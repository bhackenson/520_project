# Contributions

### Soniya Gaikwad

- Worked on the `ui-design` folder that consists of all the baseline HTML and CSS code for the UI/UX of the application that is later implemented in the `frontend-svelte` folder using [Figma](<https://www.figma.com/design/g7HDzd1IFFMkCYCwEtCxLy/Mus(ai)c-UI---COMPSCI520?node-id=2-62&t=3fBB0haAvIVYQVXA-1>)
  > - Account Info Page: `account-info-html.html` & `account-info.css`
  > - Create Account Page: `create-account-html.html` & `create-account.css`
  > - Landing Screen: `landing-screen-html.html` & `landing-screen.css`
  > - Login Page: `login-screen-html.html` & `login-screen.css`
  > - Project Editor Page: `project-editor-html.html` & `project-editor.css`
  > - Share Project Page: `share-project-html.html` & `share-project.css`
  > - Designs: `ui-original-designs.pdf`
- Worked on the [Presentation Slides](https://docs.google.com/presentation/d/1FeDPJGiS6mcSV5RTQD97QPQPcg_DqkfDDEI-0ZKV8SM/edit?usp=sharing) for the Project Proposal Meeting and Final Project Fair
- Worked on code documentation and comments for `python` files in the `server` folder
- Tested installation and deployment instructions in `README.md` with Terminal commands
- Implemented backend test code in `app-tests.py`

### Bret Hackenson

- Created the AI chord generation model in `generator.py` that predicts the next chord in a current sequence of chords, with each chord represented by a 12-length binary vector denoting which pitches are active (`1`) and not active (`0`). Libraries include Tensorflow (Sequential model) and music21 for computer-aided musical analysis. Dataset in `dataset.csv`, a subset of the dataset provided by [this repository](https://github.com/ology/Data-Dataset-ChordProgressions/tree/master).
- Created the server, including `app.py`, which uses a local json file as a database for development purposes, and `api.py`, which uses a MongoDB Atlas collection, bcrypt for password encryption, and JWTs to keep a user logged in during a session. Libraries include mongoengine for high-level interaction with MongoDB, as well as bcrypt and pyJWT
- Created `model.py` for MongoDB model definition
- Created rendering of sheet music on the client using the VexFlow npm library
- Implemented the playback and export features, with the playback feature using the Tone.JS npm library for high-level interaction with the browser's audio context
- Aided in providing functionality to Svelte implementation of frontend

### Sreya Nimmagadda

- Worked on frontend to create evaluation feature using HTML and CSS
- Worked on developing backend tests for testing the endpoints and functionality
- Worked on developing frontend tests for testing svelte implementation and functionality
- Worked on debugging frontend functionality for evaluation form
- Tested installation and deployment instructions in `README.md`
- Worked on the initial project proposal slides and created the use case diagrams
- Worked on the final project fair presentation slides. [Presentation Slides](https://docs.google.com/presentation/d/1FeDPJGiS6mcSV5RTQD97QPQPcg_DqkfDDEI-0ZKV8SM/edit?usp=sharing)

### Craig Bilelis

- Worked on frontend, including bugfix for current backend, and developed for initial concept frontend in Next.JS, further down the line scrapped for Svelte instead
- Helped with documentation in `README`
- Worked on the [Presentation Slides](https://docs.google.com/presentation/d/1FeDPJGiS6mcSV5RTQD97QPQPcg_DqkfDDEI-0ZKV8SM/edit?usp=sharing) for the Project Proposal Meeting and Final Project Fair
- Added `.mailmap` for account consolidation
- Kept repository clean through branch/commit management
- Tested Docker implementation
