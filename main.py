# main.py
# -----------------------------------------------------
# 
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from prompts import GENERATOR_PROMPT, REFLECTION_PROMPT
from tools import execute_python_code

# 1. Define the State (The memory of our agent loop)
class AgentState(TypedDict):
    request: str
    code: str
    error: str
    iterations: int

# Initialize your local model
llm = OllamaLLM(model="qwen2.5-coder:7b")
MAX_ITERATIONS = 3

# 2. Define the Nodes
def generate_code_node(state: AgentState):
    print("🧠 Agent: Thinking and writing code...")
    prompt = GENERATOR_PROMPT.format(user_request=state['request'])
    code = llm.invoke(prompt)
    return {"code": code, "iterations": state.get("iterations", 0) + 1}

def execute_node(state: AgentState):
    print("⚙️ System: Executing code...")
    result = execute_python_code(state['code'])
    
    if result["status"] == "success":
        print(f"✅ Success! Output:\n{result['output']}")
        return {"error": None} # Clears error, triggering END
    else:
        print(f"❌ Error Caught! Passing back to agent...")
        return {"error": result["output"]}

def reflect_node(state: AgentState):
    print("🔍 Agent: Analyzing error and rewriting code...")
    prompt = REFLECTION_PROMPT.format(code=state['code'], error=state['error'])
    new_code = llm.invoke(prompt)
    return {"code": new_code, "iterations": state['iterations'] + 1}

# 3. Define the Routing Logic
def route_execution(state: AgentState):
    if state["error"] is None:
        return END # Code worked, finish the loop
    elif state["iterations"] >= MAX_ITERATIONS:
        print("⚠️ Reached max loops. Stopping to prevent infinite loop.")
        return END
    else:
        return "reflect" # Code failed, send to reflection

# 4. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("generate", generate_code_node)
workflow.add_node("execute", execute_node)
workflow.add_node("reflect", reflect_node)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "execute")
workflow.add_conditional_edges("execute", route_execution)
workflow.add_edge("reflect", "execute")

# Compile the engine
agent_app = workflow.compile()

# ==========================================
# Run the Agent!
# ==========================================
if __name__ == "__main__":
    print("\n🚀 Welcome to the Self-Correcting Data Agent 🚀")
    user_input = input("What would you like me to analyze from 'E-Commerce Dashboard dataset.xlsx'?\n> ")
    
    initial_state = {"request": user_input, "code": "", "error": "", "iterations": 0}
    agent_app.invoke(initial_state)