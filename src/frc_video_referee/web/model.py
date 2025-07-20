from typing import Dict, List, Literal
from pydantic import BaseModel, TypeAdapter


class WebsocketEvent(BaseModel):
    """Base class for WebSocket events"""

    type: Literal["event"] = "event"
    """Type of the message, always 'event' for WebSocket events"""
    event_type: str
    """Type of the event, e.g. 'match_update', 'arena_state'"""
    data: dict
    """Data associated with the event, serialized as a dictionary"""


class WebsocketSubscribeRequest(BaseModel):
    """Request model for subscribing to WebSocket events"""

    type: Literal["subscribe"] = "subscribe"
    """Type of the message, always 'subscribe' for subscription requests"""
    event_types: List[str]
    """Type of the event to subscribe to, e.g. 'match_update', 'arena_state'"""
    request_id: int | None = None
    """Optional request ID for tracking the subscription request"""


class WebsocketUnsubscribeRequest(BaseModel):
    """Request model for unsubscribing from WebSocket events"""

    type: Literal["unsubscribe"] = "unsubscribe"
    """Type of the message, always 'unsubscribe' for unsubscription requests"""
    event_types: List[str]
    """Type of the event to unsubscribe from, e.g. 'match_update', 'arena_state'"""
    request_id: int | None = None
    """Optional request ID for tracking the unsubscription request"""


class WebsocketSubscribeResponse(BaseModel):
    """Response model for a subscription request"""

    type: Literal["subscribe"] = "subscribe"
    """Type of the message, always 'subscribe' for subscription responses"""
    initial_data: Dict[str, dict]
    """Data associated with the subscription, including current values for subscribed events"""
    request_id: int | None = None
    """Optional request ID for tracking the subscription response"""


class WebsocketUnsubscribeResponse(BaseModel):
    """Response model for an unsubscription request"""

    type: Literal["unsubscribe"] = "unsubscribe"
    """Type of the message, always 'unsubscribe' for unsubscription responses"""
    unsubscribed_event_types: List[str]
    """List of event types that were successfully unsubscribed from"""
    request_id: int | None = None
    """Optional request ID for tracking the unsubscription response"""


InboundWebsocketMessage = TypeAdapter(
    WebsocketSubscribeRequest | WebsocketUnsubscribeRequest
)
OutboundWebsocketMessage = TypeAdapter(
    WebsocketEvent | WebsocketSubscribeResponse | WebsocketUnsubscribeResponse
)
