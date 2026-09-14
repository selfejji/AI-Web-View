import re
from typing import Optional
from pydantic import BaseModel

import re
from typing import Optional
from pydantic import BaseModel

class Filter:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Retrieve the last assistant message
        messages = body.get("messages", [])
        if not messages or messages[-1].get("role") != "assistant":
            return body

        content = messages[-1].get("content", "")

        # Regex targeting html, css, and js/javascript markdown blocks
        pattern = re.compile(
            r"```(html|css|js|javascript)\n(.*?)```", 
            re.DOTALL | re.IGNORECASE
        )

        extracted_code = { 
            "html": [], 
            "css": [], 
            "javascript": [] 
        }

        # Separate code blocks into language lists
        for lang, code in pattern.findall(content):
            key = "javascript" if lang.lower() in ["js", "javascript"] else lang.lower()
            extracted_code[key].append(code.strip())

        # Strip out the code blocks to leave pure text explanations
        cleaned_text = pattern.sub("", content).strip()

        messages[-1]["content"] = cleaned_text

        # Inject structured data into the payload body
        body["extracted_code"] = extracted_code
        body["cleaned_text"] = cleaned_text

        return body