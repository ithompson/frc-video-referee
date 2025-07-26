<script lang="ts">
    import type { Snippet } from "svelte";

    interface Props {
        item: Snippet<[any]>;
        key_func: (item: any) => any;
        data: any[];
    }

    let { item, key_func, data }: Props = $props();
</script>

<div class="scroll-container">
    <div class="vertical-list">
        {#each data as value (key_func(value))}
            {@render item(value)}
        {/each}
    </div>
</div>

<style>
    .scroll-container {
        height: 100%;
        overflow: scroll;
        padding: 10px 0;
    }

    .vertical-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>
