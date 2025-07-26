import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import WebSocketClient from './lib/wsclient.svelte'
import { HyperdeckTransportMode, WebsocketEventType, type ControllerStatus, type HyperdeckStatus, type MatchTime, type RealtimeScore } from './lib/model'
import { server_state } from './lib/server_state.svelte'

const websocketAddress = import.meta.env.DEV ? 'rho.local:8000' : window.location.host;

const ws = new WebSocketClient(websocketAddress);
ws.subscribe(WebsocketEventType.ControllerStatus, (data) => {
  server_state.controller_status = data as ControllerStatus;
});
ws.subscribe(WebsocketEventType.CurrentMatchData, (data) => {
  console.log('Current match data received:', data);
});
ws.subscribe(WebsocketEventType.CurrentMatchTime, (data) => {
  server_state.match_time = data as MatchTime;
});
ws.subscribe(WebsocketEventType.RealtimeScore, (data) => {
  server_state.realtime_score = data as RealtimeScore;
});
ws.subscribe(WebsocketEventType.MatchList, (data) => {
  console.log('Match list updated:', data);
});
ws.subscribe(WebsocketEventType.ArenaConnection, (data) => {
  server_state.arena_connected = data.connected;
});
ws.subscribe(WebsocketEventType.HyperdeckConnection, (data) => {
  server_state.hyperdeck_connected = data.connected;
});
ws.subscribe(WebsocketEventType.HyperdeckStatus, (data) => {
  server_state.hyperdeck_status = data as HyperdeckStatus;
});

ws.enable();

const app = mount(App, {
  target: document.getElementById('app')!,
  props: {
    ws: ws,
  },
})


export default app
