import { MatchEventType } from "./model";

export function getEventTypeString(eventType: MatchEventType): string {
    switch (eventType) {
        case MatchEventType.AUTO_SCORING:
            return "Auto Score";
        case MatchEventType.ENDGAME_SCORING:
            return "Final Score";
        case MatchEventType.VAR_REVIEW:
            return "VAR Review";
        case MatchEventType.HR_REVIEW:
            return "HR Review";
        case MatchEventType.ROBOT_DISCONNECT:
            return "Robot Drop";
        default:
            return "Unknown";
    }
}

export function getEventTypeColor(eventType: MatchEventType): string {
    switch (eventType) {
        case MatchEventType.AUTO_SCORING:
            return "var(--green-200)";
        case MatchEventType.ENDGAME_SCORING:
            return "var(--green-200)";
        case MatchEventType.VAR_REVIEW:
            return "var(--blue-200)";
        case MatchEventType.HR_REVIEW:
            return "var(--auto-inactive)";
        case MatchEventType.ROBOT_DISCONNECT:
            return "var(--red-200)";
        default:
            return "var(--red-200)";
    }
}