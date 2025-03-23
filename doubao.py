import base64
from openai import OpenAI
from typing import List, Optional
import os

class DoubaoVisionLLM:
    def __init__(
        self, 
        model_name: str,
        api_key: Optional[str] = None,
        base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    ):
        self.model_name = model_name
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key or os.getenv("ARK_API_KEY")
        )

    def _get_image_mime_type(self, image_path: str) -> str:
        """Get the MIME type based on the image file extension."""
        ext = image_path.lower().split('.')[-1]
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png'
        }
        return mime_types.get(ext, 'image/jpeg')

    def _image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_response(
        self,
        prompt: str,
        image_paths: List[str],
        system_prompt: str = "你是一个结合文本与图片回答问题的AI助手。"
    ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", 
                 "content": [
                    {"type": "text", "text": prompt},
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{self._get_image_mime_type(image_path)};base64,{self._image_to_base64(image_path)}",
                            },
                        }
                        for image_path in image_paths
                    ]
                ]},
            ],
        )
        return completion.choices[0].message.content