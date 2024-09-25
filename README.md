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

### Cloning the Repository

First, clone this repository:

```bash
git clone https://github.com/yourusername/alacademy.git
cd alacademy
