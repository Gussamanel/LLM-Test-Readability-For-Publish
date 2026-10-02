import sys
import os
sys.path.append(os.path.abspath('src'))
from util.model_lib.models_thesis import Model

print("Loading model...")
model = Model.get(
    model_name_or_path="deepseek-ai/deepseek-coder-33b-instruct",
    max_new_tokens=2048,
    context_window=16384,
    temperature=1.0
)

print("Model loaded. Testing get_response...")
try:
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    res = model.get_response(history, "Hello, how are you?")
    print("Response:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
