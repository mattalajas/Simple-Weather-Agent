from types import SimpleNamespace

from src.agent import WeatherAgent


class FakeCompletions:
    def __init__(self) -> None:
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            tool_call = SimpleNamespace(
                id="call_1",
                function=SimpleNamespace(
                    name="get_forecast_for_location",
                    arguments='{"location":"Seattle","days":2}',
                ),
                model_dump=lambda: {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "get_forecast_for_location",
                        "arguments": '{"location":"Seattle","days":2}',
                    },
                },
            )
            msg = SimpleNamespace(content="", tool_calls=[tool_call])
            return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

        msg = SimpleNamespace(content="Forecast response", tool_calls=None)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])


class FakeClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_agent_completes_tool_flow(monkeypatch):
    monkeypatch.setattr(
        "src.agent.get_forecast_for_location",
        lambda location, days: {"location": {"name": location}, "forecast": {"days": days}},
    )
    agent = WeatherAgent(client=FakeClient(), model="test-model", temperature=0.0)
    result = agent.ask("What's the weather?")
    assert "Forecast response" in result
