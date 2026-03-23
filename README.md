🏢 ACME Tenant Portal

A web-based tenant portal designed to streamline communication and workflow management between tenants and property managers.

🚀 Overview

Property management workflows are often fragmented — tenants report issues via messages or calls, while managers track them across spreadsheets or disconnected tools. This leads to delays, lack of visibility, and inefficient coordination.

This project addresses that by providing a centralised platform where tenants can submit and track requests, and property managers can manage, prioritise, and respond in a structured way.

🎯 Problem Statement

In typical property management systems:

Maintenance requests are handled manually
Communication is scattered across channels
There is limited visibility into the request status
Tracking and prioritisation are inconsistent

This creates friction for both tenants and managers.

💡 Solution

The ACME Tenant Portal introduces a single source of truth for tenant–manager interactions.

Key capabilities:
Tenants can submit and track maintenance requests
Managers can view, prioritise, and update requests
Structured workflows replace manual coordination
Clear visibility into request status for all users
🧭 User Flow
Tenant logs into the portal
Tenant submits a maintenance request
The request is stored and becomes visible to the manager
Manager reviews, updates, and resolves the request
Tenant receives status updates

This flow is designed to minimise friction while maintaining transparency.

🛠️ Tech Stack

(Update this based on your actual implementation)

Frontend

React / Next.js
Tailwind CSS

Backend

Node.js / Express

Database

PostgreSQL / MongoDB

Deployment

Railway

Tools

GitHub for version control
Cursor / ChatGPT for development support
🧠 Key Technical Decisions
1. Scalable Structure

The backend is designed to support multiple users and properties, allowing the system to scale without major restructuring.

2. Clear Data Modelling

Requests are structured with status, timestamps, and ownership, enabling efficient tracking and updates.

3. Separation of Concerns

Frontend and backend responsibilities are clearly divided, improving maintainability and extensibility.

4. Rapid Deployment

Railway was used to deploy and test the application in a live environment quickly.

⚙️ Running the Project Locally
# Clone the repository
git clone https://github.com/harshmay/acme-tenant-portal.git

# Navigate into the project
cd acme-tenant-portal

# Install dependencies
npm install

# Run the development server

👉 http://web-production-46f49.up.railway.app


🔍 Future Improvements
Real-time notifications (e.g. WebSockets)
Role-based access control
File/image uploads for maintenance requests
Analytics dashboard for property managers
Mobile responsiveness improvements
📄 Additional Notes

As part of this assessment, AI tools such as Claude and Cursor were used to assist with development, debugging, and refining implementation approaches. Full interaction logs have been provided separately for transparency.

🤝 Closing

This project reflects my approach to building practical, user-focused systems — combining clean design, structured workflows, and scalable architecture.
