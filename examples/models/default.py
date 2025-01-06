from copy import deepcopy
from synthora.models.openai_chat import OpenAIChatBackend

model = OpenAIChatBackend.default()

# lazy init client to enable deepcopy
print(deepcopy(model).client)