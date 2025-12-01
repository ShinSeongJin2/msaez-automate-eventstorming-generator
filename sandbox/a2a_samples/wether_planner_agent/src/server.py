import re
import json
import datetime as dt
from typing import Dict, Any, List, Optional

import requests
from python_a2a import (
    A2AServer, agent, skill, run_server,
    TaskStatus, TaskState
)

@agent(
    name="Travel Planner",
    description="도시/일자 기반 날씨를 확인하고 간단한 여행 일정을 제안하는 A2A 에이전트",
    version="1.1.0",
    tags=["travel", "weather", "planning"],
)
class TravelAgent(A2AServer):

    @skill(
        name="get_weather",
        description="도시명/위경도와 날짜 범위를 받아 일별 일기예보를 조회합니다.",
        tags=["weather"],
    )
    def get_weather(self, lat: float, lon: float, days: int = 3) -> Dict[str, Any]:
        # Open-Meteo (무료, 키 불필요)
        # 일별 최고/최저기온과 강수확률
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            "&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("daily", {})

        # days 만큼 자르기
        result = []
        for i in range(min(days, len(data.get("time", [])))):
            result.append({
                "date": data["time"][i],
                "tmax": data["temperature_2m_max"][i],
                "tmin": data["temperature_2m_min"][i],
                "pop": data["precipitation_probability_max"][i],
            })
        return {"days": result}

    @skill(
        name="plan_itinerary",
        description="날씨 요약을 바탕으로 실외/실내 위주로 일정을 구성합니다.",
        tags=["planning", "itinerary"],
    )
    def plan_itinerary(self, city: str, weather_days: List[Dict[str, Any]]) -> Dict[str, Any]:
        plan = []
        for d in weather_days:
            is_rainy = (d["pop"] or 0) >= 50
            activities = ["미술관", "카페 탐방", "현지 음식 투어"] if is_rainy else ["도시 투어", "공원 산책", "리버 크루즈"]
            plan.append({
                "date": d["date"],
                "theme": "실내 위주" if is_rainy else "실외 위주",
                "activities": activities
            })
        return {"city": city, "itinerary": plan}

    # 도시명 → 위경도 간단 매핑(데모용)
    CITY2LL = {
        "paris": (48.8566, 2.3522),
        "seoul": (37.5665, 126.9780),
        "new york": (40.7128, -74.0060),
        "tokyo": (35.6762, 139.6503),
    }

    def _parse(self, text: str) -> Optional[Dict[str, Any]]:
        # 예) "파리 3일 일정", "paris 2 days plan", "도쿄 내일 포함 2일"
        t = text.lower()
        city = None
        for c in self.CITY2LL:
            if c in t:
                city = c
                break
        if not city:
            return None
        m = re.search(r"(\d+)\s*day|(\d+)\s*일", t)
        days = int(m.group(1) or m.group(2)) if m else 3
        return {"city": city, "days": days}

    # 최소 구현: 자유 텍스트를 받아 스킬 파이프라인 실행
    def handle_task(self, task):
        msg = (task.message or {})
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)

        parsed = self._parse(text)
        if not parsed:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent",
                         "content": {"type": "text", "text": "예) 'paris 3 days plan' 처럼 도시/기간을 알려주세요."}}
            )
            return task

        city = parsed["city"]
        days = parsed["days"]
        lat, lon = self.CITY2LL[city]

        weather = self.get_weather(lat, lon, days=days)
        plan = self.plan_itinerary(city, weather["days"])

        # 구조화(JSON) + 사람이 읽을 텍스트를 함께 artifact로 반환
        text_out = [f"[{city.title()}] {days}일 일정 제안"]
        for d in plan["itinerary"]:
            text_out.append(f"- {d['date']} | {d['theme']} | 추천: {', '.join(d['activities'])}")

        task.artifacts = [{
            "parts": [
                {"type": "text", "text": "\n".join(text_out)},
                {"type": "application/json", "text": json.dumps(plan, ensure_ascii=False)},
            ]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task

if __name__ == "__main__":
    agent = TravelAgent(url="http://0.0.0.0:6000")
    run_server(agent, host="0.0.0.0", port=6000)