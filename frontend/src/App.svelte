<script lang="ts">
  import { server_state } from "./lib/server_state.svelte";
  import type WebSocketClient from "./lib/wsclient.svelte";
  import StatusHeader from "./var_panel/StatusHeader.svelte";
  import MatchListEntry from "./var_panel/MatchListEntry.svelte";
  import EventListEntry from "./var_panel/EventListEntry.svelte";
  import Timeline from "./var_panel/Timeline.svelte";
  import VerticalList from "./var_panel/VerticalList.svelte";
  import EventCard from "./var_panel/EventCard.svelte";
  import ScoreCards from "./var_panel/ScoreCards.svelte";

  interface Props {
    ws: WebSocketClient;
  }

  let { ws }: Props = $props();
</script>

<div class="top-container">
  <StatusHeader
    server_connected={ws.state.connected}
    arena_connected={server_state.arena_connected}
    hyperdeck_connected={server_state.hyperdeck_connected}
    match_name={"Qualification 5"}
    match_time_sec={server_state.match_time?.match_time_sec || 0}
    playback_state={server_state.hyperdeck_playback_state}
  />

  <main>
    <div class="match-ui-container">
      <div class="scoring-container">
        <ScoreCards />
      </div>
      <div class="flex-spacer" style="flex: 1 1 0%"></div>
      <div class="event-info-container">
        <EventCard />
      </div>
      <div class="timeline-container">
        <Timeline />
      </div>
    </div>
    <div class="events list-container">
      <button class="add-event">Add Event</button>
      <VerticalList>
        {#snippet item()}
          <EventListEntry />
        {/snippet}
      </VerticalList>
    </div>
    <div class="matches list-container">
      <button class="go-live">Go Live</button>
      <VerticalList>
        {#snippet item()}
          <MatchListEntry />
        {/snippet}
      </VerticalList>
    </div>
  </main>
</div>

<style>
  @import "./lib/base_colors.css";

  :global(html) {
    height: 100%;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    overscroll-behavior: none;
  }

  :global(body) {
    height: 100%;
    margin: 0;
    touch-action: manipulation;
  }

  .top-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  main {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    overflow: hidden;
    padding-bottom: 20px; /* Spacer for the iOS home bar */

    background:
      radial-gradient(rgba(0, 0, 0, 0.5) 15%, transparent 16%) 0 0,
      radial-gradient(rgba(0, 0, 0, 0.5) 15%, transparent 16%) 8px 8px,
      radial-gradient(rgba(255, 255, 255, 0.05) 15%, transparent 20%) 0 1px,
      radial-gradient(rgba(255, 255, 255, 0.05) 15%, transparent 20%) 8px 9px;
    background-color: var(--gray-700);
    background-size: 16px 16px;
  }

  .match-ui-container {
    flex: 1 1 0%;
    display: flex;
    flex-direction: column;
  }

  .scoring-container {
    width: 100%;
  }

  .timeline-container {
    padding: 0 20px;
  }

  .event-info-container {
    margin: 10px;
    display: flex;
    justify-content: center;
  }

  .list-container {
    height: 100%;
    overflow: hidden;
  }
</style>
