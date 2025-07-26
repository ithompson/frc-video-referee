<script lang="ts">
    import type { HyperdeckStatus } from "../lib/model";

    interface Props {
        server_connected: boolean;
        arena_connected: boolean;
        hyperdeck_connected: boolean;
        match_name: string;
        match_time_sec: number;
        hyperdeck_status: HyperdeckStatus;
    }

    let {
        server_connected,
        arena_connected,
        hyperdeck_connected,
        match_name,
        match_time_sec,
        hyperdeck_status,
    }: Props = $props();
</script>

{#snippet status(ok: boolean)}
    {#if ok}
        <span class="status-check status-ok">✓</span>
    {:else}
        <span class="status-check status-err">✗</span>
    {/if}
{/snippet}

<header>
    <div class="banner_data">
        Server: {@render status(server_connected)}
        Arena: {@render status(arena_connected)}
        Hyperdeck: {@render status(hyperdeck_connected)}
    </div>
    <div class="banner_title">{match_name}</div>
    <div class="banner_data">Teleop 1:23 (Pause) 00:00:00.1234</div>
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

    .status-check {
        font-weight: bold;
        display: inline-block;
        inline-size: 1em;
    }

    .status-ok {
        color: green;
    }

    .status-err {
        color: red;
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
