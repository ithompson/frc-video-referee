<div class="match-card">
    <div class="card-header">Q3 Replay 1</div>
    <div class="match-score">
        <div class="match-score">
            <div class="red">273</div>
            <div class="divider">-</div>
            <div class="blue">109</div>
        </div>
    </div>
    <div class="team-lists">
        <ol class="red">
            <li>11932</li>
            <li>2623</li>
            <li>272</li>
        </ol>
        <ol class="blue">
            <li>142</li>
            <li>31332</li>
            <li>19382</li>
        </ol>
    </div>
</div>

<style>
    .match-card {
        border: 2px solid black;
        border-radius: 10px;
        overflow: clip;
        width: 140px;
        display: flex;
        flex-direction: column;
    }
    .card-header {
        width: 100%;
        text-align: center;
        background-color: var(--red-banner);
        color: var(--text-active-dark);
        font-weight: bold;
        padding-bottom: 0.2em;
        box-shadow: 0 1px 1px;
        z-index: 5;
    }
    .match-score {
        width: 100%;
        display: flex;
        justify-content: center;
        background-color: var(--red-banner);
        color: var(--text-active-dark);
        font-weight: bold;
        box-shadow: 0 1px 1px;
        z-index: 4;

        & .red,
        & .blue {
            width: 100%;
        }
        & .divider {
            width: 2em;
            text-align: center;
        }
        & .red {
            text-align: right;
        }
        & .blue {
            text-align: left;
        }
    }
    .team-lists {
        display: flex;
        & ol {
            flex: 1 1 0%;
        }
        & .red {
            background-color: var(--red-overlay-background);
        }
        & .blue {
            background-color: var(--blue-overlay-background);
        }
    }
    ol {
        list-style-type: none;
        padding: 0 10px;
        margin: 0;
    }
</style>
