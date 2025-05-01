import base64
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict


def encode_image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        # 画像をバイナリとして読み込み、Base64 にエンコード
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


root_dir = Path(__file__).resolve().parent.parent
load_dotenv(root_dir / ".env", verbose=True)


llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-exp-image-generation")


class State(TypedDict):
    input_1: str
    output_1: str
    user_feedback: str
    output_2: str


def step_1(state: State):
    print("---Step 1---")
    img_str = encode_image_to_base64(root_dir / "src" / "sample.jpeg")
    img = f"data:image/jpeg;base64,{img_str}"
    message = HumanMessage(
        content=[
            {"type": "text", "text": "この画像はなんですか？簡潔に説明してください。"},
            {"type": "image_url", "image_url": img},
        ]
    )
    output_1 = llm.invoke([message])
    print(output_1)
    return {"output_1": output_1.content}


def human_feedback(state: State):
    print("---human_feedback---")
    message = """この画像にどのような変更を加えますか？"""
    feedback = interrupt(message)
    return {"user_feedback": feedback}


def step_3(state: State):
    print("---Step 3---")
    prompt = f"""
    この画像は{state["output_1"]}
    以下のように変更してください。
    {state["user_feedback"]}
    """
    img_str = encode_image_to_base64(root_dir / "src" / "sample.jpeg")
    img = f"data:image/jpeg;base64,{img_str}"
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": img},
        ]
    )
    output_2 = llm.invoke(
        [message],
        generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
    )
    image_base64 = output_2.content[1]["image_url"]["url"].split(",")[-1]
    meow_str = output_2.content[0]
    print(len(output_2.content), len(image_base64), len(meow_str))

    # 画像をデコードしてファイルに保存
    output_image_path = root_dir / "src" / "output_image.jpeg"
    with open(output_image_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_base64))
    return {"output_2": meow_str}


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
# Start -> step_1 -> human_feedback -> step_3 -> End
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

# Set up memory
memory = MemorySaver()

# Add
graph = builder.compile(checkpointer=memory)

# Input
initial_input = {"input_1": "hello world"}

# Thread (TODO: thead_idとは何か確認する)
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="updates"):
    print(event)
    print("\n")


# Continue the graph execution
for event in graph.stream(
    Command(resume="鬼滅の刃のようなテーマで"),
    thread,
    stream_mode="updates",
):
    print(event)
    print("\n")
