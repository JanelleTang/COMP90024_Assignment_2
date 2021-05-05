<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="/">Project Name</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item class="hov" href="/data/">Data vis #1</b-nav-item>
        <b-nav-item class="hov" href="/dashboard/">Data vis #2</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<style>
    .navbar{
        padding:10px 30px;
        z-index: 999;
    }
    .hov a:hover {
        background-color: rgb(143, 143, 143);
        color: #404040;
    }   
</style>

