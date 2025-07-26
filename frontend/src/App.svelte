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
  import { PLACEHOLDER_SCORE, PLACEHOLDER_SCORE_SUMMARY } from "./lib/model";

  interface Props {
    ws: WebSocketClient;
  }

  let { ws }: Props = $props();

  let displayed_match = $derived(server_state.current_match);

  let realtime_data = $derived(server_state.controller_status.realtime_data);
  let red_score = $derived(
    realtime_data ? server_state.realtime_score.red.score : PLACEHOLDER_SCORE,
  );
  let blue_score = $derived(
    realtime_data ? server_state.realtime_score.blue.score : PLACEHOLDER_SCORE,
  );
  let red_score_summary = $derived(
    realtime_data
      ? server_state.realtime_score.red.score_summary
      : PLACEHOLDER_SCORE_SUMMARY,
  );
  let blue_score_summary = $derived(
    realtime_data
      ? server_state.realtime_score.blue.score_summary
      : PLACEHOLDER_SCORE_SUMMARY,
  );

  let sorted_matches = $derived(
    Object.values(server_state.matches).sort((a, b) =>
      a.var_data.timestamp < b.var_data.timestamp
        ? 1
        : b.var_data.timestamp < a.var_data.timestamp
          ? -1
          : 0,
    ),
  );

  let event_list = $derived(sorted_matches[0]?.var_data.events || []);
  let event_list_with_idx = $derived(
    event_list.map((event, idx) => ({ event_idx: idx + 1, event })),
  );
</script>

<div class="top-container">
  <StatusHeader
    server_connected={ws.state.connected}
    arena_connected={server_state.arena_connected}
    hyperdeck_connected={server_state.hyperdeck_connected}
    match_name={displayed_match.long_name}
    match_time_sec={server_state.match_time?.match_time_sec || 0}
    match_timing={server_state.match_timing}
    hyperdeck_status={server_state.hyperdeck_status}
  />

  <main>
    <div class="match-ui-container">
      <div class="scoring-container">
        <ScoreCards
          hide_scores={realtime_data}
          {red_score}
          {blue_score}
          {red_score_summary}
          {blue_score_summary}
          match={displayed_match}
        />
      </div>
      <div class="flex-spacer" style="flex: 1 1 0%"></div>
      <div class="event-info-container">
        <EventCard />
      </div>
      <div class="timeline-container">
        <Timeline events={event_list_with_idx} />
      </div>
    </div>
    <div class="events list-container">
      <button class="add-event">Add VAR Review</button>
      <VerticalList
        data={event_list_with_idx.reverse()}
        key_func={(event) => event.event.event_id}
      >
        {#snippet item(data)}
          <EventListEntry
            event_idx={data.event_idx}
            event={data.event}
            match_timing={server_state.match_timing}
          />
        {/snippet}
      </VerticalList>
    </div>
    <div class="matches list-container">
      <button class="go-live">Go Live</button>
      <VerticalList
        data={sorted_matches}
        key_func={(match) => match.var_data.var_id}
      >
        {#snippet item(data)}
          <MatchListEntry match={data} />
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

  button {
    background-color: var(--gray-600);
    color: var(--text-active-dark);
    border-radius: 8px;
    font-weight: bold;
    margin-top: 10px;
    height: 4em;
    box-shadow: 0 0 12px black;

    &.add-event {
      background-color: var(--blue-200);
      width: 160px;
    }

    &.go-live {
      background-color: var(--red-400);
      width: 140px;
    }
  }
</style>
