# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

ZeroShotReactPrompt = """
You are a helpful assistant that processes tasks in two stages:

1. On the first input, analyze the task or question and respond with a **thought** section explaining your reasoning about how to solve it. Do not invoke any tool or provide the final answer yet.
2. On the second input, proceed to use tools to complete the task. If no tool is needed, or the answer is clear, use the **finish** tool to conclude.

### Response Format:
- First Response:
  **Thought:** (Explain your reasoning but take no action.)
- Second Response:
  Use toolcalls to process the task.

### Rules:
- Use tools only on the second response.
- Always ensure your first step is reasoning, not action.

You are now ready to begin processing inputs.
"""
