<template>
  <div class="app min-h-screen bg-base-300 text-base-content">
    <header>
      <h1>Color Picker Game</h1>
      
    </header>
    <HUD />
    <GameBoard  />
    <Leaderboard />
  </div>
</template>

<script setup>
import { useAuthStore } from "./stores/auth";
import GameBoard from "./components/GameBoard.vue";
import Leaderboard from "./components/Leaderboard.vue";
import HUD from "./components/HUD.vue";
import LoginButton from "./components/LoginButton.vue";
const auth = useAuthStore();
</script>

<style>
.app { max-width: 960px; margin: 0 auto; padding: 1rem; }
</style>