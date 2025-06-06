from fastapi import FastAPI, Query
from indra_ai import ASI  # Assuming indra_ai.py is in the same directory

app = FastAPI()
asi = ASI()

@app.get("/chat")
async def chat_endpoint(input: str = Query(..., alias="input")):
    return asi.chat(input)

@app.get("/roam_auto")
async def roam_auto_endpoint():
    return asi.perceive_agi()

@app.get("/simulate")
async def simulate_endpoint():
    perception_data = asi.perceive_agi()
    return asi.simulate_decision(perception_data)

@app.get("/latest_updates")
async def latest_updates_endpoint():
    return asi.latest_updates()
