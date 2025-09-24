<script lang="ts">
    import { MatchStatus, type VARMatch } from "../lib/model";

    interface Props {
        match: VARMatch;
        onclick?: (match: VARMatch) => void;
    }
    let { match, onclick }: Props = $props();

    let result = $derived(match.arena_data?.result);
    let result_style_class = $derived.by(() => {
        switch (match.arena_data?.status) {
            case MatchStatus.RED_WON:
                return "alliance red";
            case MatchStatus.BLUE_WON:
                return "alliance blue";
            case MatchStatus.TIE:
                return "tie";
            default:
                return "";
        }
    });
</script>

<button class="match-card" tabindex="0" onclick={() => onclick?.(match)}>
    <div class="card-header">{match.var_data.var_id}</div>
    <div class="match-details">
        {#if match.arena_data}
            {#if result}
                <div class="match-section {result_style_class}">
                    {result.red_summary.score} - {result.blue_summary.score}
                </div>
            {/if}
            <div class="match-section team-lists">
                <ol class="red">
                    <li>{match.arena_data.red1}</li>
                    <li>{match.arena_data.red2}</li>
                    <li>{match.arena_data.red3}</li>
                </ol>
                <ol class="blue">
                    <li>{match.arena_data.blue3}</li>
                    <li>{match.arena_data.blue2}</li>
                    <li>{match.arena_data.blue1}</li>
                </ol>
            </div>
        {:else}
            <div class="match-section">No arena data</div>
        {/if}
        {#if !match.clip_available}
            <div class="match-section">No video clip</div>
        {/if}
    </div>
</button>

<style>
    .match-card {
        color: var(--text-active);
        box-sizing: border-box;
        border: 4px solid var(--gray-600);
        border-radius: 10px;
        overflow: clip;
        background-color: var(--gray-700);
        display: flex;
        flex-direction: column;
        width: 140px;
        box-shadow: 0 0 8px black;
        margin: 0 10px;
    }
    .card-header {
        background-color: var(--gray-600);
        font-weight: bold;
        padding: 2px 0.5em 4px 0.5em;
        box-shadow: 0 0px 8px black;
    }

    .match-details {
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding: 5px 0;
        align-items: center;
    }

    .match-section {
        box-sizing: border-box;
        background-color: var(--gray-600);
        border-radius: 8px;
        overflow: clip;
        width: 90%;
        padding: 0.2em;
        box-shadow: 0 0 8px black;
    }
    .match-section.alliance {
        background-color: var(--alliance-overlay-background);
    }
    .match-section.tie {
        background-color: var(--auto-active);
    }

    .team-lists {
        display: flex;
        padding: 0;
        & ol {
            flex: 1 1 0%;
        }
        & .red {
            background-color: var(--red-overlay-background);
        }
        & .blue {
            background-color: var(--blue-overlay-background);
        }
    }
    ol {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
</style>
