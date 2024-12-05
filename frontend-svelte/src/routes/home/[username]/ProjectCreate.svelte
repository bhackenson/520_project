<script>
    export let visible = false;
    export let closeProjectCreate = () => {};
    export let createProject = (name) => {};

    let project_name = "";

    const submit = () => {
        createProject(project_name);
        project_name = "";
    }
</script>

{#if visible}
  <div class="popup-overlay" on:click={closeProjectCreate}>
    <div class="container" on:click|stopPropagation>
      <h2 id="title">Create Project</h2>
      <div id="enter-project">
        <input type="text" class="input" bind:value={project_name} name="project_name" placeholder="Enter project name">
      </div>
        <div id="create-proj">
            <input type='submit' class="submit" value="Submit" on:click={submit} name="Create Project">
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
        padding: 1rem 1rem;
}
#enter-project {
    width: 663px;
    height: 60px;
    left: 389px;
    top: 399px;
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

#create-proj {
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