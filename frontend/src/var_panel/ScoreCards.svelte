<script lang="ts">
    import {
        Alliance,
        type Score,
        type ScoreSummary,
        type TeamTable,
    } from "../lib/model";
    import AllianceScoreCard from "./AllianceScoreCard.svelte";

    interface Props {
        hide_scores: boolean;
        red_score: Score;
        blue_score: Score;
        red_score_summary: ScoreSummary;
        blue_score_summary: ScoreSummary;
        teams: TeamTable;
        swap: boolean;
        reef_level_rp_threshold: number;
        barge_rp_threshold: number;
    }
    let {
        hide_scores,
        red_score,
        blue_score,
        red_score_summary,
        blue_score_summary,
        teams,
        swap,
        reef_level_rp_threshold,
        barge_rp_threshold,
    }: Props = $props();

    let hide_rp = $state(true);
    let hide_final_score = $state(true);
</script>

<div class="score-root" class:swap>
    <AllianceScoreCard
        is_blue={true}
        score={blue_score}
        score_summary={blue_score_summary}
        teams={[
            teams[Alliance.BLUE][0],
            teams[Alliance.BLUE][1],
            teams[Alliance.BLUE][2],
        ]}
        hide_final_score={hide_scores && hide_final_score}
        hide_rp={hide_scores && hide_rp}
        toggle_final_score={() => (hide_final_score = !hide_final_score)}
        toggle_rp={() => (hide_rp = !hide_rp)}
        final_score_on_right={!swap}
        {reef_level_rp_threshold}
        {barge_rp_threshold}
    />
    <AllianceScoreCard
        is_blue={false}
        score={red_score}
        score_summary={red_score_summary}
        teams={[
            teams[Alliance.RED][0],
            teams[Alliance.RED][1],
            teams[Alliance.RED][2],
        ]}
        hide_final_score={hide_scores && hide_final_score}
        hide_rp={hide_scores && hide_rp}
        toggle_final_score={() => (hide_final_score = !hide_final_score)}
        toggle_rp={() => (hide_rp = !hide_rp)}
        final_score_on_right={swap}
        {reef_level_rp_threshold}
        {barge_rp_threshold}
    />
</div>

<style>
    .score-root {
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
    .score-root.swap {
        flex-direction: row-reverse;
    }
</style>
