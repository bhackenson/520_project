<script>
    import ProjectList from "./ProjectList.svelte";
    export let userid;
    
</script>
    <!-- main container -->
    <div class="container">
        <header>
            <div class="button" id='share-proj'>share project</div>
            <div class=title>
                <div id="musaic">mus(ai)c</div>
                <div id="ai-powered">an ai-powered music application</div>
            </div>
            <div class="button" id='account-info'>account info</div>
        </header>

        <!-- main content section -->
        <div class="main-content">
            <!-- projects section -->
            <div class="projects-section">
                <div class="header">
                    <div class="projects-text">projects</div>
                    <button class="add-btn">+</button>
                </div>
                <ProjectList userid={userid}/>
                <!--
                    <ul class="project-list">
                    <li class="project">project name 1</li>
                    <li class="project">project name 2</li>
                    <li class="project">project name 3</li>
                    <li class="project">project name 4</li>
                    <li class="project">project name 5</li>
                    <li class="project">project name 6</li>
                </ul>
                -->
            </div>

            <!-- progressions section -->
            <div class="progressions-section">
                <div class="header">
                    <div class="progressions-text">progressions</div>
                    <button class="add-btn">+</button>
                </div>
                <!-- progression 1 -->
                <div class="progression">
                    <div class="progression-text">progression 1</div>
                    <div class="lines"></div>
                    <div class="actions">
                        <button class="play-btn">play</button>
                        <button class="edit-btn">edit</button>
                        <button class="export-btn">export</button>
                    </div>
                </div>
                <!-- progression 2 -->
                <div class="progression">
                    <div class="progression-text">progression 2</div>
                    <div class="lines"></div>
                    <div class="actions">
                        <button class="play-btn">play</button>
                        <button class="edit-btn">edit</button>
                        <button class="export-btn">export</button>
                    </div>
                </div>
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
    height: 100vh;
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
    justify-content: space-between;
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