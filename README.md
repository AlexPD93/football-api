# Football API & Dashboard

A modern, serverless web application for tracking football player statistics (goals and wins). Built with **FastAPI**, **HTMX**, and **DynamoDB**, and deployed using the **Serverless Framework**.

## 🚀 Features

- **Dynamic Dashboard**: Real-time updates using HTMX (no full-page reloads).
- **Player Management**: Create, update, and delete player statistics.
- **Role-Based Access**: 
  - **Admins**: Full CRUD permissions (configured via an email whitelist).
  - **Guests**: View-only access.
- **Authentication**: Integrated with Google OAuth via Authlib.
- **Infrastructure**: Fully serverless architecture on AWS (Lambda + DynamoDB).
- **Containerized**: Deployed as a Docker container for consistency across environments.

## 🛠 Tech Stack

- **Backend**: Python 3.x, FastAPI, Pydantic
- **Frontend**: HTMX, Jinja2 Templates, Vanilla CSS
- **Database**: AWS DynamoDB (via PynamoDB)
- **Deployment**: Serverless Framework, AWS Lambda (Docker Runtime)
- **Monitoring**: Sentry Integration

## 📋 Prerequisites

- Python 3.10+
- Node.js & NPM (for Serverless Framework plugins)
- Docker (for deployment)
- AWS CLI configured with appropriate credentials

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd football-api
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Install Serverless dependencies**:
   ```bash
   npm install
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and populate it:
   ```env
   SECRET_KEY="your-secret-key"
   PERSON_TABLE_NAME="your-dynamodb-table-name"
   ADMIN_WHITELIST="admin1@example.com,admin2@example.com"
   GOOGLE_CLIENT_ID="your-google-client-id"
   GOOGLE_CLIENT_SECRET="your-google-client-secret"
   ```

## 🏃 Local Development

Run the application locally using Uvicorn:
```bash
uvicorn main:app --reload
```
The dashboard will be available at `http://localhost:8000/dashboard`.

## 🚢 Deployment

The project is deployed to AWS Lambda using the Serverless Framework with a Docker image runtime.

**Deploy to dev:**
```bash
serverless deploy --stage dev
```

The configuration is managed via `serverless.yml`, which handles:
- ECR image creation and upload.
- IAM roles for DynamoDB access.
- Environment variable injection.

## 📁 Project Structure

- `main.py`: Application entry point and middleware configuration.
- `routers/`: FastAPI routers for API endpoints, dashboard, and login logic.
- `actions/`: Business logic and database operations (CRUD).
- `models/`: Pydantic and PynamoDB data models.
- `templates/`: Jinja2 HTML templates and HTMX partials.
- `static/`: Static assets (CSS, HTMX library).
- `serverless.yml`: Infrastructure as Code configuration.
- `Dockerfile`: Container definition for Lambda runtime.

## 🧪 Testing

(Add instructions here once test suites are implemented)

---
