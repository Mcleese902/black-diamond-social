# Black Diamond Therapy

Black Diamond Therapy is a desktop application developed using Python and PyQt5, designed to provide anonymous , locally run Mental Health & Addictions counseling sessions to users by communicating with the Ollama server they have running on their device . ( Check out ollama.ai ) BDT incorporates a clean and easy to use Chat UI for counseling sessions , a task management system & we are beginning to incorporate a social hub of sorts for users to take advantage of . We hope to use this to offer a new feature " Group sessions " where like minded users can join workshops or group sessions to empower one another , learn and teach . 

## Features

- User Registration and Login
- User Profiles with Profile Picture, Bio, Signature, and Social Links
- Real-time Chat using Ollama API
- Task Management System
- News Feed for Status Updates
- Friends and Co-Workers Lists

## Installation

### Prerequisites

- Python 3.x
- PyQt5
- SQLite3
- Git (for version control)

### Step-by-Step Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/black-diamond-therapy.git
   cd black-diamond-therapy

   Create a Virtual Environment


python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

python setup_database.py

python main.py


*****  This is still a very early-stage that I am using as a learning project more then anything else . Any help / thoughts / suggestions are welcome @ amacleod@blackdiamondtherapy.ca .
