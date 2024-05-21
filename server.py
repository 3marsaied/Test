from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

app = FastAPI()

class PatientData(BaseModel):
    heart_rate: int

# Redis Cloud connection details
redis_host = 'redis-11068.c325.us-east-1-4.ec2.redns.redis-cloud.com'
redis_port = 11068
redis_password = 'n8rNyzV1BBbA00Ki4kK92poJXxbSuOB5'

@app.post("/receive_data/{patient_id}/{patient_data}")
async def receive_data(patient_id: int, patient_data: int):
    try:
        # Connect to Redis Cloud
        r = redis.StrictRedis(
            host=redis_host, port=redis_port, password=redis_password
        )

        # Store data in Redis
        redis_key = f"patient:{str(patient_id)}"
        r.rpush(redis_key, patient_data)

        return {"message": "Data received and stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store data: {str(e)}")

@app.get("/get_data/{patient_id}")
async def get_data(patient_id: int):
    try:
        # Connect to Redis Cloud
        r = redis.StrictRedis(
            host=redis_host, port=redis_port, password=redis_password
        )

        # Retrieve data from Redis
        redis_key = f"patient:{str(patient_id)}"
        data = r.lrange(redis_key, 0, -1)  # Retrieve all data from the list

        # If data exists for the patient ID
        if data:
            # Decode the byte strings and convert them to dictionaries
            decoded_data = [eval(item.decode()) for item in data]
            return {"heart_rate":decoded_data}
        else:
            raise HTTPException(status_code=404, detail="No data found for the patient")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")