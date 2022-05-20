var authForm  = document.getElementById('Form')


if (authForm) {
    var reMoveable = document.querySelector('.rmv')
    var switcher = document.getElementById('Switch')
    var switcherText = document.querySelector('.switchText')
    var btnText =document.getElementById("action-btn")
        let crt ="Create an Account"
        var acl ="Already have an account ? Login"
        let lgText="Login"
        let caText="Create Account"
        let saveRMV =reMoveable.innerHTML
        reMoveable.innerHTML =""
        switcherText.innerText = crt

        switcher.addEventListener('click',function () {
            
            if(switcherText.innerText == crt){
                switcherText.innerText=acl
                reMoveable.innerHTML =saveRMV
                btnText.value=caText
                authForm.action= window.location.origin+"/signup"
                console.log(authForm)
            }else{
            switcherText.innerText=crt
            reMoveable.innerHTML =""
            btnText.value=lgText
            authForm.action= window.location.origin+"/signin"
            console.log(authForm)

        }
    })

}
