<div class="event-card">
    <div class="card-header">VAR Review</div>
    <div class="event-details">
        <div class="event-time">Teleop 1:23</div>
        <div class="event-note">Damaging contact</div>
        <div class="event-team red">Team 123</div>
    </div>
    <div class="event-controls">
        <button class="edit">Edit</button>
        <button class="delete">Delete</button>
    </div>
</div>

<style>
    .event-card {
        border: 2px solid black;
        border-radius: 10px;
        overflow: clip;
        display: flex;
        flex-direction: column;
        width: 160px;
    }
    .card-header {
        z-index: 3;
        width: 100%;
        text-align: center;
        background-color: var(--red-banner);
        color: var(--text-active-dark);
        font-weight: bold;
        padding-bottom: 0.2em;
        box-shadow: 0 1px 1px;
    }
    .event-details {
        background-color: var(--gray-500);
    }
    .match-score {
        display: flex;
        justify-content: center;
        background-color: var(--red-banner);
        color: var(--text-active-dark);
        font-weight: bold;

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
    .event-controls {
        box-shadow: 0 -1px 1px black;
        display: flex;
        & button {
            flex: 1 1 0%;
            text-align: center;
            height: 40px;
            box-shadow: none;
        }
    }
    .edit {
        font-size: 0;
        background: #a89c4c url("../assets/edit.svg") no-repeat center;
    }
    .delete {
        background: var(--red-600) url("../assets/delete_forever.svg") no-repeat
            center;
        font-size: 0;
    }
    .event-team.red {
        background-color: var(--red-overlay-background);
    }
    .event-team.blue {
        background-color: var(--blue-overlay-background);
    }
    .team-lists {
        display: flex;
    }
    ol {
        list-style-type: none;
        padding: 0 10px;
        margin: 0;
    }
</style>
