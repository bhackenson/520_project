<script>
     import { goto } from '$app/navigation'

     const redirectToLogin = () => {
        goto('/login');
     }
     const redirectToRegister = () => {
        goto('/register');
    };

</script>
    
    <div class="container">
        <div id="musaic">mus(ai)c</div>
        <div id="ai-powered">an ai-powered music application</div>
        <div id="login-box"></div>
        <div id="login">
            <input type='submit' class="submit" value="Login" on:click={redirectToLogin}>
        </div>
        <div id="signup-box"></div>
        <div id="signup">
            <input type='submit' class="submit" value="Signup" on:click={redirectToRegister}>
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

.submit {
        border-style: none;
        display: block;
        width: 100%;
        font-size: 3rem;
        background: #63B0E3;
        /* padding: 1rem 1rem; */
        color: white;
        border-radius: 0.5rem;
        /* margin-bottom: 1rem; */
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

/* login box */
#login-box {
    width: 440px;
    height: 167px;
    position: absolute;
    left: 211px;
    top: 429px;
    background: #63B0E3;
}

/* login text */
#login {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 314px;
    top: 479px;
    text-align: center;
    color: #EEF6FC;
    font-size: 50px;
    font-weight: 400;
    word-wrap: break-word;
}

/* signup box */
#signup-box {
    width: 440px;
    height: 167px;
    position: absolute;
    left: 766px;
    top: 429px;
    background: #63B0E3;
}

/* signup text */
#signup {
    width: 235px;
    height: 67px;
    position: absolute;
    left: 869px;
    top: 479px;
    text-align: center;
    color: #185D8B;
    font-size: 50px;
    font-weight: 400;
    word-wrap: break-word;
}

</style>