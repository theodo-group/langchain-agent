import os
import json
from pathlib import Path
from typing import Dict, Any, Union
from pydantic import BaseModel, ValidationError


class InputSchema(BaseModel):
    directoryPath: str


class OutputItem(BaseModel):
    name: str
    path: str
    type: str


class OutputSchema(BaseModel):
    currentDirectory: str
    fileTree: list[OutputItem]


def list_files(dir_path: str):
    files = []
    for entry in os.scandir(dir_path):
        item = {
            "name": entry.name,
            "path": str(entry.path),
            "type": "directory" if entry.is_dir() else "file",
        }


        files.append(item)

    return files


class ListFilesInADirectory:
    name = "list-files-in-a-directory"
    description = (
        'Returns the path of the current directory, and a tree structure of the '
        'descendant files. The action input should adhere to this JSON schema: '
        '{{"type":"object","properties":{{"directoryPath":{{"type":"string","description":'
        '"The path of the directory to list files from"}}}},"required":["directoryPath"]}}'
    )

    @staticmethod
    def call(directory_path: str) -> Dict[str, Any]:
        try: 
            current_directory = str(Path(directory_path).resolve())        
            input_data = {"directoryPath": directory_path}
            file_tree = list_files(input_data["directoryPath"])
            return {"currentDirectory": input_data["directoryPath"], "fileTree": file_tree[:100]}
        except (json.JSONDecodeError, ValidationError) as e:
            raise ValueError(str(e))
        

    def validate_input(self, input_data: str) -> InputSchema:
        try:
            input_data = json.loads(input_data)
            return InputSchema(**input_data)
        except (json.JSONDecodeError, ValidationError) as e:
            raise ValueError(str(e))

    def validate_output(self, output_data: Dict[str, Any]) -> OutputSchema:
        try:
            return OutputSchema(**output_data)
        except ValidationError as e:
            raise ValueError(str(e))

    def run(self, arg: str) -> str:
        try:
            input_data = self.validate_input(arg)
            output = self.call(input_data.directoryPath)
            validated_output = self.validate_output(output)
            return json.dumps(validated_output.dict())
        except Exception as e:
            return json.dumps({"error": str(e)})