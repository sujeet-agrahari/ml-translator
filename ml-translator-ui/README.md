# PDF Content Translator

This Angular application allows users to upload a PDF, select a target language, and translate the content of the PDF. The translated content can be downloaded as a PDF file.

## Features

- Upload a PDF file.
- Select a target language from a dropdown list.
- Translate the content of the uploaded PDF.
- Download the translated PDF file.

## Prerequisites

- Node.js (v18)
- Angular CLI (v16)
  npm install -g @angular/cli@16
  ng version
- A local server or backend API to handle PDF translation (e.g., a server running at `http://localhost:3000`)

## Installation

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo/ml-translator-ui
   ```

2. **Install dependencies**
    ```
       npm install
    ```

3. **Run the Angular application**

    ```
       ng serve
    ```
The application will be available at http://localhost:4200.

## **Usage**

1.Upload PDF File:
Click the "Choose File" button to upload a PDF file.

2.Select Language:
Choose the target language from the dropdown menu.

3.Translate:
Click the "Translate" button to send the PDF file to the server for translation.

4.Download Translated PDF:
After translation, a file path will be displayed, showing the location where the translated PDF can be downloaded.


## **Configuration**
1.Backend API URL: 
Ensure your backend API is running and accessible at http://localhost:3000 (or update the URL in the Angular service).

2.Background Image: 
Update the background image URL in translator.component.scss as needed.
