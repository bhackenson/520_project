<script>
    import { onMount } from 'svelte';
    import Store from './Store.js';
    import { goto } from '$app/navigation'
	import StoreEval from './StoreEval.js';
  
    export let userid;
    export let updateProj = (i) => {};

    const update = (i) => {
        updateProj(i);
        Store.update((userdata) => {return userdata;});
    }
    let user = {};

    onMount(async () => {
        const response = await fetch('http://localhost:5000/api/get_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid})
        });
        if (!response.ok) {
            if (response.status == 400) {
                console.log("Could not find user to load projects.")
                //sessionStorage.removeItem('jwt');
                //goto("/");
            }
            else {
                console.log("Failed to fetch projects.");
            }
            return;
        }
      const data = await response.json();
      Store.set(data.user);
      StoreEval.set({});
    });
  
    Store.subscribe((userdata) => {
      user = userdata;
      console.log(`projects: ${JSON.stringify(userdata)}`);
    });

    const delete_proj = async (projid) => {
        const response = await fetch('http://localhost:5000/api/delete_project', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, projid})
        });
        if (!response.ok) {
            if (response.status == 400) {
                alert("Could not find user or project.")
            }
            else {
                console.log("Failed to fetch projects.");
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

        update({});
    }
  
  </script>

<ul class="project-list">
    {#each user['projects'] as p (p.id)}
        <div class='project-group'>
            <li class="project" on:click={() => {update(p)}}>{p.name} | {p.date}</li>
            <input type='submit' class = "delete" value={"\u00D7"} on:click={() => delete_proj(p.id)}>
        </div>
    {/each}
</ul>

<style>
.project-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.project-list .project {
    background-color: #63B0E3;
    color: #0F3A57;
    padding: 10px 15px;
    border-radius: 5px;
    margin-bottom: 10px;
    margin-right: 10px;
    cursor: pointer;
    font-size: 20px;
    text-align: center;
    width: 100%;
}

.project-group {
    display: flex;
    align-items: center;
}

.delete {
    background-color: #63B0E3;
    color: #0F3A57;
    border: none;
    border-radius: 50%;
    cursor: pointer;
}
</style>