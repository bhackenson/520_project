<script>
    import Store from "./Store.js";
    import StoreEval from "./StoreEval.js";
    import SheetMusic from "./SheetMusic.svelte";

    export let visible = false;
    export let close = () => {};
    export let userid;
    export let currProj = {};

    let prog1 = {};
    let prog2 = {};

    let currSelected = prog1;
    let currNum = 1;
    let q1 = -1;
    let q2 = -1;
    let q3 = -1;
    let comment = "";

    const selectProgression = (num) => {
        if (num == 1) { currSelected = prog1; currNum = 1; }
        if (num == 2) { currSelected = prog2; currNum = 2; }
    }

    StoreEval.subscribe((progs) => {
        prog1 = progs.prog1;
        prog2 = progs.prog2;
    });

    const submit = async () => {
        const res1 = await fetch('http://localhost:5000/api/send_progression', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid,
                                "projid": currProj['id'],
                                "name": currSelected['name'],
                                "key_signature": currSelected['key_signature'],
                                "mode": currSelected['mode'],
                                "time_signature": currSelected['time_signature'],
                                "tempo": currSelected['tempo'],
                                "chords": currSelected['chords'],
                                "melody": currSelected['melody']
                            })
        });

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

        const res3 = await fetch('http://localhost:5000/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({"progression1": prog1,
                                "progression2": prog2,
                                "naturalness": q1,
                                "accuracy": q2,
                                "inspiration": q3,
                                "comment": comment
                            })
        });

        close()

    }

    //export let createProg = function(o) {return;};

    /*
    const submit = () => {
        createProg({name, key_signature, mode, time_signature, tempo});
        name = "";
        key_signature = "C";
        mode = "major";
        time_signature = "4/4";
        tempo = 100;
    }
    */

</script>
{#if visible}
{console.log(prog1)}
  <div class="popup-overlay">
    <div class='container'>
        <div class="sheets-container" on:click|stopPropagation>
            <h1 id="select-title">Select a Progression: <b>{currNum}</b></h1>
            <div class='title' on:click={() => selectProgression(1)}>
                <div class="progression-text">{prog1.name}</div>
                <div class="progression">
                    <SheetMusic data={prog1} />
                </div>
            </div>
            <div class='title' on:click={() => selectProgression(2)}>
                <div class="progression-text">{prog1.name}</div>
                <div class="progression">
                    <SheetMusic data={prog1} />
                </div>
            </div>
        </div>

        <div class="evaluate-box">
            <div class="evaluate-text">Evaluation Form</div>
            <div class="evaluate">
                <div class="question">How enjoyable is the progression musically?</div>
                <div class="radio-group">
                    <input type="radio" id="five" name="Question1" value="5" bind:group={q1} checked>
                    <label for="yes">5 (excellent)</label><br>
        
                    <input type="radio" id="four" name="Question1" value="4" bind:group={q1}>
                    <label for="no">4 (good)</label><br>
        
                    <input type="radio" id="three" name="Question1" value="3" bind:group={q1}>
                    <label for="no">3 (average)</label><br>
        
                    <input type="radio" id="two" name="Question1" value="2" bind:group={q1}>
                    <label for="no">2 (bad)</label><br>
        
                    <input type="radio" id="one" name="Question1" value="1" bind:group={q1}>
                    <label for="no">1 (poor)</label><br>
                </div>
        
                <div class="question">How consistently does the progression align with the input provided?</div>
                <div class="radio-group">
                    <input type="radio" id="five" name="Question2" value="5" bind:group={q2} checked>
                    <label for="yes">5 (excellent)</label><br>
        
                    <input type="radio" id="four" name="Question2" value="4" bind:group={q2}>
                    <label for="no">4 (good)</label><br>
        
                    <input type="radio" id="three" name="Question2" value="3" bind:group={q2}>
                    <label for="no">3 (average)</label><br>
        
                    <input type="radio" id="two" name="Question2" value="2" bind:group={q2}>
                    <label for="no">2 (bad)</label><br>
        
                    <input type="radio" id="one" name="Question2" value="1" bind:group={q2}>
                    <label for="no">1 (poor)</label><br>
                </div>
        
                <div class="question">How original and creative does the progression feel?</div>
                <div class="radio-group">
                    <input type="radio" id="five" name="Question3" value="5" bind:group={q3} checked>
                    <label for="html">5 (excellent)</label><br>
        
                    <input type="radio" id="four"  name="Question3" value="4" bind:group={q3}>
                    <label for="html">4 (good)</label><br>
        
                    <input type="radio" id="three" name="Question3" value="3" bind:group={q3}>
                    <label for="no">3 (average)</label><br>
        
                    <input type="radio" id="two" name="Question3" value="2" bind:group={q3}>
                    <label for="no">2 (bad)</label><br>
        
                    <input type="radio" id="one" name="Question3" value="1" bind:group={q3}>
                    <label for="no">1 (poor)</label><br>
                </div>
                <div class="additional">
                    Additional Comments
                    <!-- <input type="text" class="text-box" bind:value={comment} name="comment" placeholder="Enter comment"> -->
                     <textarea class='text-box' bind:value={comment} name="comment" placeholder="Enter comment"></textarea>
                </div>
                <div class="access-actions">
                    <button class="submit-btn" on:click={submit}>submit</button>
                </div>
            </div>
        </div>
    </div>
  </div>
{/if}

<style>
    #select-title {
        font-size: large;
        font-family: 'Times New Roman', Times, serif;
        color: #185D8B;
    }
    .container {
        display: flex;
        width: 95%;
        height: 95%;
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
  .sheets-container {
    width: 75%;
    height: 95%;
    display: block;
    background: white;
    padding: 0.5rem;
    text-align: center;
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

.progression {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #CBE5F6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    cursor: pointer;
}

.progression:hover {
    background-color: #b9d5e7;
}

.progression-text{
    color: #185D8B;
    font-size: 25px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word
}

.progression {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #CBE5F6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.evaluate-box {
    font-size: large;
    display: flex;
    flex-direction: column;
    background-color: #97CAED;
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 10px;
    width: 50%;
    height: 90%;
}

.evaluate-text{
    color: #185D8B;
    font-size: 30px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word;
    align-self: center;
    margin-bottom: 10px;
}

.close-btn {
    background-color: #63B0E3;
    color: #0F3A57;
    font-size: 20px;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    text-align: center;
    cursor: pointer;
}

.evaluate {
    color: #185D8B;
    font-size: 25px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word
}

.question {
    color: #0F3A57;
    font-size: 20px;
    font-family: Inter;
    justify-self: center;
    font-weight: 400;
    word-wrap: break-word;
    margin-bottom: 10px;
}

.radio-group{
    color: #0F3A57;
    font-size: 15px;
    font-family: Inter;
    justify-self: left;
    font-weight: 400;
    word-wrap: break-word;
    margin-bottom: 10px;
}

.additional {
    display: grid;
    color: #0F3A57;
    font-size: 20px;
    font-family: Inter;
    justify-self: center;
    font-weight: 400;
    word-wrap: break-word;
    margin-bottom: 10px;
}

.text-box {
    flex: 1;
    height: 5rem;
    width: 100%;
    margin: 0 10px;
    background-color: #63B0E3;
    border: 1px solid #63B0E3;
    border-radius: 5px;
    font-family: 'Times New Roman', Times, serif;
    resize: none;
}

.access-actions {
    display: flex;
    flex-direction: column;
}

button {
    margin: 5px 0;
    padding: 5px 10px;
    font-size: 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.submit-btn {
    background-color: #EEF6FC;
    height: 5rem;
    font-size: larger;
    font-family: 'Times New Roman', Times, serif;
    font-weight: 400;
    color: #63B0E3;
    margin-top: 2rem;
}

  </style>