from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

stored_data = []
current_global_depth = 1
max_bucket_size = 2
bucket_directory = {'0': [], '1': []}

def compute_hash(value, depth):
    return bin(value % (2 ** depth))[2:].zfill(depth)

def perform_rehash():
    global current_global_depth, bucket_directory, stored_data

    for bucket in bucket_directory:
        bucket_directory[bucket].clear()

    for value in stored_data:
        index = compute_hash(value, current_global_depth)

        if len(bucket_directory[index]) < max_bucket_size:
            bucket_directory[index].append(value)
        else:
            current_global_depth += 1  
            new_bucket_directory = {}
            
            for i in range(2 ** current_global_depth):
                new_bucket_directory[bin(i)[2:].zfill(current_global_depth)] = []

            for val in stored_data:
                new_index = compute_hash(val, current_global_depth)
                new_bucket_directory[new_index].append(val)

            bucket_directory = new_bucket_directory
            break

class ValueInput(BaseModel):
    value: int

@app.get("/directory")
def fetch_directory():
    result = []
    for bucket_index, values in bucket_directory.items():
        result.append(f"Bucket {bucket_index}")
        result.append(f"Values: {', '.join(map(str, values)) if values else ''}")
        local_depth = len(values)  
        result.append(f"Local Depth: {local_depth}")
    formatted_output = "\n".join(result)
    return {"global_depth": current_global_depth, "directory": bucket_directory, "formatted_directory": formatted_output}

@app.post("/insert")
def add_value(item: ValueInput):
    global stored_data
    stored_data.append(item.value)
    perform_rehash()
    return {"message": f"Value {item.value} inserted", "directory": fetch_directory()["directory"]}

@app.post("/delete")
def remove_value(item: ValueInput):
    global stored_data
    if item.value in stored_data:
        stored_data.remove(item.value)
        perform_rehash()
        return {"message": f"Value {item.value} deleted", "directory": fetch_directory()["directory"]}
    return {"message": f"Value {item.value} not found", "directory": fetch_directory()["directory"]}

@app.post("/clear")
def reset_storage():
    global stored_data, current_global_depth, bucket_directory
    stored_data.clear()
    current_global_depth = 1  
    bucket_directory = {'0': [], '1': []}  
    return {"message": "All values cleared successfully and buckets reset to default."}
