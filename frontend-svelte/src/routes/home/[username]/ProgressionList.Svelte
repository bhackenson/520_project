<script>
    import { onMount } from 'svelte';
    import Store from './Store.js';
    import { goto } from '$app/navigation'
  
    let projects = [];
  
    onMount(async () => {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({userid})
        });
        if (!res.ok) {
            if (res.status == 400) {
                alert("Could not find user.")
                //sessionStorage.removeItem('jwt');
                //goto("/");
            }
            else {
                console.log("Failed to fetch projects.");
            }
            return;
        }
      const data = await res.json();
      Store.set(data);
    });
  
    Store.subscribe((_projects) => {
      projects = _projects;
      console.log(`projects: ${JSON.stringify(_projects)}`);
    });
  
  </script>