# GymLog

GymLog is a web-based fitness tracking application developed with Python and Flask as part of a school project. It allows users to record and manage workouts, track performance metrics, and monitor their fitness progress through a responsive web interface.

The project also focused on professional software development practices, including requirements analysis, project planning, technical documentation, UML modeling, and system design. This provided practical experience in combining software engineering with structured project management.

<div>
  <img src="https://github.com/user-attachments/assets/11ee1142-a447-43c5-949c-4a6fd80cf5f2" width="49%" />
  <img src="https://github.com/user-attachments/assets/695a09ea-e726-4a12-a863-edbd86af1f38" width="49%" />
</div>

# Structure

GymLog was designed with a modular architecture to ensure maintainability, scalability, and a clear separation of responsibilities. Instead of placing all business logic inside Flask routes, the application follows a service-oriented structure where database access, business logic, and presentation logic are separated into dedicated components. The class diagram is intended to provide more details here.

## Class diagram

<img width="2000" height="711" alt="image" src="https://github.com/user-attachments/assets/fa3fce79-e63d-4d26-9bdc-4cbde4995271" />

## Authentication

GymLog uses a session-based authentication system. During login, the application verifies that the user exists and validates the provided credentials. After successful authentication, user information is stored in the current Flask session, allowing personalized access to workouts, statistics, and other features.

```python
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        if not (
            db_user_service.user_exists(email=request.form["email"])
            and db_user_service.authenticate_user(email=request.form["email"], password=request.form["password"])
        ):
            return render_template("auth/login.html", login_error=True)

        user_data = db_user_service.get_user(email=request.form["email"])
        session["user_id"] = user_data["user_id"]
        session["user_name"] = user_data["first_name"]

        return redirect(url_for("pages.overview_page"))

    return render_template("auth/login.html")
```

## Sequence diagram

The sequence diagram illustrates the workflow of creating a new workout. When a user saves a workout, the `CreateWorkout` component coordinates the process and delegates all database operations to the `DBCreateService`.

First, the workout itself is created and a unique `workout_id` is returned. Afterwards, the associated exercises and exercise sets are created and linked to the workout. This diagram demonstrates the interaction between the business logic layer and the database layer while highlighting the modular architecture of the application.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ea814ef1-b572-42d2-af36-86cec5144af3" alt="Sequence Diagram" width="600">
</p>

# License

This project is intended for learning and personal use. Feel free to use and experiment.
