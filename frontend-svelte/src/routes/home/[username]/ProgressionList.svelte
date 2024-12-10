<script>
    import SheetMusic from "./SheetMusic.svelte";
    import * as Tone from 'tone';
    import Store from './Store.js';
	import { onMount } from "svelte";
    export let userid;
    export let project;

    let progs = []
    Store.subscribe((userdata) => {
        console.log(project)
        if (Object.keys(project).length == 0) { progs = []; }
        else { progs = userdata['projects'].find(p => p['id'] == project['id'])['progressions'] }
    })

    // const synth = new Tone.PolySynth(Tone.AMSynth).toDestination();
    let sampler = new Tone.Sampler({
        urls: {
            "C2": "C2.m4a",
            "C3": "C3.m4a",
            "C4": "C4.m4a",
            "E4": "E4.m4a",
            "G4": "G4.m4a",
            "C5": "C5.m4a"
        },
        baseUrl: "/audio/",
        release: 1
        }).toDestination();

    const playProg = async (data_chords, data_melody, time_sig, tempo) => {
        
        const chords = []
        for (let chord of data_chords) { chords.push(chord.notes) }
        const melody = data_melody;

        if (time_sig == "4/4") {
            Tone.getTransport().bpm.value = tempo;
            Tone.getTransport().timeSignature = [4, 4];
            //Tone.start();
            const part = new Tone.Part(((time, chord) => {
                /*
                Tone.getTransport().scheduleOnce(() => {
                for (let note of chord) {
                    // unhighlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
                }
                }, "+4n");
                */
                sampler.triggerAttackRelease(chord, "4n", time);
                /*
                for (let note of chord) { 
                    // highlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
                }
                */
            }),[[0,     chords[0].concat(melody[0][0])],
                ["0:0:2", melody[0][1]],
                ["0:1:0", melody[0][2]],
                ["0:1:2", melody[0][3]],
                ["0:2", chords[1].concat(melody[1][0])],
                ["0:2:2", melody[1][1]],
                ["0:3:0", melody[0][2]],
                ["0:3:2", melody[0][3]],
                ["1:0", chords[2].concat(melody[2][0])],
                ["1:0:2", melody[2][1]],
                ["1:1:0", melody[2][2]],
                ["1:1:2", melody[2][2]],
                ["1:2", chords[3].concat(melody[3][0])],
                ["1:2:2", melody[3][1]],
                ["1:3:0", melody[3][2]],
                ["1:3:2", melody[3][3]]])
            .start(0);

            Tone.getTransport().scheduleOnce(() => {
                part.stop();
                part.dispose();
                Tone.getTransport().stop();
            }, '2m');

            Tone.getTransport().start();
            return;
        }

        if (time_sig == "3/4" || time_sig == "6/8") {
            Tone.getTransport().bpm.value = tempo;
            Tone.getTransport().timeSignature = [3, 4];
            const part = new Tone.Part(((time, chord) => {
                /*
                Tone.getTransport().scheduleOnce(() => {
                for (let note of chord) {
                    // unhighlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
                }
                }, "+4n");
                */
                sampler.triggerAttackRelease(chord, "4n", time);
                /*
                for (let note of chord) { 
                    // highlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
                }
                */
            }),[[0,     chords[0].concat(melody[0][0])],
                ["0:1:0", melody[0][1]],
                ["0:2:0", melody[0][2]],
                ["1:0:0", chords[1].concat(melody[1][0])],
                ["1:1:0", melody[1][1]],
                ["1:2:0", melody[0][2]],
                ["2:0:0", chords[2].concat(melody[2][0])],
                ["2:1:0", melody[2][1]],
                ["2:2:0", melody[2][2]],
                ["3:0:0", chords[3].concat(melody[3][0])],
                ["3:1:0", melody[3][1]],
                ["3:2:0", melody[3][2]]])
            .start(0);

            Tone.getTransport().scheduleOnce(() => {
                part.stop();
                part.dispose();
                Tone.getTransport().stop();
            }, '4m');

            Tone.getTransport().start();
            return;
        }

        /*
        Tone.start();

        const chords = []

        for (let chord of data) {
            chords.push(chord.notes)
        }

        let note_to_id = {
            'C': 'C', 'B#': 'C',
            'C#': 'C#', 'Db': "C#",
            'D': 'D',
            'D#': 'D#', 'Eb': 'D#',
            'E': 'E', 'Fb': 'E',
            'F': 'F', 'E#': 'E#',
            'F#': 'F#', 'Gb': 'F#',
            'G': 'G',
            'G#': 'G#', 'Ab': 'G#',
            'A': 'A',
            'A#': 'A#', 'Bb': 'A#',
            'B': 'B', 'Cb': 'B'
        }

        const part = new Tone.Part(((time, chord) => {
            Tone.getTransport().scheduleOnce(() => {
            for (let note of chord) {
                // unhighlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
            }
            }, "+4n");
            sampler.triggerAttackRelease(chord, "4n", time);
            for (let note of chord) { 
            // highlightKey(note_to_id[note.slice(0, -1)] + note.charAt(note.length - 1));
            }
        }), [[0, chords[0]], ["0:2", chords[1]], ["1:0", chords[2]], ["1:2", chords[3]]]).start(0);

        Tone.getTransport().scheduleOnce(() => {
            part.dispose();
            Tone.getTransport().stop();
        }, '2m');

        Tone.getTransport().start();
        */

    }

    const delete_prog = async (progid) => {
        const response = await fetch('http://localhost:5000/api/delete_progression', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, "projid": project['id'], progid})
        });
        if (!response.ok) {
            if (response.status == 400) {
                alert("Error deleting progression.")
            }
            else {
                console.log("Error deleting progression.");
            }
            return;
        }
  
        const res2 = await fetch('http://localhost:5000/api/get_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid})
        });
        if (!res2.ok) {
            if (response.status == 400) {
                console.log("Could not find user.")
                //sessionStorage.removeItem('jwt');
                //goto("/");
            }
            else {
                console.log("Failed to fetch projects.");
            }
            return;
        }
        const data2 = await res2.json();
        Store.update((userata) => {
            return data2.user;
        })
    }

    const createMidiFile = async (prog_obj) => {
        const response = await fetch('http://localhost:5000/api/send_midi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, "progression": prog_obj})
        });
        if (!response.ok) {
            if (response.status == 400) {
                alert("Error creating MIDI file.")
            }
            else {
                console.log({"status": response.status, "message": "Error creating MIDI file."});
            }
            return;
        }

        const blob = await response.blob();
        const URL = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = URL;
        a.download = "export.mid";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(URL);
    };


</script>
{#each progs as prog (prog.id)}
    <div class='title'>
        <div class="progression-text">{prog['name']}</div>
        <div class="progression">
            <SheetMusic data={prog} />
            <div class="actions">
                <button class="play-btn" on:click={() => playProg(prog['chords'], prog['melody'], prog['time_signature'], prog['tempo'])}>play</button>
                <button class="export-btn" on:click={() => createMidiFile(prog)}>export</button>
                <button class="delete-btn" on:click={() => delete_prog(prog['id'])}>delete</button>
                <!-- <button class="play-btn" on:click={() => delete_prog(prog['id'])}>delete</button> -->
            </div>
        </div>
    </div>
{/each}

<style>

.progression {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #CBE5F6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.progression-text{
    color: #185D8B;
    font-size: 25px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word
}

.progression .lines {
    flex: 1;
    height: 100px;
    margin: 0 10px;
    border: 1px solid #63B0E3;
    border-radius: 5px;
}

.progression .actions {
    display: flex;
    flex-direction: column;
}

.progression .actions button {
    margin: 5px 0;
    padding: 5px 10px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.progression .actions .play-btn {
    background-color: #EEF6FC;
    color: #63B0E3;
}

.progression .actions .export-btn {
    background-color: #97CAED;
    color: #185D8B;
}

.progression .actions .delete-btn {
    background-color: #63B0E3;
    color: #EEF6FC;
}
</style>