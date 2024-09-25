# Booking System

## Project Description

Alacademy Booking System is a web application developed with Django that allows users to book equipment and spaces. The system supports booking management, status notifications, and expiration checks. It is designed for use in educational institutions and organizations that want to streamline the booking process for resources.

## Features

- Equipment and space booking with specified start and end times.
- Notifications about booking status (active, completed, expired).
- Expiration checks for active bookings.
- Queues for managing booking statuses: `active`, `completed`, and `expired` statuses are automatically updated.

## Technologies

- Django 5.1.1
- PostgreSQL
- Django REST Framework
- Celery (for background task processing)
- Redis (as the message broker for Celery)
- Sentry (for error tracking and monitoring)

## Installation

### Requirements

Make sure you have the following components installed:

- Python 3.10 or higher
- PostgreSQL
- Redis

### Running Celery

In a separate terminal, you will need to start Celery. Use the following commands:

1. **Start Celery Worker**:

    ```bash
    celery -A alacademy worker --pool=solo
    ```

    This command starts a Celery worker that processes tasks. The `--pool=solo` option is useful for debugging in a development environment, as it runs the worker in a single-threaded mode.

2. **Start Celery Beat**:

    ```bash
    celery -A alacademy beat
    ```

    This command starts the Celery Beat scheduler, which sends tasks to the Celery worker at scheduled intervals. This is necessary for tasks like checking booking statuses periodically.

### Queue System for Booking Status

The booking system automatically updates the statuses of bookings using Celery and Redis queues. The following queues are used:

- **Active Queue**: Processes bookings that are currently active, sending notifications and managing resources.
- **Completed Queue**: Once a booking's end time is reached, it moves to the `completed` queue, marking it as completed and notifying users.
- **Expired Queue**: Checks bookings that were supposed to be active but have passed without completion, marking them as expired.

Celery Beat schedules these tasks to run at specific intervals to keep the booking statuses updated.

### Setting Up Sentry

To enable error tracking and monitoring with Sentry, follow these steps:

1. Install the Sentry SDK:

    ```bash
    pip install sentry-sdk
    ```

2. Configure Sentry in your Django `settings.py` file:

    ```python
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="DSN",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
    ```

3. Test Sentry integration by triggering an error in your application. You can use a test URL (e.g., `/sentry-debug/`) that raises an exception to verify that Sentry captures errors correctly.

## API Endpoints

The system provides a set of REST API endpoints to interact with the booking system. Below is a list of the main endpoints available:

### Booking Endpoints

1. **List All Resources**

    - **URL**: `/resources/`
    - **Method**: `GET`
    - **Description**: Retrieves a list of all available resources for booking.
    - **Response Example**:
        ```json
        [
            [
                {
                    "id": 1,
                    "name": "Conference Room A",
                    "max_slots": 4
                },
                {
                    "id": 2,
                    "name": "Tennis Court 1",
                    "max_slots": 2
                },
                {
                    "id": 3,
                    "name": "Projector",
                    "max_slots": 1
                }
            ]
        ]
        ```

2. **List All Bookings**

    - **URL**: `/bookings/`
    - **Method**: `GET`
    - **Description**: Retrieves a list of all bookings with their statuses.
    - **Response Example**:
        ```json
        [
            {
                "id": 1,
                "resource": "Conference Room",
                "start_time": "2024-09-25T10:00:00Z",
                "end_time": "2024-09-25T12:00:00Z",
                "status": "active"
            },
            {
                "id": 2,
                "resource": "Projector",
                "start_time": "2024-09-25T14:00:00Z",
                "end_time": "2024-09-25T16:00:00Z",
                "status": "completed"
            },
           {
                "id": 3,
                "resource": "Conference Room",
                "start_time": "2024-09-25T11:00:00Z",
                "end_time": "2024-09-25T14:00:00Z",
                "status": "queue"
            }
        ]
        ```

3. **Create a New Booking**

    - **URL**: `/bookings/create/`
    - **Method**: `POST`
    - **Description**: Creates a new booking for a specified resource.
    - **Request Body Example**:
        ```json
        {
            "resource": 1,
            "user": 3,
            "start_time": "2024-09-26T10:00:00Z",
            "end_time": "2024-09-26T12:00:00Z"
        }
        ```
    - **Response Example**:
        ```json
        {
            "id": 3,
            "resource": "Projector",
            "start_time": "2024-09-26T10:00:00Z",
            "end_time": "2024-09-26T12:00:00Z",
            "status": "active",
            "user": 3,
            "resource": 1
        }
        ```

4. **Cancel a Booking**

    - **URL**: `/bookings/cancel/<int:booking_id>/`
    - **Method**: `POST`
    - **Description**: Cancels an active booking based on the booking ID.
    - **Response Example**:
        ```json
        {
            "message": "Booking cancelled and next user notified."
        }
        ```

### API Documentation

Swagger and Redoc are available for testing and exploring the API.

- **Swagger UI**: `/api/docs/`
- **Redoc**: `/api/docs/redoc/`
- **OpenAPI Schema**: `/api/schema/`


### Cloning the Repository

First, clone this repository:

```bash
git clone https://github.com/yourusername/alacademy.git
cd alacademy
