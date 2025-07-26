<script lang="ts">
    import { type Match, type Score, type ScoreSummary } from "../lib/model";
    import AllianceScoreCard from "./AllianceScoreCard.svelte";

    interface Props {
        hide_scores: boolean;
        red_score: Score;
        blue_score: Score;
        red_score_summary: ScoreSummary;
        blue_score_summary: ScoreSummary;
        match: Match;
    }
    let {
        hide_scores,
        red_score,
        blue_score,
        red_score_summary,
        blue_score_summary,
        match,
    }: Props = $props();

    let hide_rp = $state(true);
    let hide_final_score = $state(true);
</script>

<div class="score-root">
    <AllianceScoreCard
        is_blue={true}
        score={blue_score}
        score_summary={blue_score_summary}
        teams={[match.blue1, match.blue2, match.blue3]}
        hide_final_score={hide_scores && hide_final_score}
        hide_rp={hide_scores && hide_rp}
        toggle_final_score={() => (hide_final_score = !hide_final_score)}
        toggle_rp={() => (hide_rp = !hide_rp)}
    />
    <AllianceScoreCard
        is_blue={false}
        score={red_score}
        score_summary={red_score_summary}
        teams={[match.red1, match.red2, match.red3]}
        hide_final_score={hide_scores && hide_final_score}
        hide_rp={hide_scores && hide_rp}
        toggle_final_score={() => (hide_final_score = !hide_final_score)}
        toggle_rp={() => (hide_rp = !hide_rp)}
    />
</div>

<style>
    .score-root {
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
</style>
