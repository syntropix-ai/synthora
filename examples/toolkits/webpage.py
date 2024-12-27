import json
from synthora.toolkits.webpage_toolkit import TrafilaturaWebpageReader

reader = TrafilaturaWebpageReader(False)
tool = reader.sync_tools[0]

print(json.dumps(tool.schema, indent=2))

print(tool.run("https://github.com/camel-ai/camel/pull/1315"))
