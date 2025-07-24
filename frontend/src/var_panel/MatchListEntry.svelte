<div class="match-card">
    <div class="card-header">Q3 Replay 1</div>
    <div class="match-details">
        <div class="match-section alliance red">273 - 109</div>
        <div class="match-section team-lists">
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
</div>

<style>
    .match-card {
        box-sizing: border-box;
        border: 4px solid var(--gray-600);
        border-radius: 10px;
        overflow: clip;
        background-color: var(--gray-700);
        display: flex;
        flex-direction: column;
        width: 140px;
        box-shadow: 0 0 8px black;
        margin: 0 10px;
    }
    .card-header {
        background-color: var(--gray-600);
        color: var(--text-active);
        font-weight: bold;
        padding: 2px 0.5em 4px 0.5em;
        box-shadow: 0 0px 8px black;
    }

    .match-details {
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding: 5px 0;
        align-items: center;
    }

    .match-section {
        box-sizing: border-box;
        background-color: var(--gray-600);
        border-radius: 8px;
        overflow: clip;
        width: 90%;
        padding: 0.2em;
        box-shadow: 0 0 8px black;
    }
    .match-section.alliance {
        background-color: var(--alliance-overlay-background);
    }

    .team-lists {
        display: flex;
        padding: 0;
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
        padding: 0;
        margin: 0;
    }
</style>
