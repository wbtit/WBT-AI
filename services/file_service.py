import os
from fastapi import UploadFile
from datetime import datetime,timezone
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH","./app/storage/uploads")

class FileService:
    @staticmethod
    async def save_file(file:UploadFile)->str:
        os.makedirs(STORAGE_PATH,exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        filename= f"{timestamp}_{file.filename}"
        file_path= os.path.join(STORAGE_PATH,filename)
        
        with open(file_path,"wb") as f:
            f.write(await file.read())

        return file_path