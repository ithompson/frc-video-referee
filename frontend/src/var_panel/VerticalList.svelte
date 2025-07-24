<script lang="ts">
    import type { Snippet } from "svelte";

    interface Props {
        item: Snippet;
    }

    let { item }: Props = $props();
</script>

<div class="vertical-list">
    {@render item()}
    {@render item()}
    {@render item()}
</div>

<style>
    .vertical-list {
        height: 100%;
        display: flex;
        flex-direction: column;
        overflow: scroll;
        padding: 10px 0;
        gap: 10px;
    }
</style>
