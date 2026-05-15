from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Enable CORS (important for UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Foundry Endpoint
endpoint = "https://automated-approach-resource.services.ai.azure.com/api/projects/automated-approach"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

my_agent = "Nexus-AI"
my_version = "9"

# ✅ Request model
class ChatRequest(BaseModel):
    message: str

# ✅ API endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    response = openai_client.responses.create(
        input=[{"role": "user", "content": req.message}],
        extra_body={
            "agent_reference": {
                "name": my_agent,
                "version": my_version,
                "type": "agent_reference",
            }
        },
    )

    return {"reply": response.output_text}
