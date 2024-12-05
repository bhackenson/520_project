<script>
    import { onMount } from "svelte";
    import { NoteSubGroup, Vex } from "vexflow";

    export let data = {};

    const { Factory, EasyScore, System } = Vex.Flow;
    let container;

    onMount(() => {
        const insertSlash = (str) => { return str.slice(0, (str.length - 1)) + "/" + str.slice((str.length-1)); }

        let keySig = data['key_signature'];
        keySig = String(keySig).toUpperCase() !== String(keySig) ? String(keySig).toUpperCase() + 'm' : String(keySig)
        keySig = keySig.replace("-", "b")
        const time_sig = data.time_signature;
        const chords = data.chords;
        /*
        let names = '';
        for (let c of chords) {
            names += c.chord + " | "
        }
        names = names.slice(0, -3);
        let name_elem = document.getElementById('chordnames');
        name_elem.innerHTML = names;
        */

        const vf = new Factory({ renderer: { elementId: container, width: 790, height: 300 } });

       // mel = mel.map(n => { return vf.StaveNote({keys: [n], duration: "16"}); });
        /*

        let mel1;
        if (time_sig == "4/4") { mel1 = data.melody.map(notes => notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "16"}))); }
        else if (time_sig == "3/4") { mel1 = data.melody.map(notes => notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "16"}))); }
        else if (time_sig == "6/8") { mel1 = data.melody.map(notes => new Vex.Flow.Tuplet(notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "q"})))); }
        else { mel1 = data.melody.map(notes => notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "q"}))); }
        */
        // let mel1 = data.melody.map(notes => notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "16"})));

        if (time_sig == "4/4") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 410);
            const staveTreble2 = new Vex.Flow.Stave(420, 30, 350);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 410);
            const staveBass2 = new Vex.Flow.Stave(420, 150, 350);

            staveTreble1.addClef('treble').addTimeSignature('4/4').addKeySignature(keySig);
            staveBass1.addClef('treble').addTimeSignature('4/4').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'h'}));
            // let mel1 = data.melody.map(notes => new Vex.Flow.Tuplet(notes.map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}))));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});

            bassVoice1.addTickables(_chords.slice(0,2));
            bassVoice2.addTickables(_chords.slice(2,4));

            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 4, beat_value: 4});

            trebleVoice1.addTickables(mel1.slice(0,8));
            trebleVoice2.addTickables(mel1.slice(8,16));

            const beams = [
                new Vex.Flow.Beam(mel1.slice(0,4)),
                new Vex.Flow.Beam(mel1.slice(4,8)),
                new Vex.Flow.Beam(mel1.slice(8,12)),
                new Vex.Flow.Beam(mel1.slice(12,16))
            ]

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);

            beams.forEach(beam => beam.setContext(vf.getContext()).draw());
            /*
            let voice = '';
            let bass = '';

            for (let k = 0; k < chords.length; k++) {
                let s = '';
                for (let i = 0; i < chords[k].notes.length; i++) {
                    if (i == 0) {
                        if (k == chords.length - 1) {bass += chords[k].notes[i]; }
                        else { bass += chords[k].notes[i] + ', '; }
                    }
                    else {
                        if (i == chords[k].notes.length - 1) { s += chords[k].notes[i]; }
                        else { s += chords[k].notes[i] + ' '; }
                    }
                }
                if (k == chords.length - 1) { voice += `(${s})`; }
                else { voice += `(${s}), `; }
            }

            console.log(voice)
            console.log(bass)
            let voice_arr = voice.split(", ");
            let bass_arr = bass.split(", ");

            let voice1 = voice_arr[0] + "/q, " + voice_arr[1];
            let voice2 = voice_arr[2] + "/q, " + voice_arr[2];
            let bass1 = bass_arr[0] + "/q, " + bass_arr[1];
            let bass2 = bass_arr[2] + "/q, " + bass_arr[2];

            const commaIndex_v = voice.indexOf(',');
            const beforeComma_v = voice.slice(0, commaIndex_v);
            const afterComma_v = voice.slice(commaIndex_v)
            voice = beforeComma_v + '/q' + afterComma_v;

            const commaIndex_b = bass.indexOf(',');
            const beforeComma_b = bass.slice(0, commaIndex_b);
            const afterComma_b = bass.slice(commaIndex_b)
            bass = beforeComma_b + '/q' + afterComma_b;


            let mel1 = data.melody.map(notes => notes.map(n => vf.StaveNote({keys: [insertSlash(n)], duration: "16"})));

            const stave = new Vex.Flow.Stave(10, 40, 400);
            stave.addClef("treble").setContext(vf.getContext()).draw();
            const score = vf.EasyScore();
            const system = vf.System();
            let beams = mel1.map(notes => new Vex.Flow.Beam(notes))

            const voiceTreble1 = score.voice(vf.Voice().addTickables(mel1.slice(0,2).reduce((acc, e) => acc.concat(e), [])));
            const voiceTreble2 = score.voice(score.notes(mel1.slice(2,4).reduce((acc, e) => acc.concat(e), [])));
            
            
            system
            .addStave({
                voices: [
                    vf.Voice().addTickables(mel1.reduce((acc, e) => acc.concat(e), []))
                ],
            })
            .addClef('treble')
            .addTimeSignature(time_sig)
            .addKeySignature(keySig);


            system.addStave({
                voices: [
                    score.voice(score.notes(voice, { stem: 'up' })),
                    score.voice(score.notes(bass, { clef: 'treble', stem: 'up' }))
                ]
            })
            .addClef('treble')
            .addTimeSignature(time_sig)
            .addKeySignature(keySig)
            
            const formatter = new Vex.Flow.Formatter();
            formatter.joinVoices([voiceTreble1, voiceTreble2]).format([voiceTreble1, voiceTreble2], 350);
            voice1.draw(vf.getContext(), stave);
            voice2.draw(vf.getContext(), stave);
            
            vf.draw();
            beams.forEach(beam => beam.setContext(vf.getContext()).draw());
            */

        }
        else if (time_sig == "3/4") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 280);
            const staveTreble2 = new Vex.Flow.Stave(290, 30, 160);
            const staveTreble3 = new Vex.Flow.Stave(450, 30, 160);
            const staveTreble4 = new Vex.Flow.Stave(610, 30, 160);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 280);
            const staveBass2 = new Vex.Flow.Stave(290, 150, 160);
            const staveBass3 = new Vex.Flow.Stave(450, 150, 160);
            const staveBass4 = new Vex.Flow.Stave(610, 150, 160);

            staveTreble1.addClef('treble').addTimeSignature('3/4').addKeySignature(keySig);
            staveBass1.addClef('treble').addTimeSignature('3/4').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveTreble3.setContext(vf.getContext()).draw();
            staveTreble4.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();
            staveBass3.setContext(vf.getContext()).draw();
            staveBass4.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'h', dots: 1}));
            // let mel1 = data.melody.map(notes => new Vex.Flow.Tuplet(notes.map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}))));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "q"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice3 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice4 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            bassVoice1.addTickables(_chords.slice(0,1));
            bassVoice2.addTickables(_chords.slice(1,2));
            bassVoice3.addTickables(_chords.slice(2,3));
            bassVoice4.addTickables(_chords.slice(3,4));
            
            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice3 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice4 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            trebleVoice1.addTickables(mel1.slice(0,3));
            trebleVoice2.addTickables(mel1.slice(3,6));
            trebleVoice3.addTickables(mel1.slice(6,9));
            trebleVoice4.addTickables(mel1.slice(9,12));

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([trebleVoice3], staveTreble3)
            .formatToStave([trebleVoice4], staveTreble4)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)
            .formatToStave([bassVoice3], staveBass3)
            .formatToStave([bassVoice4], staveBass4)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            trebleVoice3.draw(vf.getContext(), staveTreble3);
            trebleVoice4.draw(vf.getContext(), staveTreble4);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);
            bassVoice3.draw(vf.getContext(), staveBass3);
            bassVoice4.draw(vf.getContext(), staveBass4);

            /*
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 410);
            const staveTreble2 = new Vex.Flow.Stave(420, 30, 350);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 410);
            const staveBass2 = new Vex.Flow.Stave(420, 150, 350);

            staveTreble1.addClef('treble').addTimeSignature('3/4').addKeySignature(keySig);
            staveBass1.addClef('treble').addTimeSignature('3/4').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'q', dots: 1}));
            // let mel1 = data.melody.map(notes => new Vex.Flow.Tuplet(notes.map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}))));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            bassVoice1.addTickables(_chords.slice(0,2));
            bassVoice2.addTickables(_chords.slice(2,4));

            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 3, beat_value: 4});

            trebleVoice1.addTickables(mel1.slice(0,6));
            trebleVoice2.addTickables(mel1.slice(6,12));

            const beams = [
                new Vex.Flow.Beam(mel1.slice(0,3)),
                new Vex.Flow.Beam(mel1.slice(3,6)),
                new Vex.Flow.Beam(mel1.slice(6,9)),
                new Vex.Flow.Beam(mel1.slice(9,12))
            ]

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);

            beams.forEach(beam => beam.setContext(vf.getContext()).draw());
            */
        }
        else if (time_sig == "6/8") {
            const staveTreble1 = new Vex.Flow.Stave(10, 30, 410);
            const staveTreble2 = new Vex.Flow.Stave(420, 30, 350);
            const staveBass1 = new Vex.Flow.Stave(10, 150, 410);
            const staveBass2 = new Vex.Flow.Stave(420, 150, 350);

            staveTreble1.addClef('treble').addTimeSignature('6/8').addKeySignature(keySig);
            staveBass1.addClef('treble').addTimeSignature('6/8').addKeySignature(keySig);

            staveTreble1.setContext(vf.getContext()).draw();
            staveTreble2.setContext(vf.getContext()).draw();
            staveBass1.setContext(vf.getContext()).draw();
            staveBass2.setContext(vf.getContext()).draw();

            let _chords = []; for (let c of chords) { _chords.push(c.notes); }
            _chords = _chords.map(notes => new Vex.Flow.StaveNote({keys: notes.map(n => insertSlash(n)), duration: 'q', dots: 1}));
            // let mel1 = data.melody.map(notes => new Vex.Flow.Tuplet(notes.map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}))));
            let mel1 = data.melody.reduce((acc,e) => acc.concat(e), []).map(n => new Vex.Flow.StaveNote({keys: [insertSlash(n)], duration: "8"}));

            const bassVoice1 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});
            const bassVoice2 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});

            bassVoice1.addTickables(_chords.slice(0,2));
            bassVoice2.addTickables(_chords.slice(2,4));

            const trebleVoice1 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});
            const trebleVoice2 = new Vex.Flow.Voice({num_beats: 6, beat_value: 8});

            trebleVoice1.addTickables(mel1.slice(0,6));
            trebleVoice2.addTickables(mel1.slice(6,12));

            const beams = [
                new Vex.Flow.Beam(mel1.slice(0,3)),
                new Vex.Flow.Beam(mel1.slice(3,6)),
                new Vex.Flow.Beam(mel1.slice(6,9)),
                new Vex.Flow.Beam(mel1.slice(9,12))
            ]

            new Vex.Flow.Formatter()
            .formatToStave([trebleVoice1], staveTreble1)
            .formatToStave([trebleVoice2], staveTreble2)
            .formatToStave([bassVoice1], staveBass1)
            .formatToStave([bassVoice2], staveBass2)

            trebleVoice1.draw(vf.getContext(), staveTreble1);
            trebleVoice2.draw(vf.getContext(), staveTreble2);
            bassVoice1.draw(vf.getContext(), staveBass1);
            bassVoice2.draw(vf.getContext(), staveBass2);

            beams.forEach(beam => beam.setContext(vf.getContext()).draw());
        }
    });
</script>
<div bind:this={container}></div>