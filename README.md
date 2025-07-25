# 🔗 URL Shortener

A simple and efficient URL Shortener built with **Node.js**, **Express.js**, and **MongoDB**. This application allows users to convert long URLs into short, shareable links and redirect them back to the original link.

## 🚀 Features

- 🔒 Generate unique short URLs
- 📥 Store original URLs in MongoDB
- 🔁 Redirect short URLs to the original link
- 🧾 API-based architecture for easy integration
- 📊 Click count tracking *(optional enhancement)*

## 🛠️ Tech Stack

- **Backend:** Node.js, Express.js
- **Database:** MongoDB (with Mongoose ODM)
- **Environment Management:** dotenv
- **Other Dependencies:** nanoid, cors, body-parser

## 📂 Project Structure

Url-Shortner/
├── models/
│ └── Url.js # Mongoose model for URL schema
├── routes/
│ └── url.js # API routes for shortening and redirecting
├── .env # Environment variables
├── server.js # Main server file
├── package.json
└── README.md # Project documentation

bash
Copy
Edit

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kunal141206/Url-Shortner.git
cd Url-Shortner
2. Install Dependencies
bash
Copy
Edit
npm install
3. Configure Environment Variables
Create a .env file in the root directory and add:

env
Copy
Edit
PORT=5000
MONGODB_URI=your_mongodb_connection_string
BASE_URL=http://localhost:5000
4. Run the Application
bash
Copy
Edit
npm start
Server will be running at http://localhost:5000.

📡 API Endpoints
POST /api/url/shorten
Description: Create a short URL.

Request Body:

json
Copy
Edit
{
  "longUrl": "https://www.example.com/very/long/url"
}
Response:

json
Copy
Edit
{
  "shortUrl": "http://localhost:5000/xyz123"
}
GET /:shortCode
Description: Redirects to the original URL based on the short code.

Example:
Visit http://localhost:5000/xyz123 → redirects to the original long URL.

🧠 Future Enhancements
Add a frontend UI with analytics dashboard

Track click counts and user geolocation

Add QR code generation

Implement user authentication for custom URLs

🧑‍💻 Author
Kunal Rathore

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
