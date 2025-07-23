<script>
    import AllianceScoreCard from "./AllianceScoreCard.svelte";

    let hide_scores = $state(true);

    let hide_rp = $state(true);
    let hide_final_score = $state(true);
</script>

<div class="score-root">
    <AllianceScoreCard
        is_blue={true}
        hide_final_score={hide_scores && hide_final_score}
        hide_rp={hide_scores && hide_rp}
        toggle_final_score={() => (hide_final_score = !hide_final_score)}
        toggle_rp={() => (hide_rp = !hide_rp)}
    />
    <AllianceScoreCard
        is_blue={false}
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
