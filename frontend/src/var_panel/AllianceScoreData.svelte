<script lang="ts">
    interface Props {
        is_blue: boolean;
    }
    let { is_blue }: Props = $props();
</script>

{#snippet teamStatus(team: number, msg: string, highlight: boolean = false)}
    <div class="team-status" class:highlight>
        <div class="team-number">{team}</div>
        <div class="status">{msg}</div>
    </div>
{/snippet}

<div class="alliance-score" class:red={!is_blue} class:blue={is_blue}>
    <div class="auto-score">
        {@render teamStatus(11932, "Leave", true)}
        {@render teamStatus(2623, "None", false)}
        {@render teamStatus(272, "Leave", true)}
    </div>
    <div class="reef-algae-container">
        <div class="reef-pole">Reef pole icon</div>
        <div class="reef-totals">
            <div>6/5 ✓ A:1</div>
            <div>3/5 ✗ A:0</div>
            <div>5/5 ✓ A:2</div>
            <div>2/5 ✗ A:3</div>
        </div>
        <div class="algae-container">
            <div class="algae-barge">Barge: 5</div>
            <div class="algae-processor">Processor: 3</div>
        </div>
    </div>
    <div class="endgame-score">
        {@render teamStatus(11932, "Deep", true)}
        {@render teamStatus(2623, "None", false)}
        {@render teamStatus(272, "Shallow", true)}
    </div>

    <div class="rp-summary">RP totals go here</div>
</div>

<style>
    .alliance-score {
        background-color: var(--alliance-background);
        padding: 20px;
        margin: 10px;
        border-radius: 20px;
        border: 4px solid var(--alliance-highlight);
        box-shadow: 0 0 10px black;
        overflow: clip;
    }

    .auto-score,
    .endgame-score {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }

    .team-status {
        border-radius: 8px;
        height: 3.5em;
        width: 5em;
        overflow: clip;

        & div {
            height: 50%;
            align-content: center;
            padding: 0 0.2em;
        }

        & .team-number {
            background-color: var(--alliance-action);
        }

        &:not(.highlight) .status {
            background-color: var(--neutral-action);
        }
        &.highlight .status {
            background-color: var(--alliance-highlight);
        }
    }

    .reef-algae-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 0.5em;
    }
</style>
