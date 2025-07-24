<div class="event-card">
    <div class="card-header">
        <span class="event-idx">2</span>
        <span class="event-label">VAR Review</span>
        <span class="event-spacer"></span>
    </div>
    <div class="event-details">
        <div class="event-section">Teleop 1:23</div>
        <div class="event-section">Damaging contact</div>
        <div class="event-section alliance red">Team 123</div>
    </div>
</div>

<style>
    .event-card {
        box-sizing: border-box;
        border: 4px solid var(--gray-600);
        border-radius: 10px;
        overflow: clip;
        background-color: var(--gray-700);
        display: flex;
        flex-direction: column;
        width: 160px;
        box-shadow: 0 0 8px black;
        margin: 0 10px;
    }
    .card-header {
        background-color: var(--gray-600);
        color: var(--text-active);
        font-weight: bold;
        padding: 2px 0.5em 4px 0.5em;
        box-shadow: 0 0px 8px black;

        display: flex;
        flex-direction: row;
        justify-content: space-between;

        & .event-label {
            color: var(--text-active-dark);
            background-color: var(--green-200);
            border-radius: 16px;
            padding: 0 0.5em;
            min-width: 6em;
        }
    }

    .event-details {
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding: 5px 0;
        align-items: center;
    }

    .event-section {
        background-color: var(--gray-600);
        border-radius: 4px;
        width: 90%;
        padding: 0.2em;
        box-shadow: 0 0 8px black;
    }
    .event-section.alliance {
        background-color: var(--alliance-overlay-background);
    }
</style>
