# Required Cheesy Arena changes

These changes are required to Cheesy Arena to support all VAR server features:
1. A websocket with notifiers for:
   * RealtimeScore (Detailed scoring status)
   * MatchTime (timestamping within matches)
   * MatchLoad (match IDs and lineups)
   * ArenaStatus (match ready indication)
2. Websocket operation to signal VAR scoring done
3. List in RealtimeScore of field-requested VAR review moments
4. Button on HR panel to add to the VAR review list (scoring panels too?)