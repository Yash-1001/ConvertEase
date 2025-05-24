# 🚀 ConvertEase

**ConvertEase** is a powerful and user-friendly web application designed to simplify file conversions. Whether you're working with PDFs, JSON, Excel files, or other formats, ConvertEase offers a seamless experience to upload, convert, and download your files in just a few clicks.

## ✨ Features

- 📄 Convert files between multiple formats (e.g., PDF ⇌ Excel, JSON ⇌ Excel)
- 🔐 Secure login and file handling
- 📁 Download converted files instantly
- 🗂 Organized dashboard with multiple conversion options
- 🖥️ Built using Django for backend, HTML/CSS/JS for frontend

## 💻 Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Django Auth
- **File Handling**: Python, Adobe PDF Services API (for PDF-related conversions)
- **Database**: SQLite (or any Django-supported DB)

## 🚧 How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Yash-1001/ConvertEase.git
   cd ConvertEase
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the App**
   - Visit: `http://127.0.0.1:8000`

## 📸 Screenshots

_Add screenshots or GIFs here showing the UI._

## 📂 Folder Structure

```
ConvertEase/
│
├── core/                   # Main app for file conversion logic
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
├── media/                  # Uploaded & converted files
├── manage.py
└── requirements.txt
```

## 🛡️ Security & Privacy

- All file uploads are user-authenticated.
- Files are automatically removed after download or after a set time period.
- No user data is shared or stored beyond conversion needs.

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request for new features or bug fixes.


