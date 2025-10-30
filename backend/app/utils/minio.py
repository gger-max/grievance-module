import requests
import os
from typing import Optional, Dict, Any
import uuid
from fastapi import HTTPException

class MinIOClient:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
        self.bucket_name = os.getenv("MINIO_BUCKET", "grievance-bucket")

    def upload_file(self, file_content: bytes, filename: str, content_type: str) -> Dict[str, Any]:
        """Upload a file to MinIO and return file info."""
        # Generate unique filename
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        try:
            # Simple PUT request to MinIO (bucket has public access)
            url = f"{self.endpoint}/{self.bucket_name}/{unique_filename}"
            headers = {'Content-Type': content_type}

            response = requests.put(url, data=file_content, headers=headers)

            if response.status_code in [200, 201]:
                file_url = f"{self.endpoint}/{self.bucket_name}/{unique_filename}"
                return {
                    "name": filename,
                    "url": file_url,
                    "size": len(file_content),
                    "type": content_type,
                    "key": unique_filename
                }
            else:
                raise HTTPException(status_code=500, detail=f"Upload failed with status {response.status_code}: {response.text}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

    def delete_file(self, file_key: str) -> bool:
        """Delete a file from MinIO."""
        try:
            url = f"{self.endpoint}/{self.bucket_name}/{file_key}"
            response = requests.delete(url)
            return response.status_code in [200, 204]
        except Exception:
            return False

# Global instance
minio_client = MinIOClient()