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
                console.log("Failed to fetch workouts.");
            }
            return;
        }
      const data = await res.json();
      Store.set(data);
    });
  
    Store.subscribe((_projects) => {
      projects = _workouts;
      console.log(`projects: ${JSON.stringify(_projects)}`);
    });
    /*
    const delete_wkt = async (wktid) => {
        const res1 = await fetch(`http://localhost:4000/workouts/delete/${wktid}`, {
          method: 'GET',
          headers: { 
            'Authorization':  `Bearer ${sessionStorage.getItem('jwt')}`},
        });
        if (!res1.ok) {
          if (res1.status == 401) {
            console.log("Unauthorized access.");
            alert("Unauthorized access.")
            sessionStorage.removeItem('jwt');
            goto("/");
          }
          else {
            console.log("Failed to delete workout.");
          }
          return;
        }
  
        const res2 = await fetch(`http://localhost:4003/workouts`, {
          method: 'GET',
          headers: { 
            'Authorization':  `Bearer ${sessionStorage.getItem('jwt')}`},
        });
        if (!res2.ok) {
          if (res2.status == 401) {
            console.log("Unauthorized access.");
            alert("Unauthorized access.")
            sessionStorage.removeItem('jwt');
            goto("/");
          }
          else {
            console.log("failed to fetch workouts.");
          }
          return;
        }
        const data2 = await res2.json();
        Store.update((_workouts) => {
            return data2;
        })
    }
    */
  
  </script>