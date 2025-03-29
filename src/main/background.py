# For FastAPI BackgroundTasks:
# 'from fastapi import BackgroundTasks'
from json import loads, dumps

def accountForUsage(*files_paths):
    print("Running in background, after execution")
    # with open("usage-reg.json", "r") as usage_json:
    #     usage_reg: dict = loads(usage_json.read())
    #     if len(usage_reg.keys()) == 0: #if empty/not initialized
    #         usage_reg = {}
    
