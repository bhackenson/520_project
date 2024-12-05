<script>
    import { goto } from '$app/navigation'
    let username = "";
    let password1 = "";
    let password2 = "";

    const register = async () => {
        if (username === "" || password1 === "" || password2 === "") {
            alert("Please fill in all fields.");
            return;
        }
        if (!(password1 === password2)) {
            alert("Passwords do not match.")
            return;
        }
        const response = await fetch('http://localhost:5000/api/create_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify({
                username,
                password: password1
            })
        });
        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('userid', data.userid);
            goto(`/login`);
            alert("User added!")
        }
        else {
            if (response.status == 404) {
                alert ("Username already exists.")
            }
            else {
                goto(`/`);
                alert("Could not register new user.")
            }
        }
    };

    const redirect = () => {
        goto('/login');
    };

</script>
    <div class="container">
        <div id="musaic">mus(ai)c</div>
        <div id="ai-powered">an ai-powered music application</div>
        <div id="signup-text">sign up</div>
        <div id="username-box"></div>
        <div id="enter-username">
            <input type="text" class="input" bind:value={username} name="login_username" placeholder="Enter Username">
        </div>
        <div id="password-box"></div>
        <div id="enter-password">
            <input type="text" class="input" bind:value={password1} name="login_password" placeholder="Enter Password">
        </div>
        <div id="confirm-password-box"></div>
        <div id="confirm-password">
            <input type="text" class="input" bind:value={password2} name="login_password" placeholder="Confirm Password">
        </div>
        <div id="signup-box"></div>
        <div id="signup">
            <input type='submit' class="submit" value="Signup" on:click={register}>
        </div>
        <div id="have-account">
            <button id="btn-sign-in" on:click={redirect}><u>Already have an account? Sign in!</u></button>
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
        margin-bottom: 1rem;
        background: #2280BF;
        cursor: pointer;

}

#btn-sign-in {
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
    left: 454px;
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
    left: 431px;
    top: 213px;
    text-align: center;
    color: #185D8B;
    font-size: 30px;
    font-weight: 400;
    word-wrap: break-word;
}

/* signup text */
#signup-text {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 603px;
    top: 282px;
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
    left: 358px;
    top: 372px;
    background: #63B0E3;
}

/* enter username text */
#enter-username {
    width: 663px;
    height: 60px;
    position: absolute;
    left: 389px;
    top: 390px;
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
    left: 358px;
    top: 501px;
    background: #97CAED;
}

/* enter password text */
#enter-password {
    width: 663px;
    height: 60px;
    position: absolute;
    left: 389px;
    top: 519px;
    text-align: center;
    color: #185D8B;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* confirm password box */
#confirm-password-box {
    width: 724px;
    height: 96px;
    position: absolute;
    left: 358px;
    top: 630px;
    background: #3498DB;
}

/* confirm password text */
#confirm-password {
    width: 663px;
    height: 60px;
    position: absolute;
    left: 389px;
    top: 648px;
    text-align: center;
    color: #CBE5F6;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* signup box */
#signup-box {
    width: 317px;
    height: 96px;
    position: absolute;
    left: 562px;
    top: 759px;
    background: #2280BF;
}

/* signup button */
#signup {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 603px;
    top: 773px;
    text-align: center;
    color: #EEF6FC;
    font-size: 50px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    word-wrap: break-word;
}

/* have an account text */
#have-account {
    width: 532px;
    height: 36px;
    position: absolute;
    left: 454px;
    top: 888px;
    text-align: center;
    color: #0F3A57;
    font-size: 30px;
    font-family: Inter, sans-serif;
    font-weight: 400;
    text-decoration: underline;
    word-wrap: break-word;
}
</style>