import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import { startWebsocket } from './lib/wsclient'
import { WebsocketEventType } from './lib/model'

const app = mount(App, {
  target: document.getElementById('app')!,
})

startWebsocket('localhost:8000', [
  WebsocketEventType.CurrentMatchTime,
  WebsocketEventType.RealtimeScore,
  WebsocketEventType.ArenaConnection,
  WebsocketEventType.HyperdeckConnection
])

export default app
