<script>
	import ProjectCreate from "./ProjectCreate.svelte";
    import ProgressionCreate from "./ProgressionCreate.svelte";
    import ProjectList from "./ProjectList.svelte";
    import ProgressionList from "./ProgressionList.svelte";
    import Store from "./Store.js";
	import StoreEval from "./StoreEval.js";
	import { goto } from "$app/navigation";

    export let userid;
    export let username;

    let isProjectCreateVisible = false;
    let isProgCreateVisible = false;

    let currProj = {};
    const updateCurrProj = (obj) => { currProj = obj; }

    const openProjectCreate = () => {
        isProjectCreateVisible = true;
    }
    const closeProjectCreate = () => {
        isProjectCreateVisible = false;
    }
    const openProgCreate = () => {
        isProgCreateVisible = true;
    }
    const closeProgCreate = function() {
        isProgCreateVisible = false;
    }

    const create_proj = async (project_name) => {
        let D = new Date();
        let day = D.getDate();
        let month = D.getMonth() + 1;
        let year = D.getFullYear();
        const date = month + '/' + day + '/' + year;
        const response = await fetch('http://localhost:5000/api/create_project', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, "name": project_name, date})
        });
        if (!response.ok) {
            if (response.status == 400) {
                console.log("Could not find user.")
            }
            else {
                console.log("Failed to find user.");
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
        isProjectCreateVisible = false;
    }

    const get_progs = async (obj) => {
        const {name, key_signature, mode, time_signature, tempo} = obj;
        const response1 = await fetch('http://localhost:5000/api/get_progression', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, name, key_signature, mode, time_signature, tempo})
        });
        if (!response1.ok) {
            if (response1.status == 400) {
                alert("Error creating progression.")
            }
            else {
                console.log("Error creating progression.");
            }

        }
        const response2 = await fetch('http://localhost:5000/api/get_progression', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid, name, key_signature, mode, time_signature, tempo})
        });
        if (!response2.ok) {
            if (response2.status == 400) {
                alert("Error creating progression.")
            }
            else {
                console.log("Error creating progression.");
            }

        }
        const data1 = await response1.json()
        const data2 = await response2.json()
        StoreEval.update((progs) => {
            return {prog1: data1.progression, prog2: data2.progression}
        })

            //return data.progression;
    }

    const logout = () => {
        goto('/')
    }
  
        /*
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
        */
    
</script>
    <!-- main container -->
    <div class="container">
        <header>
            <!-- <div class="button" id='share-proj'>logout</div> -->
            <input type="submit" class="button" id="share-proj" value="Logout" on:click={logout}/>
            <div class=title>
                <div id="musaic">mus(ai)c</div>
                <div id="ai-powered">an ai-powered music application</div>
            </div>
            <div id='account-info'><b>Hi, {username}</b></div>
        </header>

        <!-- main content section -->
        <div class="main-content">
            <!-- projects section -->
            <div class="projects-section">
                <div class="header">
                    <div class="projects-text">Projects</div>
                    <button class="add-btn" on:click={openProjectCreate}>+</button>
                    <ProjectCreate visible={isProjectCreateVisible} closeProjectCreate={closeProjectCreate} createProject={create_proj}/>
                </div>
                <ProjectList userid={userid} updateProj={updateCurrProj}/>
            </div>

            <!-- progressions section -->
            <div class="progressions-section">
                <div class="header">
                    <div class="progressions-text">Progressions</div>
                    <button class="add-btn" on:click={openProgCreate}>+</button>
                    <ProgressionCreate visible={isProgCreateVisible} close={closeProgCreate} getProgs={get_progs} userid={userid} project={currProj}/>
                </div>

                <ProgressionList userid={userid} project={currProj}/>
            </div>

        </div>
    </div>
<style>

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    padding: 20px;
    box-sizing: border-box;
}

header {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

#musaic {
    color: #0F3A57;
    font-size: 80px;
    font-weight: 400;
}

#ai-powered {
    text-align: center;
    color: #185D8B;
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 1rem;
}

#share-proj {
    margin-right: 80%;
}

#account-info {
    margin-left: 80%;
    font-size: xx-large;
    color: #185D8B;
}

header .button {
    background-color: #0F3A57;
    color: white;
    font-size: 30px;
    font-weight: 400;
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    font-family: 'Times New Roman', Times, serif;
}

.main-content {
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 100%;
}

.projects-section,
.progressions-section {
    background-color: #97CAED;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.projects-section {
    flex: 1;
    margin-right: 20px;
}

.progressions-section {
    flex: 2;
    display: flex;
    flex-direction: column;
    /* justify-content: space-between; */
}

.projects-section .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.projects-section .header .projects-text {
    color: #185D8B;
    font-size: 35px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word
}

.projects-section .header .add-btn {
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
    cursor: pointer;
    font-size: 20px;
    text-align: center;
}

.progressions-section .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.progressions-section .header .progressions-text{
    /* font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center; */
    text-align: center;
    color: #0F3A57;
    font-size: 35px;
    font-family: Inter;
    font-weight: 400;
    word-wrap: break-word
}

.progressions-section .header .add-btn {
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

.progression {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #CBE5F6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.progression .progressions-text{
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