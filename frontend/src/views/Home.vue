<template>
    <div class="home">     
        <Navbar></Navbar>
        <div id="background-wrapper">
            <div class="container-fluid landing-pg" >
                <h1 class="display-3 mb-4 wte">COMP90024 Assignment 2</h1>
                <table class="table table-borderless table-sm">
                    <tbody>
                        <tr>
                        <td class="bld wte">Insert names</td>
                        <td class="bld wte">Insert names</td>
                        <td class="bld wte">Insert names</td>
                        <td class="bld wte">Insert names</td>
                        <td class="bld wte">Insert names</td>
                        </tr>
                        <tr>
                        <td class='wte'>Insert id</td>
                        <td class='wte'>Insert id</td>
                        <td class='wte'>Insert id</td>
                        <td class='wte'>Insert id</td>
                        <td class='wte'>Insert id</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="row card-container">
                <div class="col-sm-6">
                    <div class="card">
                    <div class="card-body">
                        <img class="card-img-top" src="https://via.placeholder.com/100x50" alt="Card image">
                        <h5 class="card-title">Data vis 1</h5>
                        <p class="card-text">enter some description</p>
                        <b-button variant="info" href='/data/'>Visit</b-button>
                    </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="card">
                    <div class="card-body">
                        <img class="card-img-top" src="https://via.placeholder.com/100x50" alt="Card image">
                        <h5 class="card-title">Data vis 2</h5>
                        <p class="card-text">enter some description</p>
                        <b-button variant="info" href='/dashboard/'>Visit</b-button>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from '../components/Navbar'
    export default{
        name:'Home',
         components: {
             Navbar
            },
        data() {
            return{
                show: false
            }
        }

    }
</script>

<style>
    .landing-pg {
        margin: auto;
        width: 70%;
        text-align: center;
        height:100px;
        padding:20vh 0;
        z-index: 100;

    }

    #background-wrapper {
        background:linear-gradient(0deg, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.7)), url(../assets/bg.jpeg);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        background-size: cover;
        -o-background-size: cover;
        z-index:1
    }

    .card-container{
        padding: 5vh 20vw;
        
    }
    .card {
        box-shadow: 3px 3px #565656;
    }
    .bld{
        font-weight: 600;
    }
    .wte{
        color:white
    }
</style>