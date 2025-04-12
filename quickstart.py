import os.path
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def compare_books_with_local(local_files: set[str]) -> List[dict]:
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        query = (
            "mimeType='application/pdf' or "
            "mimeType='application/epub+zip' or "
            "mimeType='application/x-djvu' or "
            "mimeType='application/x-mobipocket-ebook'"
        )

        results = (
            service.files()
            .list(
                q=query,
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType)"
            )
            .execute()
        )

        drive_files = results.get("files", [])
        seen_names = set()
        unique_drive_files = []
        for file in drive_files:
            name = file['name']
            if name not in seen_names:
                seen_names.add(name)
                unique_drive_files.append(file)

        missing = [
            file for file in unique_drive_files
            if file['name'] not in local_files
        ]

        return missing

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def download_file_from_drive(file_id: str, filename: str, output_dir: str, creds: Credentials):
    service = build("drive", "v3", credentials=creds)
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"Downloaded to: {file_path}")
    return file_path


if __name__ == "__main__":
    local_books = {"11. Finale.pdf", "mybook.pdf", "sample.pdf"}
    missing_books = compare_books_with_local(local_books)

    if not missing_books:
        print("No missing files. Everything in Drive is already local.")
    else:
        print("Missing files from local:")
        for file in missing_books:
            print(f"{file['name']}")
        
        # Example: download the first missing file
        to_download = missing_books[0]
        output_directory = "./downloads"
        os.makedirs(output_directory, exist_ok=True)
        download_file_from_drive(
            file_id=to_download['id'],
            filename=to_download['name'],
            output_dir=output_directory,
            creds=Credentials.from_authorized_user_file("token.json", SCOPES)
        )