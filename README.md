
# Social Networking API

This project is an API for a social networking application built using Django Rest Framework. The application supports functionalities such as user login/signup, searching for users, managing friend requests, and listing friends. The application is containerized using Docker.




## Features

• User Signup/Login

• Search for users by email or name

• Send/Accept/Reject friend requests

• List friends

• List pending friend requests


## Installation

### Using Docker
Clone the repository:

```bash
git clone <repository-url>
cd social_networking_api
```

Build and run the Docker container:

```bash
docker-compose up --build
```

Run database migrations:

```bash
docker-compose exec web python manage.py migrate
```

Create a superuser (for accessing the admin panel):

```bash
docker-compose exec web python manage.py createsuperuser
```

Access the application:

API: [http://localhost:8000/api/](http://localhost:8000/api/)

Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Without Docker

Clone the repository:

```bash
git clone <repository-url>
cd social_networking_api
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Access the application:

API: [http://localhost:8000/api/](http://localhost:8000/api/)

Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## API Reference

#### Register 

```http
POST /api/register/
```

#### Login

```http
POST /api/login/
```

#### Send Friend Request
```http
POST /api/friend-request/
```
#### Pending Friend Requests
```http
GET /api/friend-request/
```
#### Get User's Friends List
```http
GET /api/friend-request/friends/
```

#### Reject Friend Request
```http
POST /api/friend-request/reject/
```

#### Search User
```http
GET /api/search-user/?q='keyword'
```


## Constraints

• Can only send 3 Friend Request per minute.
