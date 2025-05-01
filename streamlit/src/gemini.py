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
    output_theme_changed_base64: str
    output_theme_changed_supplement: str
    output_result_base64: str
    output_result_supplement: str


@dataclass
class LineDrawGenerationLifecycle:
    target_base64: str
    theme_base64: str
    theme_description: str
    user_request: str

    def __post_init__(self) -> None:
        root_dir = Path(__file__).resolve().parent.parent
        load_dotenv(root_dir / ".env", verbose=True)

        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash-exp-image-generation"
        )

    def change_theme(self, state: State) -> State:
        print("---Change Theme---")

        target_image = f"data:image/jpeg;base64,{self.target_base64}"
        theme_image = f"data:image/jpeg;base64,{self.theme_base64}"
        prompt = f"""
        target imageを次のように修正してください。
        - theme imageを参考にしてください
        - requestのように修正してください
        
        以下は与えられる入力についてです。
        ```
        - images
          1. The first image : theme image
          2. The second image : target image
        - theme description : {self.theme_description}
        - request : {self.user_request}
        ```
        """
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": theme_image},
                {"type": "image_url", "image_url": target_image},
            ]
        )
        output = self.llm.invoke(
            [message],
            generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
        )
        text, image = output.content

        output_theme_changed_supplement = text
        output_theme_changed_base64 = image["image_url"]["url"].split(",")[-1]

        return {
            "output_theme_changed_supplement": output_theme_changed_supplement,
            "output_theme_changed_base64": output_theme_changed_base64,
        }

    def line_draw(self, state: State) -> State:
        print("---Line Draw---")

        target_image = f"data:image/jpeg;base64,{state['output_theme_changed_base64']}"
        prompt = """
        次の画像をいかに注意して線画にしてください。
        - 輪郭線がはっきりとしていること
        - ぼやけている部分をはっきりさせること
        - 影や色をつけないこと。必ず白黒の線画にすること。
        - 画像の内容を変えないこと
        """
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": target_image},
            ]
        )
        output = self.llm.invoke(
            [message],
            generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
        )
        text, image = output.content

        output_result_supplement = text
        output_result_base64 = image["image_url"]["url"].split(",")[-1]

        return {
            "output_result_supplement": output_result_supplement,
            "output_result_base64": output_result_base64,
        }

    def run(self) -> dict[str, str]:
        builder = StateGraph(State)
        builder.add_node("change_theme", self.change_theme)
        builder.add_node("line_draw", self.line_draw)

        builder.add_edge(START, "change_theme")
        builder.add_edge("change_theme", "line_draw")
        builder.add_edge("line_draw", END)

        memory = MemorySaver()
        graph = builder.compile(checkpointer=memory)

        initial_input = {}
        thread = {"configurable": {"thread_id": str(int(time.time()))}}
        # Run the graph until the first interruption

        results = {}
        for event in graph.stream(initial_input, thread, stream_mode="updates"):
            if "change_theme" in event:
                print(
                    f"change_theme: {event['change_theme']['output_theme_changed_supplement']}"
                )
                results["theme_changed_base64"] = event["change_theme"][
                    "output_theme_changed_base64"
                ]
            elif "line_draw" in event:
                print(f"line_draw: {event['line_draw']['output_result_supplement']}")
                results["line_draw_base64"] = event["line_draw"]["output_result_base64"]
            print("\n")

        del graph

        return results
