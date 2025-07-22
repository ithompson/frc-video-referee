<script lang="ts">
    interface Props {
        is_blue: boolean;
    }
    let { is_blue }: Props = $props();
</script>

<div class="alliance-score">
    <div class="alliance-name">{is_blue ? "Blue" : "Red"} Alliance</div>
    <div class="auto-score">Autos go here</div>
    <div class="reef-score">Reef row totals go here</div>
    <div class="algae-container">
        <div class="algae-barge">Barge algae</div>
        <div class="algae-processor">Processor Algae</div>
    </div>
    <div class="endgame-score">Endgames go here</div>

    <div class="rp-summary">RP totals go here</div>
</div>
