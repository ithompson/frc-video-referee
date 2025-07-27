<script lang="ts">
    import reef_pole from "../assets/mini_reef_pole.svg";
    import { EndgameStatus, type Score, type ScoreSummary } from "../lib/model";

    let reef_level_rp_threshold = 5;
    let barge_rp_threshold = 14;

    interface Props {
        is_blue: boolean;
        score: Score;
        score_summary: ScoreSummary;
        teams: number[];
        hide_final_score: boolean;
        hide_rp: boolean;
        toggle_rp?: () => void;
        toggle_final_score?: () => void;
        final_score_on_right: boolean;
    }
    let {
        is_blue,
        score,
        score_summary,
        teams,
        hide_final_score,
        hide_rp,
        toggle_rp,
        toggle_final_score,
        final_score_on_right,
    }: Props = $props();

    let l1_total = $derived(score.reef.trough_near + score.reef.trough_far);
    let l2_total = $derived(score.reef.branches[0].filter(Boolean).length);
    let l3_total = $derived(score.reef.branches[1].filter(Boolean).length);
    let l4_total = $derived(score.reef.branches[2].filter(Boolean).length);
    let l1_auto_total = $derived(
        score.reef.auto_trough_near + score.reef.auto_trough_far,
    );
    let l2_auto_total = $derived(
        score.reef.auto_branches[0].filter(Boolean).length,
    );
    let l3_auto_total = $derived(
        score.reef.auto_branches[1].filter(Boolean).length,
    );
    let l4_auto_total = $derived(
        score.reef.auto_branches[2].filter(Boolean).length,
    );

    function leaveText(state: boolean): string {
        return state ? "Leave" : "None";
    }

    function endgameText(state: EndgameStatus): string {
        switch (state) {
            case EndgameStatus.DEEP_CAGE:
                return "Deep";
            case EndgameStatus.SHALLOW_CAGE:
                return "Shallow";
            case EndgameStatus.PARKED:
                return "Park";
            case EndgameStatus.NONE:
                return "None";
            default:
                return "";
        }
    }
</script>

{#snippet rpCheck(count: number, threshold: number)}
    {#if count >= threshold}
        <span class="rp-check rp-ok">✓</span>
    {:else}
        <span class="rp-check rp-miss">✗</span>
    {/if}
{/snippet}

{#snippet teamStatus(team: number, msg: string, highlight: boolean = false)}
    <div class="status-box" class:highlight>
        <div class="status-row1">{team}</div>
        <div class="status-row2">{msg}</div>
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
    <div class="score-header" class:swap={final_score_on_right}>
        <div
            class="score-total"
            role="button"
            tabindex="0"
            onclick={toggle_final_score}
            onkeydown={toggle_final_score}
        >
            {#if !hide_final_score}
                {score_summary.score}
            {/if}
        </div>
        <div class="score-banner">
            {is_blue ? "Blue" : "Red"} Alliance Score
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Auto</div>
        <div class="score-content auto-score">
            {#each teams as team, idx}
                {@render teamStatus(
                    team,
                    leaveText(score.leave_statuses[idx]),
                    score.leave_statuses[idx],
                )}
            {/each}
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Scoring</div>
        <div class="score-content reef-algae-container">
            <img class="reef-pole" src={reef_pole} alt="Reef Pole" />
            <div class="reef-totals">
                {@render reefTotal(l4_total, l4_auto_total)}
                {@render reefTotal(l3_total, l3_auto_total)}
                {@render reefTotal(l2_total, l2_auto_total)}
                {@render reefTotal(l1_total, l1_auto_total)}
            </div>
            <div class="algae-container">
                <div class="algae-barge">Barge: {score.barge_algae}</div>
                <div class="algae-processor">
                    Processor: {score.processor_algae}
                </div>
            </div>
        </div>
    </div>
    <div class="score-card">
        <div class="score-title">Endgame</div>
        <div class="score-content endgame-score">
            {#each teams as team, idx}
                {@render teamStatus(
                    team,
                    endgameText(score.endgame_statuses[idx]),
                    score.endgame_statuses[idx] !== EndgameStatus.NONE,
                )}
            {/each}
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
                <div class="status-box">
                    <div class="status-row1">Auto</div>
                    <div class="status-row2">
                        {@render rpCheck(
                            score_summary.auto_bonus_ranking_point ? 1 : 0,
                            1,
                        )}
                    </div>
                </div>
                <div class="status-box">
                    <div class="status-row1">Coral</div>
                    <div class="status-row2">
                        {score_summary.num_coral_levels}/{score_summary.num_coral_levels_goal}
                        {@render rpCheck(
                            score_summary.coral_bonus_ranking_point ? 1 : 0,
                            1,
                        )}
                    </div>
                </div>
                <div class="status-box">
                    <div class="status-row1">Barge</div>
                    <div class="status-row2">
                        {score_summary.barge_points}/{barge_rp_threshold}
                        {@render rpCheck(
                            score_summary.barge_bonus_ranking_point ? 1 : 0,
                            1,
                        )}
                    </div>
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

            &.swap {
                flex-direction: row-reverse;
            }

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

    .status-box {
        border-radius: 8px;
        height: 3.5em;
        width: 5em;
        overflow: clip;

        & div {
            height: 50%;
            align-content: center;
            padding: 0 0.2em;
        }

        & .status-row1 {
            background-color: var(--alliance-highlight);
        }

        &:not(.highlight) .status-row2 {
            background-color: var(--neutral-action);
        }
        &.highlight .status-row2 {
            background-color: var(--alliance-action);
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
</style>
