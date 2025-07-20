<script lang="ts">
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/assets/vite.svg";
  import Counter from "./lib/Counter.svelte";
  import { server_state } from "./lib/server_state.svelte";
  import { MatchState } from "./lib/model";
  import type WebSocketClient from "./lib/wsclient.svelte";

  interface Props {
    ws: WebSocketClient;
  }

  let { ws }: Props = $props();
</script>

<main>
  <div>
    <a href="https://vite.dev" target="_blank" rel="noreferrer">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div>
  <h1>Vite + Svelte</h1>

  <div class="card">
    <Counter />
  </div>

  <div class="card">
    <h2>Server State</h2>
    <p>
      Server connection: {ws.state.connected ? "Connected" : "Disconnected"}
    </p>
    <p>
      Arena connection: {server_state.arena_connected
        ? "Connected"
        : "Disconnected"}
    </p>
    <p>
      Hyperdeck connection: {server_state.hyperdeck_connected
        ? "Connected"
        : "Disconnected"}
    </p>
    <p>
      Match phase: {server_state.match_time?.match_state !== undefined
        ? MatchState[server_state.match_time.match_state]
        : "Unknown"}
    </p>
    <p>Match time: {server_state.match_time?.match_time_sec} seconds</p>
  </div>

  <p>
    Check out <a
      href="https://github.com/sveltejs/kit#readme"
      target="_blank"
      rel="noreferrer">SvelteKit</a
    >, the official Svelte app framework powered by Vite!
  </p>

  <p class="read-the-docs">Click on the Vite and Svelte logos to learn more</p>
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
