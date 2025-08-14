import asyncio
import os
from typing import Optional
from unittest import async_case

from dotenv import load_dotenv
from httpx import Client
from openai import BaseModel, OpenAI
from openai.types import vector_store

load_dotenv()

openai_model_gpt41 = "gpt-4.1"
vector_store_name = "TestVectorStore"
vs_file_id = "file-RS6D5VLa9XUKh1QNmayoQV"

openai = OpenAI()


class VectorStore(BaseModel):
    id: str
    name: str


def file_exists(vector_store_files, file_id: str) -> bool:
    for vs_file in vector_store_files:
        # print(vs_file)
        if vs_file.id == file_id:
            return True
        return False


async def get_vector_store_id(vector_store_name: str) -> Optional[str]:
    print(f"Fetching vector store id for: {vector_store_name}")
    vector_stores = [(vs.name, vs.id) for vs in openai.vector_stores.list()]
    for vs_name, vs_id in vector_stores:
        if vs_name == vector_store_name:
            return vs_id
    return None


async def create_vector_store(vector_store_name: str) -> VectorStore:
    print(f"Creating vector store: {vector_store_name}")
    return openai.vector_stores.create(name=vector_store_name)


async def check_file_exists_in_vector_store(file_id: str, vector_store_id: str) -> bool:
    print(f"Checking if file exists in vectorStore: {vector_store_id} {file_id}")
    vector_store_files = openai.vector_stores.files.list(vector_store_id)
    if file_exists(vector_store_files, file_id):
        return True
    while vector_store_files.has_next_page():
        vector_store_files = vector_store_files.get_next_page()
        if file_exists(vector_store_files, file_id):
            return True
    return False


async def upload_file_to_vector_store(file_path: str, vector_store_id: str):
    print(f"Uploading file in vector store: {vector_store_id} file: {file_path}")
    file = openai.files.create(file=open(file_path, "rb"), purpose="assistants")
    print(f"File uploaded: {file} adding file to vector store")
    openai.vector_stores.files.create_and_poll(
        vector_store_id=vector_store_id, file_id=file.id
    )
    # In real life after you upload file you will have to manually track file id with filename in db
    vs_file_id = file.id


async def check_file_exists_in_local(file_path: str) -> bool:
    print(f"Checking if file exists in local: {file_path}")
    return os.path.exists(file_path) and os.path.isfile(file_path)


def format_results(results) -> str:
    formatted_results = "<sources>"
    for result in results:
        formatted_result = (
            f"<result file_id='{result.file_id}' filename='{result.filename}'>"
        )
        for part in result.content:
            formatted_result += f"<content>{part.text}</content>"
        formatted_results += formatted_result + "</result>"
    return formatted_results + "</sources>"


async def perform_rag(user_query: str, vector_store_id: str):
    results = openai.vector_stores.search(
        vector_store_id=vector_store_id, query=user_query
    )
    formatted_results = format_results(results.data)
    # print(formatted_results)
    completion = openai.chat.completions.create(
        model=openai_model_gpt41,
        messages=[
            {
                "role": "user",
                "content": "Provide a concise answer to the query based on the provided sources.",
            },
            {
                "role": "user",
                "content": f"Sources: {formatted_results}\n\nQuery: '{user_query}'",
            },
        ],
    )
    print(f"\nQuery: {user_query}\nResponse: {completion.choices[0].message.content}\n")


async def main():
    file_path = os.path.join("vector_store_demo", "dummy_company_policy.txt")
    if not await check_file_exists_in_local(file_path):
        raise ValueError(f"file: {file_path} is not present!")
    vector_store_id = await get_vector_store_id(vector_store_name)
    if not vector_store_id:
        vector_store = await create_vector_store(vector_store_name)
        vector_store_id = vector_store.id
    print(f"Vector store id: f{vector_store_id}")
    if not await check_file_exists_in_vector_store(vs_file_id, vector_store_id):
        await upload_file_to_vector_store(file_path, vector_store_id)
    await perform_rag("What is policy for Dummy Company?", vector_store_id)
    await perform_rag("What is capital of India?", vector_store_id)


"""
		Files can be uploaded to openai and then the files can be added to vector store
		Then based on the files uploaded in vector store questions can be answered
		Uploaded files and vector store can be viewed at: https://platform.openai.com/storage/files/
"""
if __name__ == "__main__":
    asyncio.run(main())
