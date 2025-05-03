import time
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class State(TypedDict):
    output_first_phase: str
    output_add_color: str
    output_second_phase: str


@dataclass
class LineDrawGenerationLifecycle:
    target_base64: str

    def __post_init__(self) -> None:
        root_dir = Path(__file__).resolve().parent.parent
        load_dotenv(root_dir / ".env", verbose=True)

        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash-exp-image-generation"
        )

    def first_phase(self, state: State) -> State:
        print("---1st Phase---")

        target_image = f"data:image/jpeg;base64,{self.target_base64}"
        message = HumanMessage(
            content=[
                {"type": "text", "text": "この画像を白黒の塗り絵にしてください"},
                {"type": "image_url", "image_url": target_image},
            ]
        )
        output = self.llm.invoke(
            [message],
            generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
        )
        _, image = output.content
        output_first_phase = image["image_url"]["url"].split(",")[-1]

        return {"output_first_phase": output_first_phase}

    def add_color(self, state: State) -> State:
        print("---Add Color---")

        target_image = f"data:image/jpeg;base64,{state['output_first_phase']}"
        message = HumanMessage(
            content=[
                {"type": "image_url", "image_url": target_image},
                {
                    "type": "text",
                    "text": "この画像に色鉛筆で書いたように色をつけてください",
                },
            ]
        )
        output = self.llm.invoke(
            [message],
            generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
        )
        _, image = output.content
        output_add_color = image["image_url"]["url"].split(",")[-1]

        return {"output_add_color": output_add_color}

    def run(self) -> dict[str, str]:
        builder = StateGraph(State)
        builder.add_node("first_phase", self.first_phase)
        builder.add_node("add_color", self.add_color)

        builder.add_edge(START, "first_phase")
        builder.add_edge("first_phase", "add_color")
        builder.add_edge("add_color", END)

        memory = MemorySaver()
        graph = builder.compile(checkpointer=memory)

        initial_input = {}
        thread = {"configurable": {"thread_id": str(int(time.time()))}}
        # Run the graph until the first interruption

        try:
            results = {}
            for event in graph.stream(initial_input, thread, stream_mode="updates"):
                if "first_phase" in event:
                    results["first_phase"] = event["first_phase"]["output_first_phase"]
                elif "add_color" in event:
                    results["add_color"] = event["add_color"]["output_add_color"]
        except Exception as e:
            raise GeminiException("Gemini 2.0 failed") from e
        del graph

        return results


class GeminiException(Exception):
    pass
