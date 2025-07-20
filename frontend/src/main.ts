import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import { startWebsocket } from './lib/wsclient'
import { WebsocketEventType } from './lib/model'

const websocketAddress = import.meta.env.DEV ? 'localhost:8000' : window.location.host

const ws = startWebsocket(websocketAddress, [
  WebsocketEventType.CurrentMatchTime,
  WebsocketEventType.RealtimeScore,
  WebsocketEventType.ArenaConnection,
  WebsocketEventType.HyperdeckConnection
])

const app = mount(App, {
  target: document.getElementById('app')!,
})


export default app
