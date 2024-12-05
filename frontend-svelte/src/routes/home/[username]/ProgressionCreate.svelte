<script>
    import * as Tone from 'tone';
    export let visible = false;
    export let close = () => {};
    export let createProg = function(o) {return;};

    let name = "";
    let key_signature = "C";
    let mode = "major";
    let time_signature = "";
    let tempo = "";

    let key_name = key_signature.replace("-", '\u266D').replace("#", '\u266F');

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

    const playChord = async (chord, len) => {
      await Tone.start();
      sampler.triggerAttackRelease(chord, len);
    }

    const submit = () => {
        createProg({name, key_signature, mode, time_signature, "tempo": parseInt(tempo)});
        name = "";
        key_signature = "";
        mode = "";
        time_signature = "";
        tempo = "";
    }

    const selectKey = (key) => {
      key_signature = key;
      if (key.toUpperCase() !== key) { mode = "minor" }
      else { mode = "major"; }
      key_name = key_signature.toUpperCase().replace("-", '\u266D').replace("#", '\u266F');

      switch (key) {
              case "G-":
                playChord(['Gb4', 'Bb4', 'Db4'], "4n");
                break;
              case "B":
                playChord(['B4', 'D#4', 'F#4'], "4n");
                break;
              case "E":
                playChord(['E4', 'G#4', 'B4'], "4n")
                break;
              case "A":
                playChord(['A4', 'C#4', 'E4'], "4n")
                break;
              case "D":
                playChord(['D4', 'F#4', 'A4'], "4n")
                break;
              case "G":
                playChord(['G4', 'B4', 'D4'], "4n")
                break;
              case "C":
                playChord(['C4', 'E4', 'G4'], "4n")
                break;
              case "F":
                playChord(['F4', 'A4', 'C4'], "4n")
                break;
              case "B-":
                playChord(['Bb4', 'D4', 'F4'], "4n")
                break;
              case "E-":
                playChord(['Eb4', 'G4', 'Bb4'], "4n")
                break;
              case "A-":
                playChord(['Ab4', 'C4', 'Eb4'], "4n")
                break;
              case "D-":
                playChord(['Db4', 'F4', 'Ab4'], "4n")
                break;

              case "e-":
                playChord(['Eb4', 'Gb4', 'Bb4'], "4n");
                break;
              case "g#":
                playChord(['G#4', 'B4', 'D#4'], "4n");
                break;
              case "c#":
                playChord(['C#4', 'E4', 'G#4'], "4n");
                break;
              case "f#":
                playChord(['F#4', 'A4', 'C#4'], "4n");
                break;
              case "b":
                playChord(['B4', 'D4', 'F#4'], "4n");
                break;
              case "e":
                playChord(['E4', 'G4', 'B4'], "4n");
                break;
              case "a":
                playChord(['A4', 'C4', 'E4'], "4n");
                break;
              case "d":
                playChord(['D4', 'F4', 'A4'], "4n");
                break;
              case "g":
                playChord(['G4', 'Bb4', 'D4'], "4n");
                break;
              case "c":
                playChord(['C4', 'Eb4', 'G4'], "4n");
                break;
              case "f":
                playChord(['F4', 'Ab4', 'C4'], "4n");
                break;
              case "b-":
                playChord(['Bb4', 'Db4', 'F4'], "4n");
                break;
            }
    }

</script>
{#if visible}
  <div class="popup-overlay" on:click={close}>
    <div class="container" on:click|stopPropagation>
      <h2 id="title">Create Progression</h2>
      <div id="enter-progression">
        <input type="text" class="input" bind:value={name} name="prog_name" placeholder="Enter progression name">
        <p id="key-sig-title">Key signature: {key_name+ " " + mode}</p><!-- <input type="text" class="input" bind:value={key_signature} name="key_signature" placeholder="Enter key signature">  -->
        <div class="wheels">
          <div class="circle-container">
            <div class="slice" id="G-" on:click={() => selectKey("G-")}><p class="key k1"><b>G&#9837;/F&#9839;</b></p></div>
            <div class="slice" id="B" on:click={() => selectKey("B")}><p class="key k2"><b>B</b></p></div>
            <div class="slice" id="E" on:click={() => selectKey("E")}><p class="key k3"><b>E</b></p></div>
            <div class="slice" id="A" on:click={() => selectKey("A")}><p class="key k4"><b>A</b></p></div>
            <div class="slice" id="D" on:click={() => selectKey("D")}><p class="key k5"><b>D</b></p></div>
            <div class="slice" id="G" on:click={() => selectKey("G")}><p class="key k6"><b>G</b></p></div>
            <div class="slice" id="C" on:click={() => selectKey("C")}><p class="key k7"><b>C</b></p></div>
            <div class="slice" id="F" on:click={() => selectKey("F")}><p class="key k8"><b>F</b></p></div>
            <div class="slice" id="B-" on:click={() => selectKey("B-")}><p class="key k9"><b>B&#9837;</b></p></div>
            <div class="slice" id="E-" on:click={() => selectKey("E-")}><p class="key k10"><b>E&#9837;</b></p></div>
            <div class="slice" id="A-" on:click={() => selectKey("A-")}><p class="key k11"><b>A&#9837;</b></p></div>
            <div class="slice" id="D-" on:click={() => selectKey("D-")}><p class="key k12"><b>D&#9837;</b></p></div>
            <div class="inner-circle"><p><b>Major</b></p></div>
          </div>
          <div class="circle-container">
            <div class="slice" id="e-" on:click={() => selectKey("e-")}><p class="key k1"><b>e&#9837;/d&#9839;</b></p></div>
            <div class="slice" id="g#" on:click={() => selectKey("g#")}><p class="key k2"><b>g&#9839;</b></p></div>
            <div class="slice" id="c#" on:click={() => selectKey("c#")}><p class="key k3"><b>c&#9839;</b></p></div>
            <div class="slice" id="f#" on:click={() => selectKey("f#")}><p class="key k4"><b>f&#9839;</b></p></div>
            <div class="slice" id="b" on:click={() => selectKey("b")}><p class="key k5"><b>b</b></p></div>
            <div class="slice" id="e" on:click={() => selectKey("e")}><p class="key k6"><b>e</b></p></div>
            <div class="slice" id="a" on:click={() => selectKey("a")}><p class="key k7"><b>a</b></p></div>
            <div class="slice" id="d" on:click={() => selectKey("d")}><p class="key k8"><b>d</b></p></div>
            <div class="slice" id="g" on:click={() => selectKey("g")}><p class="key k9"><b>g</b></p></div>
            <div class="slice" id="c" on:click={() => selectKey("c")}><p class="key k10"><b>c</b></p></div>
            <div class="slice" id="f" on:click={() => selectKey("f")}><p class="key k11"><b>f</b></p></div>
            <div class="slice" id="b-" on:click={() => selectKey("b-")}><p class="key k12"><b>b&#9837;</b></p></div>
            <div class="inner-circle"><p><b>Minor</b></p></div>
          </div>
        </div>
        <!-- <input type="text" class="input" bind:value={mode} name="mode" placeholder="Enter mode"> -->
        <input type="text" class="input" bind:value={time_signature} name="time_signature" placeholder="Enter time signature">
        <input type="text" class="input" bind:value={tempo} name="tempo" placeholder="Enter tempo">
      </div>
        <div id="create-prog">
            <input type='submit' class="submit" value="Generate" on:click={submit} name="Create Progression">
      </div>
    </div>
  </div>
{/if}

<style>

  #title {
      font-family: sans-serif;
      color: #0F3A57;
  }

  #key-sig-title {
    color: #0F3A57;
    font-size: x-large;
  }

  .wheels {
      display: flex;
      justify-content: center;
    }

    .container {
      width: 75%;
      display: block;
      background: white;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
    }
  
    .circle-container {
      margin-top: 10px;
      margin-bottom: 10px;
      margin-left: 10px;
      margin-right: 10px;
      position: relative;
      width: 400px;
      height: 400px;
      border-radius: 50%;
      overflow: hidden;
    }

    .inner-circle {
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: Arial, Helvetica, sans-serif;
      font-size: x-large;
      left: 25%;
      bottom: -25%;
      width: 200px;
      height: 200px;
      border-radius: 50%;
      background-color: white;
      color: #0F3A57;
    }

    .slice {
      position: absolute;
      display: flex;
      justify-content: center;
      align-items: center;
      bottom: 0;
      width: 50%;
      height: 50%;
      left: 25%;
      transform-origin: top center;
      clip-path: polygon(50% 0, 75% 100%, 25% 100%);
      background-color: #bce4ff;
      transition: background-color 0.2s;
    }

    .slice:hover {
      cursor: pointer;
      background-color: #92d3ff;
    }

    .slice:nth-child(1) { transform: rotate(0deg); }
    .slice:nth-child(2) { transform: rotate(-30deg); }
    .slice:nth-child(3) { transform: rotate(-60deg); }
    .slice:nth-child(4) { transform: rotate(-90deg); }
    .slice:nth-child(5) { transform: rotate(-120deg); }
    .slice:nth-child(6) { transform: rotate(-150deg); }
    .slice:nth-child(7) { transform: rotate(-180deg); }
    .slice:nth-child(8) { transform: rotate(-210deg); }
    .slice:nth-child(9) { transform: rotate(-240deg); }
    .slice:nth-child(10) { transform: rotate(-270deg); }
    .slice:nth-child(11) { transform: rotate(-300deg); }
    .slice:nth-child(12) { transform: rotate(-330deg); }

    .key {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 25%;
      height: 25%;
      bottom: 0;
      position: absolute;
      font-size: x-large;
      color: black;
      transform-origin: center;
    }

    .k1 { transform: rotate(0deg); }
    .k2 { transform: rotate(30deg); }
    .k3 { transform: rotate(60deg); }
    .k4 { transform: rotate(90deg); }
    .k5 { transform: rotate(120deg); }
    .k6 { transform: rotate(150deg); }
    .k7 { transform: rotate(180deg); }
    .k8 { transform: rotate(210deg); }
    .k9 { transform: rotate(240deg); }
    .k10 { transform: rotate(270deg); }
    .k11 { transform: rotate(300deg); }
    .k12 { transform: rotate(330deg); }
  
  .input {
      border-style: solid;
      border-radius: 8px;
      display: block;
      width: 95%;
      font-size: 1.125rem;
      padding: 1rem 0.25rem;
      margin-top: 1rem;
      margin-bottom: 1rem;
  }
  #enter-progression {
      /*
      width: 663px;
      height: 60px;
      left: 389px;
      top: 399px;
      */
      width: 100%;
      text-align: center;
      color: #EEF6FC;
      font-size: 50px;
      font-family: Inter, sans-serif;
      font-weight: 400;
      word-wrap: break-word;
  }
  
  .submit {
          border-style: none;
          display: block;
          width: 100%;
          font-size: 2rem;
          padding: 1rem 1rem;
          color: white;
          /* background-color: rgb(104, 75, 125); */
          border-radius: 8px;
          margin-bottom: 1rem;
          background: #3498DB;
          cursor: pointer;
  
  }
  
  #create-prog {
     /* width: ;
      height: 67px;
      left: 603px;
      top: 687px;
      */
      width: 100%;
      margin-top: 1rem;
      text-align: center;
      color: #CBE5F6;
      font-size: 50px;
      font-family: Inter, sans-serif;
      font-weight: 400;
      word-wrap: break-word;
  }
  
  .popup-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>