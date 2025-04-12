# Book-Drive

**Book-Drive** is a mobile book reader that seamlessly synchronizes with your Google Drive. It indexes your locally installed books, lets you selectively import new titles from your Drive, and keeps your reading progress in sync across devices.

---

## Core Functionality

- **Local Book Indexing:**  
  Automatically scan and index books already installed on your device.

- **Google Drive Integration:**  
  - **Selective Import:** Browse and select books from your designated Google Drive folder that haven’t been indexed yet.
  - **Dynamic Syncing:** Automatically update the sync list when new books are added or removed.
  - **In-App Folder Management:**  
    - Upload new books  
    - Delete unwanted files  
    - Edit file names directly within the app

- **Reading Progress Tracking:**  
  Record your progress (e.g., current page, total pages) for each book so you can easily resume reading anywhere.

- **Built-In PDF Reader:**  
  Enjoy a smooth, integrated PDF reading experience without the need to switch to external apps.

---

## Features

- **Seamless Synchronization:**  
  Integrate with Google Drive to keep your digital library up-to-date.

- **User-Friendly Interface:**  
  Intuitive tools for managing your books—upload, delete, rename—directly from your app.

- **Persistent Reading Experience:**  
  Sync your reading progress across devices, ensuring you always pick up exactly where you left off.

- **Offline Access:**  
  Once downloaded, books are available for offline reading.

## Technical Overview

- **Platform:** Android
- **Programming Language:** Kotlin 
- **API Integration:** Google Drive API (via REST with OAuth2 for secure authentication)