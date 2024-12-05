<script>
    import ProjectEditor from './ProjectEditor.svelte';
    import { page } from '$app/stores';
    let username = $page.params.username;
</script>
<ProjectEditor userid={sessionStorage.getItem('userid')} username={username}/>