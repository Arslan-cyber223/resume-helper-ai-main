# Resume Builder Pro 🚀

An AI-powered resume builder application that helps you create, edit, and improve your resume with intelligent suggestions. Built with Flask and featuring Google Gemini AI integration.

## ✨ Features

- **📝 Intuitive Editor**: Drag-and-drop interface with real-time editing
- **🎨 Multiple Templates**: Choose from Modern, Professional, Creative, and Minimal designs
- **🤖 AI-Powered Suggestions**: Get intelligent recommendations using Google Gemini Flash 2.5
- **📤 Smart Upload**: Import your old resume (PDF, DOCX, or TXT) with preserved formatting
- **✍️ AI Text Improvement**: Select any text and let AI enhance it
- **💾 Auto-Save**: Your work is automatically saved to your browser
- **🎨 Distinctive Design**: Features a fresh green/teal/orange color scheme
- **📱 Responsive**: Works on desktop, tablet, and mobile devices
- **🖨️ Print Ready**: Download your resume as PDF using browser print

## 🎨 Design Philosophy

Unlike typical AI apps that use purple and blue, Resume Builder Pro features:

- **Primary**: Teal (#00BFA5)
- **Secondary**: Orange (#FF6F00)
- **Accent**: Green (#4CAF50)

This distinctive color palette makes the app stand out while maintaining professionalism.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:

   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key**:

   Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

   **Windows PowerShell**:

   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```

   Or create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your-api-key-here
   ```

4. **Run the application**:

   ```powershell
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 How to Use

### 1. Choose a Template

Click on any template from the sidebar (Modern, Professional, Creative, or Minimal) to get started.

### 2. Edit Your Resume

- Click on any text to edit it directly
- Use the toolbar for formatting (bold, italic, underline, etc.)
- Drag and rearrange sections as needed

### 3. Upload Existing Resume

- Click "Upload Resume" button
- Drag & drop or browse for your file (PDF, DOCX, or TXT)
- The text will be extracted and loaded into the editor

### 4. Get AI Suggestions

- Click "Get Suggestions" to receive AI-powered improvement recommendations
- Review suggestions in the sidebar
- Apply changes manually to your resume

### 5. Improve Specific Text

- Select any text in your resume
- Click the "Improve" button in the toolbar
- AI will suggest an enhanced version

### 6. Download Your Resume

- Click "Download PDF" or press Ctrl+P
- Use your browser's print dialog to save as PDF

## 🔧 Project Structure

```
resume-helper/
│
├── app.py                 # Flask backend with API endpoints
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/
│   └── index.html        # Main HTML template
│
├── static/
│   ├── style.css         # Styles with green/teal/orange theme
│   └── script.js         # Frontend JavaScript
│
└── uploads/              # Temporary folder for file uploads (auto-created)
```

## 🔑 API Endpoints

- `GET /` - Main application page
- `POST /api/upload-resume` - Upload and extract text from resume files
- `POST /api/get-suggestions` - Get AI suggestions for resume improvement
- `POST /api/improve-text` - Get AI-improved version of selected text

## 💡 Features in Detail

### AI Suggestions

The app analyzes your resume and provides suggestions for:

- Content clarity and impact
- Achievement quantification
- Keyword optimization
- Professional formatting
- Action verb usage

### Template System

Each template is designed for different career levels and industries:

- **Modern**: Tech and startup-focused
- **Professional**: Corporate and traditional industries
- **Creative**: Design, arts, and creative fields
- **Minimal**: Clean and simple for any industry

### Auto-Save

Your resume is automatically saved to browser's localStorage every time you make changes. Never lose your work!

## 🛠️ Customization

### Change Colors

Edit `static/style.css` and modify the CSS variables:

```css
:root {
  --primary-color: #00bfa5; /* Teal */
  --secondary-color: #ff6f00; /* Orange */
  --accent-color: #4caf50; /* Green */
}
```

### Add New Templates

Edit `static/script.js` and add your template to the `templates` object.

## 🔒 Privacy & Security

- All resume editing happens in your browser
- Uploaded files are temporarily processed and immediately deleted
- AI suggestions are processed through Google's Gemini API
- Auto-save uses browser localStorage (data stays on your device)

## 📝 Tips for Best Results

1. **Be Specific**: Use quantifiable achievements (e.g., "Increased sales by 40%")
2. **Use Action Verbs**: Start bullet points with strong verbs (Led, Developed, Achieved)
3. **Keep It Concise**: Aim for 1-2 pages maximum
4. **Get AI Feedback**: Use the suggestions feature multiple times as you refine
5. **Customize for Jobs**: Adjust your resume for each job application

## 🤝 Contributing

Feel free to fork this project and customize it for your needs!

## 📄 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- AI powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Icons from [Font Awesome](https://fontawesome.com/)

## 🐛 Troubleshooting

**Issue**: AI suggestions not working

- **Solution**: Make sure your GEMINI_API_KEY is set correctly

**Issue**: File upload fails

- **Solution**: Check file format (only PDF, DOCX, TXT supported) and size (max 16MB)

**Issue**: Styles not loading

- **Solution**: Clear browser cache and refresh

## 📧 Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.

---

Made with 💚 by Resume Builder Pro Team
