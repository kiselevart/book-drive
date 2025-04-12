import os.path
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

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

# Example usage
if __name__ == "__main__":
    local_books = {"11. Finale.pdf", "mybook.pdf", "sample.pdf"}
    missing_books = compare_books_with_local(local_books)
    if not missing_books:
        print("No missing files. Everything in Drive is already local.")
    else:
        print("Missing files from local:")
        for file in missing_books:
            print(f"{file['name']}")