<template>
<base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
</base-dialog>
<div class="login-box">
    <img src="../../images/sbtlogo.png" alt="Logo Here" class="avatar">
    <h1>Login Here</h1>
    <form id="login_form" method="POST" @submit.prevent="loginUser">
        <p class="emptyInput" v-if="!isFormValid">Please Enter Your Extension and Secret Password</p>
        <p>Extension</p>
        <input type="text" name="extension" id="extension" placeholder="Enter Extension" v-model="extension">
        <p>Secret</p>
        <input type="password" name="secret" id="secret" placeholder="Enter Secret" v-model="secret">
        <input type="submit" name="submit" id="" value="Login">
        <a href="#">SBTPHILIPPINES APP</a>
    </form>
</div>   
 
</template>


<script>
export default {
    data() {
        return {
            extension: '',
            secret: '',
            isFormValid: true,
            error: null,
            appName: this.$store.getters.getAppName
        }
    },
    methods: {
        loginUser(){
            this.isFormValid = true
            if(this.extension == ''|| this.secret == ''){
                this.isFormValid = false
                return
            }
            this.$store.dispatch('loginUser',{
                extension: this.extension,
                secret: this.secret})
                .then(() => {
                    const position = this.$store.getters['getLoggedinUserData'].position
                    if(position == '99' || position == '20' ||
                      position == '30' || position == '31' || 
                      position == '21' || position =='22'  || position =='0')
                    {
                         this.$router.replace({path: `/${this.appName}/phone/loggedin`})
                    }else if(position == '2' || position == '3' || position == '10'){
                         this.$router.replace({path: `/${this.appName}/callsummaries/csdinbound`})
                    }else if (position == '1'){
                        this.$router.replace ({path: `/${this.appName}/callsummaries/sales`})
                    }else if (position == '40' || position == '41'){
                        this.$router.replace ({path: `/${this.appName}/callsummaries/collection`})
                    }

                   
                }).catch(e => {
                    this.error = e.message
                })
        },
        handleError(){
            this.error = null
            this.extension = ''
            this.secret = ''
        }
    },
    beforeCreate(){
        document.body.className = 'login';
    },
    beforeUnmount(){
       document.body.className = 'home';
    }
}
</script>
<style scoped>

.emptyInput {
    color: red;
    font-weight: 50;
}

.login-box {
    width: 320px;
    height: 420px;
    background:  rgba(0,0,0,0.5);
    color: #fff;
    top: 50%;
    left: 50%; 
    position: absolute;
    transform: translate(-50%, -50%);
    box-sizing: border-box;
     padding: 70px 30px ;
    border-radius: 50px;
}
h1 {
    margin: 0;
    padding: 0 0px 20px;
    text-align: center;
    font-size: 22px;
    

}
.login-box p {
    padding: 0;
    margin: 0;
    font-weight: bold;
}

.login-box input {
    width: 100%;
    margin-bottom: 20px;
}

.login-box input[type="text"], input[type="password"]{

    border: none;
    border-bottom: 1px solid #fff;
    background: transparent;
    outline: none;
    height: 40px;
    color: #fff;
    font-size: 16px;
}
.login-box input[type="submit"] {

    border: none;
    outline: none;
    background: #1c8adb;
    color: #fff;
    font-size: 18px;
    border-radius: 20px;
    height: 40px;

}
.login-box input[type="submit"]:hover {
    cursor: pointer;
    background: #39dc79;
    color: #000;
}

.login-box a {
    text-decoration: none;
    font-size: 14px;
    color: #fff;
    text-align: center;
    padding-left: 50px;

}
.login-box a:hover {
    color: #39dc79;
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    position: absolute;
    top: -50px;
    left: calc(50% - 50px);

}
</style>