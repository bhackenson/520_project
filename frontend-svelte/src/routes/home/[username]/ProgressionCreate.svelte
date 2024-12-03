<script>
    export let visible = false;
    export let close = () => {};
    export let createProg = function(o) {return;};

    let name = "";
    let key_signature = "";
    let mode = "";
    let time_signature = "";
    let tempo = "";

    const submit = () => {
        createProg({name, key_signature, mode, time_signature, "tempo": parseInt(tempo)});
        name = "";
        key_signature = "";
        mode = "";
        time_signature = "";
        tempo = "";
    }

</script>
{#if visible}
  <div class="popup-overlay" on:click={close}>
    <div class="container" on:click|stopPropagation>
      <h2 id="title">Create Progression</h2>
      <div id="enter-progression">
        <input type="text" class="input" bind:value={name} name="prog_name" placeholder="Enter progression name">
        <input type="text" class="input" bind:value={key_signature} name="key_signature" placeholder="Enter key signature">
        <input type="text" class="input" bind:value={mode} name="mode" placeholder="Enter mode">
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
    .container {
      width: 25%;
      display: block;
      background: white;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
    }
  
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