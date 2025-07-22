<script lang="ts">
    import type { HyperdeckPlaybackState } from "../lib/model";

    interface Props {
        arena_connected: boolean;
        hyperdeck_connected: boolean;
        match_name: string;
        match_time_sec: number;
        playback_state: HyperdeckPlaybackState;
    }

    let {
        arena_connected,
        hyperdeck_connected,
        match_name,
        match_time_sec,
        playback_state,
    }: Props = $props();
</script>

<header>
    <div class="banner_data">
        Connection Status: {arena_connected ? "Connected" : "Disconnected"}
    </div>
    <div class="banner_title">{match_name}</div>
    <div class="banner_data">Match Time: {match_time_sec} seconds</div>
</header>

<style>
    header {
        width: 100%;
        color: var(--text-active-dark);
        background-color: var(--neutral-banner);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18pt;

        --banner-title-angle: 30deg;
    }

    .banner_data {
        flex: 1 1 0%;
    }

    .banner_title {
        contain: layout;
        background-color: black;
        width: fit-content;
        color: var(--text-active);
        white-space: nowrap;
        font-weight: normal;
        z-index: 0;
        padding: 0 0.5em;

        &::before,
        &::after {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            background-color: black;
            z-index: -1;
        }

        &::before {
            left: 0;
            transform: skewX(var(--banner-title-angle));
            transform-origin: left bottom;
        }
        &::after {
            right: 0;
            transform: skewX(calc(var(--banner-title-angle) * -1));
            transform-origin: right bottom;
        }
    }
</style>
