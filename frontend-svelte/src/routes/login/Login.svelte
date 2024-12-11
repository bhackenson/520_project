<script lang="js">
    import { goto } from '$app/navigation'

    let username = "";
    let password = "";

    const authenticate = async () => {
        if (username === "" || password === "") {
            alert ("Please fill in all fields.")
            return;
        }
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({
                username,
                password
            })
        });
        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('userid', data.userid);
            goto(`/home/${data.username}`);
        } else {
            if (response.status == 400) {
                alert("Incorrect username or password.")
                return;
            }
            else {
                console.error('Authentication failed.');
                alert("Authentication failed.")
                return;
            }
        }
    
    };

    const redirect = () => {
        goto('/register');
    };
</script>
<!--- 
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
</head>
-->
    <div class="container">
        <div id="musaic">mus(ai)c</div>
        <div id="ai-powered">an ai-powered music application</div>
        <div id="login-text">log in</div>
        <div id="username-box"></div>
        <div id="enter-username">
            <input type="text" class="input" bind:value={username} name="login_username" placeholder="Enter Username">
        </div>
        <div id="password-box"></div>
        <div id="enter-password">
            <input type="text" class="input" bind:value={password} name="login_password" placeholder="Enter Password">
        </div>
        <div id="login-box"></div>
        <div id="no-account">
            <button id="btn-sign-up" on:click={redirect}><u>don't have an account? sign up!</u></button>
        </div>
        <div id="login">
                <input type='submit' class="submit" value="Submit" on:click={authenticate} name="Login">
        </div>
    </div>
<style>
    /* container style */
.container {
    width: 100%;
    height: 100%;
    position: relative;
    background: #CBE5F6;
}

.input {
        border-style: none;
        display: block;
        width: 95%;
        font-size: 1.125rem;
        padding: 1rem 1rem;
    }

.submit {
        border-style: none;
        display: block;
        width: 100%;
        font-size: 2rem;
        padding: 1rem 1rem;
        color: white;
        /* background-color: rgb(104, 75, 125); */
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background: #3498DB;
        cursor: pointer;

}

#btn-sign-up {
        border-style: none;
        width: 100%;
        font-size: 1.5rem;
        padding: 1rem 1rem;
        color: black;
        margin-bottom: 1rem;
        background: white;
        cursor: pointer;
}

/* musaic text */
#musaic {
    width: 532px;
    height: 145px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 68px;
    text-align: center;
    color: #0F3A57;
    font-size: 120px;
    font-weight: 400;
    word-wrap: break-word;
}

/* ai-powered text */
#ai-powered {
    width: 578px;
    height: 36px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 213px;
    text-align: center;
    color: #185D8B;
    font-size: 30px;
    font-weight: 400;
    word-wrap: break-word;
}

/* log in text */
#login-text {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 291px;
    text-align: center;
    color: #0F3A57;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* username box */
#username-box {
    width: 724px;
    height: 96px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 381px;
    background: #63B0E3;
}

/* enter username text */
#enter-username {
    width: 663px;
    height: 60px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 399px;
    text-align: center;
    color: #EEF6FC;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* password box */
#password-box {
    width: 724px;
    height: 96px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 527px;
    background: #97CAED;
}

/* enter password text */
#enter-password {
    width: 663px;
    height: 60px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 545px;
    text-align: center;
    color: #185D8B;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* login box */
#login-box {
    width: 317px;
    height: 96px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 673px;
    background: #3498DB;
}

/* login button text */
#login {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 687px;
    text-align: center;
    color: #CBE5F6;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* no account text */
#no-account {
    width: 532px;
    height: 36px;
    position: absolute;
    left: 50%;
		transform: translateX(-50%);
    top: 819px;
    text-align: center;
    color: #0F3A57;
    font-size: 30px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    text-decoration: underline;
    word-wrap: break-word;
}

</style>