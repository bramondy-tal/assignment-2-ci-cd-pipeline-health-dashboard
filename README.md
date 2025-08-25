# CI Dashboard Application

## Description
The CI Dashboard is a containerized application designed to monitor and visualize Continuous Integration (CI) metrics. It consists of a **React** frontend, a **FastAPI** backend, and a **TimescaleDB** database. The application provides insights into build metrics, durations, and statuses, and sends email alerts for critical events.

---

## Features
- **Frontend**:
  - Interactive dashboard with metrics visualization.
  - Responsive design using React and TailwindCSS.
- **Backend**:
  - API endpoints for metrics, email alerts, and GitHub data ingestion.
  - Integration with TimescaleDB for data storage.
- **Database**:
  - Stores build metrics and alerts.
  - Schema migrations for database setup.

---

## Prerequisites
- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: Required for orchestrating the services.

---

## Setup and Usage

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Start the Application
Use Docker Compose to build and start the services:
```bash
docker-compose up -d --build
```

### 3. Access the Application
- **Frontend**: Open your browser and navigate to `http://localhost:5173`.
- **Backend**: API is available at `http://localhost:8000`.
- **Database**: Accessible on port `5432`.

### 4. Stop the Application
To stop the services, run:
```bash
docker-compose down
```

### 5. Apply Database Migrations
Before testing the application, ensure the database schema is set up by applying migrations:
```bash
docker exec -it assignment_db_1 psql -U postgres -d ci_dashboard -f /db/migrations/001_create_builds.sql

docker exec -it assignment_db_1 psql -U postgres -d ci_dashboard -f /db/migrations/002_create_build_alerts.sql
```
This step initializes the necessary tables in the database.

---

## How to Use the Application

### 1. Start the Application
- Ensure Docker and Docker Compose are installed on your system.
- Navigate to the project directory and run:
  ```bash
  docker-compose up -d --build
  ```
  This will build and start the frontend, backend, and database services.

### 2. Provide a Repository for Ingestion
- On the dashboard, input the GitHub repository you want to monitor.
- The backend will fetch data from GitHub Actions for the specified repository.

### 3. View Metrics
- Once the data is fetched, the dashboard will display metrics for the provided repository, including:
  - Build durations.
  - Last Build statuses.
  - Sucesss and Failure Rates.

### 4. Stop the Application
- To stop all running services, use:
  ```bash
  docker-compose down
  ```

### 5. Apply Database Migrations (if not already done)
- Ensure the database schema is initialized by running the migration scripts as described in the "Apply Database Migrations" section.

### 6. Debugging
- Check logs for any issues:
  ```bash
  docker logs <container_id>
  ```
- Replace `<container_id>` with the ID of the service you want to debug.

---

## Environment Variables

Before running the application, ensure the following environment variables are set in the `.env` file or directly in the `docker-compose.yml` file:

- `GITHUB_TOKEN`: Your GitHub personal access token for API access.

These variables are required for the backend service to function correctly. Replace the placeholders with your own values.

### Using a `.env` File

Instead of directly setting environment variables in the `docker-compose.yml` file, you can use a `.env` file for better security and organization. Create a `.env` file in the root directory and add the following variables:

```
GITHUB_TOKEN=<your-github-token>
```

Make sure to replace `<your-github-token>` with your actual value. The `docker-compose.yml` file is already configured to load variables from the `.env` file.

### Example `.env` File

Below is an example of a `.env` file configuration. Ensure you replace the placeholder values with your actual credentials:

```
GITHUB_TOKEN=
# FastAPI-Mail configuration for Gmail
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
SMTP_RECIPIENTS=
```

This file should be placed in the root directory of the project. The application will load these values automatically when starting the services.

---

## Project Structure
```
.
├── backend/                # FastAPI backend
│   ├── app/               # Application code
│   ├── Dockerfile         # Backend Dockerfile
│   └── requirements.txt   # Python dependencies
├── db/                    # Database migrations
├── frontend/              # React frontend
│   ├── src/               # Source code
│   ├── Dockerfile         # Frontend Dockerfile
│   └── package.json       # Node.js dependencies
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # Project documentation
```

---

## Future Enhancements
- Add authentication and authorization.
- Optimize database queries for better performance.
- Enhance the dashboard with more visualizations.

---

## License
This project is licensed under the MIT License.

---

## AI Usage Summary

This project leverages AI tools to streamline development and enhance functionality:

- **Frontend Development**:
  - React components were designed and optimized with AI assistance.
  - TailwindCSS was integrated for responsive and modern UI design.
- **Backend Development**:
  - FastAPI endpoints were structured with AI-generated templates.
  - CORS and middleware configurations were debugged with AI support.
- **Dockerization**:
  - Dockerfiles for both frontend and backend were created with AI guidance.
  - Docker Compose setup was optimized for seamless service orchestration.
- **Documentation**:
  - README files were generated with AI assistance.

AI tools were instrumental in accelerating development, debugging, and documentation processes, ensuring a robust and efficient application.

---

## Setting Up Alerts for Failed Workflows

To receive alerts for failed workflows, we used **ngrok** to expose the backend service and set it up as a GitHub webhook. Follow these steps to configure it:

1. **Install ngrok**:
   - Download and install ngrok from [ngrok's official website](https://ngrok.com/download).

2. **Expose the Backend Service**:
   - Run the following command to expose the backend service:
     ```bash
     ngrok http 8000
     ```
   - Note the public URL generated by ngrok (e.g., `https://<random-subdomain>.ngrok.io`).

3. **Set Up GitHub Webhook**:
   - Go to your GitHub repository settings.
   - Navigate to **Webhooks** and click **Add webhook**.
   - Use the ngrok public URL as the **Payload URL**, appending `/webhook` (e.g., `https://<random-subdomain>.ngrok.io/webhook`).
   - Set the **Content type** to `application/json`.
   - Select **Let me select individual events** and choose `Workflow runs`.
   - Save the webhook.

4. **Test the Webhook**:
   - Trigger a workflow in your GitHub repository.
   - Check the backend logs to verify that the webhook payload is received.

5. **Configure Alerts**:
   - Ensure the backend is configured to send email alerts for failed workflows using the `.env` variables for SMTP settings.

This setup allows you to receive real-time alerts whenever a workflow fails in your GitHub repository.
