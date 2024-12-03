<script>
    import SheetMusic from "./SheetMusic.svelte";
    import Store from './Store.js';
    export let userid;
    export let project;

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
                alert("Could not find user.")
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


</script>
{#each project['progressions'] as prog (prog.id)}
<div class="progression">
    <div class="progression-text">{prog['name']}</div>
    <SheetMusic data={prog} />
    <div class="actions">
        <button class="play-btn">play</button>
        <button class="edit-btn">edit</button>
        <button class="export-btn">export</button>
        <button class="play-btn" on:click={() => delete_prog(prog['id'])}>delete</button>
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

.progression .progression-text{
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

.progression .actions .edit-btn {
    background-color: #97CAED;
    color: #185D8B;
}

.progression .actions .export-btn {
    background-color: #63B0E3;
    color: #EEF6FC;
}
</style>