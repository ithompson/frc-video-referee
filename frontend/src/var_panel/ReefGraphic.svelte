<script lang="ts">
    interface Props {
        mirror: boolean;
        current_scored: [boolean, boolean, boolean];
        auto_scored: [boolean, boolean, boolean];
    }
    let { mirror, current_scored, auto_scored }: Props = $props();

    const coral_positions = [
        { level: 4, x: 45, y: 20, angle: 0 },
        { level: 3, x: 45, y: 240, angle: 45 },
        { level: 2, x: 45, y: 440, angle: 45 },
    ];
</script>

<svg viewBox="0 0 120 600" class:mirror>
    <g stroke="var(--reef-pole)" stroke-width="12px" fill="none">
        <path
            d="m 60,0 v 125 a 24.142136,24.142136 112.5 0 1 -7.071068,17.07107 L 12.071068,182.92893 A 24.142136,24.142136 112.5 0 0 5,200 v 400"
        />
        <line x1="5" y1="355" x2="115" y2="245" />
        <line x1="5" y1="555" x2="115" y2="445" />
    </g>
    {#each coral_positions as { level, x, y, angle } (level)}
        <g transform="translate({x}, {y}) rotate({angle}, 15, 60)">
            <rect
                width="30"
                height="80"
                fill="var(--coral)"
                class:hidden={!current_scored[level - 2]}
            />
            <g class:hidden={!auto_scored[level - 2]}>
                <rect width="30" height="20" y="85" fill="var(--coral-auto)" />"
                <text
                    font-size="16pt"
                    font-weight="bold"
                    text-anchor="middle"
                    fill="black"
                    x="15"
                    y="103">A</text
                >
            </g>
        </g>
    {/each}
</svg>

<style>
    .mirror {
        transform: scaleX(-1);
    }

    .hidden {
        visibility: hidden;
    }
</style>
