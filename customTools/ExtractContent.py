from langchain.agents import Tool
import requests
from bs4 import BeautifulSoup
import jsonschema
import json


class ExtractTextContentFromUrl:
    name = "extract-text-content-from-url"
    description = (
        "It extracts the text content from a URL. It requests the content of the URL. "
        "Useful when you want to know what a page says. The action input MUST adhere "
        "to this JSON schema: "
        '{"type":"object","properties":{"url":{"type":"string","format":"uri", "description": "The url to extract content from"} },"required":["url"]}'
    )

    input_schema = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "format": "uri"
            }
        },
        "required": [
            "url"
        ]
    }

    output_schema = {
        "type": "object",
        "properties": {
            "textContent": {
                "type": "string"
            }
        },
        "required": [
            "textContent"
        ]
    }

    @staticmethod
    def validate(data, schema):
        try:
            jsonschema.validate(data, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Validation error: {e.message}")

    @staticmethod
    def call(input_data):
        ExtractTextContentFromUrl.validate(input_data, ExtractTextContentFromUrl.input_schema)
        response = requests.get(input_data["url"])
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = soup.get_text()
        ## Clean up the text
        text_content = text_content.replace("\n", " ")
        text_content = text_content.replace("\t", " ")
        text_content = text_content.replace("\r", " ")
        text_content = text_content.replace("  ", " ")

        ## Limit the text to 2000 words
        text_content = " ".join(text_content.split(" ")[:2000])
        output = {"textContent": text_content}
        # ExtractTextContentFromUrl.validate(output, ExtractTextContentFromUrl.output_schema)
        return output

    def run(self, arg: str) -> str:
        try:
            print(f"Input JSON: {arg}")
            input_data = json.loads(arg)
            self.validate(input_data, self.input_schema)
            output = self.call(input_data)
            print(f"Output JSON: {output}")

            return json.dumps(output)
        except ValueError as e:
            return json.dumps({"error": str(e)})
        