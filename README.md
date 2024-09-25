# Booking System

## Project Description

Alacademy Booking System is a web application developed with Django that allows users to book equipment and spaces. The system supports booking management, status notifications, and expiration checks. It is designed for use in educational institutions and organizations that want to streamline the booking process for resources.

## Features

- Equipment and space booking with specified start and end times.
- Notifications about booking status (active, completed, expired).
- Expiration checks for active bookings.

## Technologies

- Django 5.1.1
- PostgreSQL
- Django REST Framework
- Celery (for background task processing)
- Redis (as the message broker for Celery)

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

### Cloning the Repository

First, clone this repository:

```bash
git clone https://github.com/yourusername/alacademy.git
cd alacademy
