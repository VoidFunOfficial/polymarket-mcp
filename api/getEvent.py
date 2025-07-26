import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union, overload
from datetime import datetime
import json
#标签
@dataclass
class Tag:
    id: str #标签id
    publishedAt: str #发布时间
    createdAt: str #创建时间
    updatedAt: str #更新时间
    label: str #标签名称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tag':
        return cls(
            id=data.get('id'),
            publishedAt=data.get('publishedAt'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt'),
            label=data.get('label'),
        )

#压铸市场(对事件的具体压铸)
@dataclass
class Market:
    id: str #市场id
    question: str #压铸问题
    endDate: str #结束时间
    liquidity: str #流动性
    startDate: str #开始时间
    description: str #描述
    outcomes: List[str] #压铸选项
    outcomePrices: List[str] #压铸选项价格
    volume: str #交易量
    closed: bool #是否结束
    createdAt: str #创建时间
    volumeNum: float #交易量
    liquidityNum: float #流动性
    competitive: float #竞争度
    volume24hr: float #24小时交易量
    volume1wk: float #1周交易量
    volume1mo: float #1月交易量
    volume1yr: float #1年交易量
    liquidityClob: float #流动性clob

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Market':
        outcomes = data.get('outcomes', [])
        if isinstance(outcomes, str):
            try:
                outcomes = json.loads(outcomes)
            except:
                outcomes = []

        outcomePrices = data.get('outcomePrices', [])
        if isinstance(outcomePrices, str):
            try:
                outcomePrices = json.loads(outcomePrices)
            except:
                outcomePrices = []

        return cls(
            id=data.get('id'),
            question=data.get('question'),
            endDate=data.get('endDate'),
            liquidity=data.get('liquidity'),
            startDate=data.get('startDate'),
            description=data.get('description'),
            outcomes=outcomes,
            outcomePrices=outcomePrices,
            volume=data.get('volume'),
            closed=data.get('closed'),
            createdAt=data.get('createdAt'),
            volumeNum=data.get('volumeNum', 0.0),
            liquidityNum=data.get('liquidityNum', 0.0),
            competitive=data.get('competitive', 0.0),
            volume24hr=data.get('volume24hr', 0.0), #24小时交易量
            volume1wk=data.get('volume1wk', 0.0), #1周交易量
            volume1mo=data.get('volume1mo', 0.0), #1月交易量
            volume1yr=data.get('volume1yr', 0.0), #1年交易量
            liquidityClob=data.get('liquidityClob', 0.0) #流动性clob
        )

@dataclass
class Event:
    id: str #事件id
    ticker: str #事件代码
    title: str #事件标题
    description: str #事件描述
    startDate: str #事件开始时间
    creationDate: str #事件创建时间
    endDate: str #事件结束时间
    closed: bool #是否结束
    liquidity: float #流动性
    event_total_volume: float #总事件交易量(包含各个压铸选项)
    createdAt: str #创建时间
    updatedAt: str #更新时间
    competitive: float 
    event_total_volume24hr: float #总事件24小时交易量
    event_total_volume1wk: float #总事件1周交易量
    event_total_volume1mo: float #总事件1月交易量
    event_total_volume1yr: float #总事件1年交易量
    liquidityClob: float #流动性clob
    markets: List[Market] #压铸市场列表
    tags: List[Tag] #标签列表

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        return cls(
            id=data.get('id'),
            ticker=data.get('ticker'),
            title=data.get('title'),
            description=data.get('description'),
            startDate=data.get('startDate'),
            creationDate=data.get('creationDate'),
            endDate=data.get('endDate'),
            closed=data.get('closed'),
            liquidity=data.get('liquidity', 0.0),
            event_total_volume=data.get('volume', 0.0),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt'),
            competitive=data.get('competitive', 0.0),
            event_total_volume24hr=data.get('volume24hr', 0.0),
            event_total_volume1wk=data.get('volume1wk', 0.0),
            event_total_volume1mo=data.get('volume1mo', 0.0),
            event_total_volume1yr=data.get('volume1yr', 0.0),
            liquidityClob=data.get('liquidityClob', 0.0),
            markets=[Market.from_dict(m) for m in data.get('markets', [])],
            tags=[Tag.from_dict(t) for t in data.get('tags', [])],
        )

class PolymarketAPI:
    BASE_URL = "https://gamma-api.polymarket.com"
    
    def get_events(self, active_only: bool = True,limit:int = 10,offset:int = 0) -> List[Event]:
        """
        获取Polymarket事件列表
        
        Args:
            active_only: 是否只返回活跃事件
        
        Returns:
            事件列表
        """
        url = f"{self.BASE_URL}/events"
        params = {}
        if active_only:
            params["closed"] = "False"
            params["limit"] = limit
            params["offset"] = offset
        
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            events_data = response.json()
            return [Event.from_dict(event) for event in events_data]
        else:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 响应: {response.text}")
    def get_markets(self,active_only:bool=True,limit:int=10,offset:int=0)->List[Market]:
        """
        获取市场列表
        """
        url = f"{self.BASE_URL}/markets"
        params = {}
        if active_only:
            params["closed"] = "False"
            params["limit"] = limit
            params["offset"] = offset
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            markets_data = response.json()
            return [Market.from_dict(market) for market in markets_data]
        else:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 响应: {response.text}")
    def get_event_by_id(self, event_id: str) -> Event:
        """
        通过ID获取特定事件
        
        Args:
            event_id: 事件ID
        
        Returns:
            事件对象
        """
        url = f"{self.BASE_URL}/events?id={event_id}"
        print(url)
        response = requests.request("GET", url)
        if response.status_code == 200:
            event_data = response.json()
            return Event.from_dict(event_data[0])
        else:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 响应: {response.text}")
        
    def get_market_by_id(self, market_id: str) -> Market:
        """
        通过ID获取特定市场
        """
        url = f"{self.BASE_URL}/markets?id={market_id}"
        response = requests.request("GET", url)
        if response.status_code == 200:
            market_data = response.json()
            return Market.from_dict(market_data[0])
        else:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 响应: {response.text}")
    def get_llm_analysis_market_info(self,limit:int=10,offset:int=0)->str:
        """
        获取市场信息
        """
        markets = self.get_markets(active_only=True,limit=limit,offset=offset)
        info={}
        for market in markets:
            info[market.id]={
                "market_info":to_llm_friendly_format(market,details=False)
            }   
        return info
@overload
def to_llm_friendly_format(event: Event) -> str:
    ...

@overload
def to_llm_friendly_format(market: Market) -> str:
    ...
@overload
def to_llm_friendly_format(events: List[Event]) -> str:
    ...
@overload
def to_llm_friendly_format(markets: List[Market]) -> str:
    ...
def to_llm_friendly_format(obj: Union[Event, Market],details:bool=True) -> str:

    """
    将对象转换为LLM友好的格式
    
    Args:
        obj: Event或Market对象
        
    Returns:
        格式化的字符串
    """
    if isinstance(obj, Event):
        if details:
            return {
                "event_id":obj.id,
                "title":obj.title,
                "description":obj.description,
                "start_date":obj.startDate,
                "end_date":obj.endDate,
                "liquidity":obj.liquidity,
                "volume":obj.event_total_volume,
                "markets":len(obj.markets),
                "tags":[tag.label for tag in obj.tags]
            }
        else:
            return {
                "event_id":obj.id,
                "title":obj.title,
                "description":obj.description,
                "start_date":obj.startDate,
                "end_date":obj.endDate,
                "markets":len(obj.markets),
                "tags":[tag.label for tag in obj.tags]
            }
    elif isinstance(obj, Market):
        if details:
            return {
                "market_id":obj.id,
                "question":obj.question,
                "end_date":obj.endDate,
                "start_date":obj.startDate,
                "description":obj.description,
                "outcomes":obj.outcomes,
                "market_price_probability":obj.outcomePrices,
                "volume":obj.volume,
                "closed":obj.closed,
                "created_at":obj.createdAt,
                "volume_num":obj.volumeNum,
                "liquidity_num":obj.liquidityNum,
                "competitive":obj.competitive,
                "24hr_volume":obj.volume24hr,
                "1wk_volume":obj.volume1wk,
                "1mo_volume":obj.volume1mo,
                "1yr_volume":obj.volume1yr,
                "liquidity_clob":obj.liquidityClob
            }
        else:
            return {
                "market_id":obj.id,
                "question":obj.question,
                "end_date":obj.endDate,
                "start_date":obj.startDate,
                "description":obj.description,
                "you_gamble_on":obj.outcomes,
                "price_probability":obj.outcomePrices
            }
    elif isinstance(obj, list):
        return [to_llm_friendly_format(item) for item in obj]
    else:
        raise TypeError("参数必须是Event或Market类型")
if __name__ == "__main__":
    api = PolymarketAPI()
    
    # 获取所有活跃事件
    events = api.get_events(active_only=True,limit=10,offset=0)
    print(to_llm_friendly_format(events))
    
    # # 打印第一个事件的基本信息
    # if events:
    #     event = events[0]
    #     print(f"事件ID: {event.id}") 
    #     print(f"标题: {event.title}")
    #     print(f"描述: {event.description[:100]}...")
    #     print(f"开始日期: {event.startDate}")
    #     print(f"结束日期: {event.endDate}")
    #     print(f"流动性: {event.liquidity}")
    #     print(f"交易量: {event.event_total_volume}")
    #     print(f"市场数量: {len(event.markets)}")
    #     print(f"标签: {[tag.label for tag in event.tags]}")
    # eventTest = api.get_event_by_id("14371")
    # marketTest = api.get_market_by_id("512812")
    # print(to_llm_friendly_format(eventTest))
    # print(to_llm_friendly_format(marketTest))
    # print(api.get_llm_analysis_market_info())