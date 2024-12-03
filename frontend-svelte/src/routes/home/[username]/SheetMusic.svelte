<script>
    import { onMount } from "svelte";
    import { Vex } from "vexflow";

    export let data = {};

    const { Factory, EasyScore, System } = Vex.Flow;
    let container;

    onMount(() => {
        let keySig = data['key_signature'];
        keySig = String(keySig).toUpperCase() !== String(keySig) ? String(keySig).toUpperCase() + 'm' : String(keySig)
        keySig = keySig.replace("-", "b")
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
        let voice = '';
        let bass = '';

        let mel = data.melody.reduce((acc, e) => acc.concat(e), []);
        const insertSlash = (str) => { return str.slice(0, (str.length - 1)) + "/" + str.slice((str.length-1)); }
        mel = mel.map(s => insertSlash(s));


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

        const commaIndex_v = voice.indexOf(',');
        const beforeComma_v = voice.slice(0, commaIndex_v);
        const afterComma_v = voice.slice(commaIndex_v)
        voice = beforeComma_v + "/q" + afterComma_v;

        const commaIndex_b = bass.indexOf(',');
        const beforeComma_b = bass.slice(0, commaIndex_b);
        const afterComma_b = bass.slice(commaIndex_b)
        bass = beforeComma_b + "/q" + afterComma_b;

        console.log("voice: " + voice);
        console.log("bass: " + bass);
        console.log("mel: " + mel);

        const vf = new Factory({
            renderer: { elementId: container, width: 450, height: 300 },
        });

        mel = mel.map(n => { return vf.StaveNote({keys: [n], duration: "16"}); });

        const score = vf.EasyScore();
        const system = vf.System();
        system
            .addStave({
            voices: [
                score.voice(score.notes(voice, { stem: 'up' })),
                vf.Voice().addTickables(mel)
            ],
            })
            .addClef('treble')
            .addTimeSignature('4/4')
            .addKeySignature(keySig);

        system.addStave({
            voices: [
            score.voice(score.notes(bass, { clef: 'bass', stem: 'down' }))
            ]
        })
        .addClef('bass')
        .addTimeSignature('4/4')
        .addKeySignature(keySig)
        
        vf.draw();
    });
</script>
<div bind:this={container}></div>