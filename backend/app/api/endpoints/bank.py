import os
import uuid
import hashlib
import base64
from typing import Tuple

import pdfplumber
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import BankStatement, User
from app.schemas.responses import BankProcessResponse


router = APIRouter()


@router.post("/process_bank_statement", response_model=BankProcessResponse, status_code=201)
async def create_new_process_bank_statement(
        bank_statement: UploadFile = File(...),
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
):
    """Processes a bank statement and saves it to the database.
    :param bank_statement: The uploaded bank statement file
    :param session: The database session
    :param current_user: The currently authenticated user
    :return: The response containing the processed bank statement message
    """
    try:
        # Read the contents of the uploaded file
        contents = await bank_statement.read()

        # Decode the Base64-encoded bank statement
        encoded_data = base64.b64encode(contents).decode("utf-8")
        contents = base64.b64decode(encoded_data)

        # Extract text from the PDF file
        text, filename = extract_text_from_pdf(contents)

        new_bank_statement = BankStatement(
            user_id=current_user.id,
            base64_bank_statement=calculate_file_hash(filename),
        )

        session.add(new_bank_statement)
        await session.commit()
        return BankProcessResponse(message=text)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing bank statement") from e


def extract_text_from_pdf(decoded_data: bytes) -> Tuple[str, str]:
    """
         Extracts text from a PDF file given its decoded data
    :param decoded_data(bytes) The decoded data of the PDF file
    :return: A tuple containing the extracted text and the file path.
    :rtype: Tuple[str, str]
    """

    folder_path = "pdf_files/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    unique_filename = str(uuid.uuid4()) + ".pdf"
    file_path = os.path.join(folder_path, unique_filename)

    try:
        with open(file_path, "wb") as file:
            file.write(decoded_data)
    except OSError as e:
        raise OSError(f"Error writing PDF file: {e}")

    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text, file_path


def calculate_file_hash(file_path, algorithm="sha256") -> str:
    """
        Calculate the hash value of a file using the specified algorithm
    :param file_path: The path to the file
    :param algorithm: The hash algorithm to use. Defaults to "sha256"
    :return: str: The calculated hash value as a hexadecimal string.
    """

    hash_object = hashlib.new(algorithm)

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_object.update(chunk)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    file_hash = hash_object.hexdigest()

    return file_hash
