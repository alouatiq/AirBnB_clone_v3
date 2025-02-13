# AirBnB Clone - RESTful API (Version 3)

The console was the first segment of the AirBnB project, but this version focuses on building a RESTful API using Flask to enable communication between the front-end and back-end of the application.

#### Functionalities of this RESTful API:
* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database, etc.
* Perform operations on objects (count, compute stats, etc.)
* Update attributes of an object
* Destroy an object

## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Example API Endpoints](#example-api-endpoints)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 20.04 LTS using Python 3.4.3.

## Installation
* Clone this repository:  
  ```bash
  git clone "https://github.com/alouatiq/AirBnB_clone_v3.git"
  ```
* Access AirBnB directory:  
  ```bash
  cd AirBnB_clone_v3
  ```
* Install dependencies:  
  ```bash
  pip3 install -r requirements.txt
  ```
* Run the Flask API:  
  ```bash
  python3 -m api.v1.app
  ```

## File Descriptions
The API is structured to handle multiple endpoints and interactions with resources.

[api/v1/app.py](api/v1/app.py) - The main entry point for running the Flask application.  
[api/v1/views/](/api/v1/views/) - This directory contains route definitions and request handling logic for different API endpoints.

### `models/` directory contains classes
- `base_model.py` - Defines the base class for all models.
- `user.py` - Handles user-related data.
- `place.py` - Manages information related to places.
- `review.py` - Handles reviews and feedback.
- `state.py` - Stores state-related data.
- `city.py` - Contains city-specific information.
- `amenity.py` - Manages amenities available at different places.

## Example API Endpoints
- **Get all places**  
  ```http
  GET /api/v1/places
  ```
- **Create a new user**  
  ```http
  POST /api/v1/users
  ```
- **Retrieve a specific user**  
  ```http
  GET /api/v1/users/<user_id>
  ```
- **Update a user**  
  ```http
  PUT /api/v1/users/<user_id>
  ```
- **Delete a user**  
  ```http
  DELETE /api/v1/users/<user_id>
  ```

## Bugs
No known bugs at this time.

## Authors
- **Hassan AL OUATIQ** - [GitHub](https://github.com/alouatiq)
- **Anas AATEF** - [GitHub](https://github.com/Anas2018EMI)

## License
Public Domain. No copyright protection.
