<script lang="ts">
    import reef_pole from "../assets/mini_reef_pole.svg";

    let reef_level_rp_threshold = 5;

    interface Props {
        is_blue: boolean;
        hide_final_score: boolean;
        hide_rp: boolean;
        toggle_rp?: () => void;
        toggle_final_score?: () => void;
    }
    let {
        is_blue,
        hide_final_score,
        hide_rp,
        toggle_rp,
        toggle_final_score,
    }: Props = $props();
</script>

{#snippet rpCheck(count: number, threshold: number)}
    {#if count >= threshold}
        <span class="rp-check rp-ok">✓</span>
    {:else}
        <span class="rp-check rp-miss">✗</span>
    {/if}
{/snippet}

{#snippet teamStatus(team: number, msg: string, highlight: boolean = false)}
    <div class="team-status" class:highlight>
        <div class="team-number">{team}</div>
        <div class="status">{msg}</div>
    </div>
{/snippet}

{#snippet reefTotal(count: number, auto: number)}
    <div>
        {count}/{reef_level_rp_threshold}
        {@render rpCheck(count, reef_level_rp_threshold)}
        <span class="reef-auto">{auto}</span>
    </div>
{/snippet}

<div class="alliance-score" class:red={!is_blue} class:blue={is_blue}>
    <div class="score-header">
        <div
            class="score-total"
            role="button"
            tabindex="0"
            onclick={toggle_final_score}
            onkeydown={toggle_final_score}
        >
            {#if !hide_final_score}
                {is_blue ? 109 : 273}
            {/if}
        </div>
        <div class="score-banner">
            {is_blue ? "Blue" : "Red"} Alliance Score
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Auto</div>
        <div class="score-content auto-score">
            {@render teamStatus(11932, "Leave", true)}
            {@render teamStatus(2623, "None", false)}
            {@render teamStatus(272, "Leave", true)}
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Scoring</div>
        <div class="score-content reef-algae-container">
            <img class="reef-pole" src={reef_pole} alt="Reef Pole" />
            <div class="reef-totals">
                {@render reefTotal(6, 1)}
                {@render reefTotal(3, 0)}
                {@render reefTotal(5, 2)}
                {@render reefTotal(3, 3)}
            </div>
            <div class="algae-container">
                <div class="algae-barge">Barge: 5</div>
                <div class="algae-processor">Processor: 3</div>
            </div>
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Endgame</div>
        <div class="score-content endgame-score">
            {@render teamStatus(11932, "Deep", true)}
            {@render teamStatus(2623, "None", false)}
            {@render teamStatus(272, "Shallow", true)}
        </div>
    </div>

    <div
        class="score-card"
        role="button"
        tabindex="0"
        onclick={toggle_rp}
        onkeydown={toggle_rp}
    >
        <div class="score-title">RP</div>
        <div class="score-content rp-wrapper" class:hide_rp>
            <div class="rp-summary">
                <div class="rp-display rp-auto">
                    <div class="rp-title">Auto</div>
                    <div class="rp-state">{@render rpCheck(0, 1)}</div>
                </div>
                <div class="rp-display rp-coral">
                    <div class="rp-title">Coral</div>
                    <div class="rp-state">2/4 {@render rpCheck(0, 1)}</div>
                </div>
                <div class="rp-display rp-barge">
                    <div class="rp-title">Barge</div>
                    <div class="rp-state">7/14 {@render rpCheck(0, 1)}</div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .alliance-score {
        background-color: var(--alliance-background);
        padding: 0 10px;
        margin: 10px;
        border-radius: 20px;
        border: 4px solid var(--alliance-overlay-background);
        box-shadow: 0 0 10px black;
        overflow: clip;

        & .score-header {
            display: flex;
            flex-direction: row;
            font-weight: bold;
            align-items: center;
            margin-top: 10px;

            & .score-total {
                background-color: var(--alliance-overlay-background);
                border-radius: 8px;
                box-shadow: 0 0 6px black;
                width: 3.5em;
                height: 2em;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .blue & .score-total {
                order: 3;
            }

            & .score-banner {
                flex: 1 1 0%;
            }
        }
    }

    .score-card {
        background-color: var(--alliance-overlay-background);
        border-radius: 8px;
        box-shadow: 0 0 6px black;
        margin: 10px 0;
        width: 100%;

        display: flex;
        flex-direction: row;
        align-items: center;

        & .score-title {
            font-weight: bold;
            display: inline-block;
            width: 5.5em;
        }

        & .score-content {
            flex: 1 1 0%;
            position: relative;
        }
    }

    .rp-check {
        font-weight: bold;
        display: inline-block;
        inline-size: 1em;
    }

    .rp-ok {
        color: green;
    }

    .rp-miss {
        color: red;
    }

    .auto-score,
    .endgame-score,
    .rp-summary {
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
        height: 140px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 0.5em;
    }

    .reef-pole {
        padding-left: 10px;
        height: 100%;
        object-fit: contain;
    }

    .reef-totals {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        height: 100%;
    }

    .reef-auto {
        color: yellow;
    }

    .algae-container {
        flex: 1 1 0%;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        height: 100%;
    }

    .hide_rp:after {
        content: "Tap to reveal";
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin-inline: auto;
        width: fit-content;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .hide_rp .rp-summary {
        visibility: hidden;
    }
    .rp-display {
        border-radius: 8px;
        height: 3.5em;
        width: 5em;
        overflow: clip;

        & div {
            height: 50%;
            align-content: center;
            padding: 0 0.2em;
        }

        & .rp-title {
            background-color: var(--alliance-action);
        }

        & .rp-state {
            background-color: var(--neutral-action);
        }
    }
</style>
