<script lang="ts">
    import { getEventTypeColor } from "../lib/events";
    import type { MatchEvent } from "../lib/model";

    interface EventWithIdx {
        event_idx: number;
        event: MatchEvent;
    }

    interface Props {
        events: EventWithIdx[];
    }

    let { events }: Props = $props();

    let fps = 59.94;
    let auto_duration_sec = 15;
    let pause_duration_sec = 3;
    let teleop_duration_sec = 135;
    let scoring_capture_sec = 5;

    let auto_start_time = 0;
    let auto_end_time = auto_duration_sec;
    let teleop_start_time = auto_end_time + pause_duration_sec;
    let teleop_end_time = teleop_start_time + teleop_duration_sec;
    let total_recording_duration = teleop_end_time + scoring_capture_sec;

    let total_time = total_recording_duration * fps; // Total time in frames for the clip
    let event_points = $derived(
        events.map((event) => ({
            label: String(event.event_idx),
            time: event.event.time * fps,
            color: getEventTypeColor(event.event.event_type),
        })),
    );

    let periods = [
        {
            name: "auto",
            start: auto_start_time * fps,
            end: auto_end_time * fps,
        },
        {
            name: "teleop",
            start: teleop_start_time * fps,
            end: teleop_end_time * fps,
        },
    ];

    let timeline_pos = $state(total_time / 2);

    function handlePointClick(event: MouseEvent) {
        const target = event.currentTarget as HTMLButtonElement;
        timeline_pos = parseInt(target.dataset.time!, 10);
    }
</script>

{#snippet timelinePoint(
    time: number,
    label: string,
    color: string = "var(--gray-500)",
)}
    <button
        class="point-wrap"
        style="left: calc(((100% - 20px) * {time / total_time}));"
        onclick={handlePointClick}
        data-time={time}
    >
        <div class="point-label" style="background-color: {color};">
            {label}
        </div>
    </button>
{/snippet}

{#snippet timelinePeriod(name: string, start: number, end: number)}
    <div
        class="slider-period {name}"
        style="left: calc((100% - 20px) * {start /
            total_time} + 10px); width: calc((100% - 20px) * {(end - start) /
            total_time});"
    ></div>
{/snippet}

<div class="timeline">
    <div class="timeline-points">
        {#each event_points as point}
            {@render timelinePoint(point.time, point.label, point.color)}
        {/each}
    </div>
    <div class="slider-container">
        {#each periods as period}
            {@render timelinePeriod(period.name, period.start, period.end)}
        {/each}
        <input
            type="range"
            min="0"
            max={total_time - 1}
            class="slider"
            bind:value={timeline_pos}
        />
    </div>
</div>

<style lang="scss">
    .timeline {
        box-sizing: border-box;
        --slider-height: 30px;
    }

    .timeline-points {
        height: 30px;
        width: 100%;
        position: relative;
    }

    .point-wrap {
        position: absolute;
        background: none;
        top: 0;
        filter: drop-shadow(-1px 6px 3px rgba(0, 0, 0, 0.5));
        z-index: 2;
    }
    .point-label {
        box-sizing: border-box;
        color: var(--text-active-dark);
        background-color: var(--gray-500);
        font-weight: bold;
        height: 30px;
        width: 20px;
        clip-path: polygon(0% 0%, 100% 0%, 100% 80%, 50% 100%, 0% 80%);
    }

    .slider-container {
        position: relative;
        height: var(--slider-height);
        background: var(--gray-600);
        border-radius: 8px;
        overflow: clip;
        box-shadow: 0 0 10px black;

        & .slider-period {
            position: absolute;
            top: 0;
            bottom: 0;

            &.auto {
                background-color: var(--auto-inactive);
            }
            &.teleop {
                background-color: var(--green-200);
            }
        }
    }

    @mixin thumb {
        box-sizing: border-box;
        height: var(--slider-height);
        width: 20px;
        border-radius: 3px;
        border: 2px solid var(--gray-500);
        background: #ffffff;
        cursor: pointer;
    }
    @mixin track {
        width: 100%;
        height: var(--slider-height);
        cursor: pointer;
        background: transparent;
    }

    input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        background: transparent;
        height: var(--slider-height);
        margin: 0;
        position: relative;
        z-index: 1;

        /* Special styling for WebKit/Blink */
        &::-webkit-slider-thumb {
            @include thumb;
            -webkit-appearance: none;
            //margin-top: -14px; /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
        }

        /* All the same stuff for Firefox */
        &::-moz-range-thumb {
            @include thumb;
        }

        /* All the same stuff for IE */
        &::-ms-thumb {
            @include thumb;
        }

        &::-webkit-slider-runnable-track {
            @include track;
        }
        &::-moz-range-track {
            @include track;
        }
        &::-ms-track {
            @include track;
            background: transparent; /* IE requires a transparent background for the track */
            border-color: transparent; /* IE requires a transparent border for the track */
            color: transparent; /* IE requires a transparent color for the track */
        }
    }
</style>
