# PolyMarket MCP Server
## Skills
### get_events
parameters:
{
    "active_only":bool
    "limit":int
    "offset":int
}

### get_markets
parameters:
{
    "active_only":bool
    "limit":int
    "offset":int
}

### get_event_by_id
parameters:
{
    "event_id":str
}


### get_market_by_id
parameters:
{
    "market_id":str
}


## Response
{
    "event_id/market_id":str,
    "title":str,
    "description":str,
    "start_date":str,
    "end_date":str,
    "liquidity":float,
    "volume":float,
    "markets":int,
    "tags":list[str]
}