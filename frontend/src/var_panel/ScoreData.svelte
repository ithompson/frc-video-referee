<script>
    import AllianceScoreData from "./AllianceScoreData.svelte";
</script>

<div class="score-root">
    <AllianceScoreData is_blue={true} />
    <AllianceScoreData is_blue={false} />
</div>

<style>
    .score-root {
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
</style>
