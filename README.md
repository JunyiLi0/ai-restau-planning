# AI Restaurant Planning

A SaaS application that automatically generates employee work schedules for restaurants using AI. Users can upload PDF files or use a chat interface to specify scheduling requirements, and the system generates/modifies Excel planning files with PDF export capability.

## Features

- **AI-Powered Scheduling**: Use natural language to create and modify employee schedules
- **PDF Upload**: Upload existing schedule PDFs to extract and import data
- **Excel Import/Export**: Load existing Excel plannings or export new ones
- **PDF Export**: Generate professional PDF reports of your schedules
- **Chat Interface**: Conversational UI to modify schedules on the fly
- **Real-time Updates**: See schedule changes immediately in the planning view

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **OpenAI GPT-4** - AI-powered schedule generation
- **openpyxl** - Excel file handling
- **pdfplumber** - PDF text extraction
- **ReportLab** - PDF generation

### Frontend
- **React 18** with TypeScript
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## Project Structure

```
ai-restau-planning/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── services/         # API calls
│   │   └── types/            # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/routes/       # API endpoints
│   │   ├── core/             # Configuration
│   │   ├── models/           # Data models
│   │   └── services/         # Business logic
│   ├── data/                 # File storage
│   └── requirements.txt
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/pdf` | Upload PDF file for parsing |
| POST | `/api/upload/excel` | Upload existing Excel planning |
| GET | `/api/planning/current` | Get current planning data |
| PUT | `/api/planning/update` | Update planning manually |
| POST | `/api/planning/generate` | Generate new planning with AI |
| PUT | `/api/planning/ai-update` | Update existing planning with AI |
| POST | `/api/chat/message` | Send chat message for planning |
| GET | `/api/export/pdf` | Download planning as PDF |
| GET | `/api/export/excel` | Download planning as Excel |

## Excel Planning Structure

Each week's planning includes:
- Employee names
- Daily schedules (Monday-Sunday)
- For each day: Afternoon hours/meals, Evening hours/meals
- Weekly totals for hours and meals

## Usage Examples

### Create a new schedule via chat:
```
"Create a schedule for week 3 with employees: John, Marie, and Pierre.
John works Monday to Friday afternoons (4h each),
Marie works evenings Tuesday to Saturday (5h each),
Pierre works full days on weekends."
```

### Modify an existing schedule:
```
"Add 2 hours to John's Monday afternoon shift"
"Remove Marie from Thursday evening"
"Add a new employee Sophie working Monday and Wednesday afternoons"
```

## License

MIT
