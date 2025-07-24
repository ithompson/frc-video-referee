<script lang="ts">
</script>

{#snippet timelinePoint(
    time: number,
    label: string,
    color: string = "var(--gray-500)",
)}
    <div class="point-wrap">
        <div class="point-label" style="background-color: {color};">
            {label}
        </div>
    </div>
{/snippet}

<div class="timeline">
    <div class="timeline-points">
        {@render timelinePoint(0, "0", "var(--red-200)")}
        {@render timelinePoint(100, "1", "var(--blue-200)")}
        {@render timelinePoint(200, "2", "var(--green-200)")}
    </div>
    <div class="slider-container">
        <div class="slider-period auto" style="left: 0%; width: 20%;"></div>
        <div class="slider-period teleop" style="left: 40%; width: 40%;"></div>
        <input type="range" min="0" max="10000" value="5000" class="slider" />
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
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }

    .point-wrap {
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
