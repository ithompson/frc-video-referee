<script lang="ts">
    import { getEventTypeColor } from "../lib/events";
    import type { MatchEvent, MatchTiming } from "../lib/model";

    interface EventWithIdx {
        event_idx: number;
        event: MatchEvent;
    }

    interface Props {
        events: EventWithIdx[];
        warpToEvent?: (event: MatchEvent) => void;
        warpToTime?: (time: number) => void;
        currentTime: number;
        match_timing: MatchTiming;
    }

    let { events, warpToEvent, warpToTime, currentTime, match_timing }: Props =
        $props();

    const num_ticks = 100000;
    let scoring_capture_sec = 5;

    const auto_start_time = match_timing.warmup_duration_sec;
    const auto_end_time = auto_start_time + match_timing.auto_duration_sec;
    const teleop_start_time = auto_end_time + match_timing.pause_duration_sec;
    const teleop_end_time =
        teleop_start_time + match_timing.teleop_duration_sec;
    const total_recording_duration = teleop_end_time + scoring_capture_sec;

    let ticks_per_second = num_ticks / total_recording_duration;

    let periods = [
        {
            name: "auto",
            start: auto_start_time * ticks_per_second,
            end: auto_end_time * ticks_per_second,
        },
        {
            name: "teleop",
            start: teleop_start_time * ticks_per_second,
            end: teleop_end_time * ticks_per_second,
        },
    ];

    let timeline_pos = $derived(currentTime * ticks_per_second);

    function handlePointClick(mouseEvent: MouseEvent) {
        const target = mouseEvent.currentTarget as HTMLButtonElement;
        const event_idx = parseInt(target.dataset.eventIdx!, 10);
        const event = events.find((e) => e.event_idx === event_idx)!.event;

        warpToEvent?.(event);
        timeline_pos = event.time * ticks_per_second;
    }

    function handleSliderChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const timeInTicks = parseInt(target.value, 10);
        const timeInSeconds = timeInTicks / ticks_per_second;

        warpToTime?.(timeInSeconds);
    }
</script>

{#snippet timelinePoint(event: EventWithIdx)}
    <button
        class="point-wrap"
        style="left: calc(((100% - 20px) * {(event.event.time *
            ticks_per_second) /
            num_ticks}));"
        onclick={handlePointClick}
        data-event-idx={event.event_idx}
    >
        <div
            class="point-label"
            style="background-color: {getEventTypeColor(
                event.event.event_type,
            )};"
        >
            {event.event_idx}
        </div>
    </button>
{/snippet}

{#snippet timelinePeriod(name: string, start: number, end: number)}
    <div
        class="slider-period {name}"
        style="left: calc((100% - 20px) * {start /
            num_ticks} + 10px); width: calc((100% - 20px) * {(end - start) /
            num_ticks});"
    ></div>
{/snippet}

<div class="timeline">
    <div class="timeline-points">
        {#each events as event}
            {@render timelinePoint(event)}
        {/each}
    </div>
    <div class="slider-container">
        {#each periods as period}
            {@render timelinePeriod(period.name, period.start, period.end)}
        {/each}
        <input
            type="range"
            min="0"
            max={num_ticks - 1}
            class="slider"
            bind:value={timeline_pos}
            oninput={handleSliderChange}
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
