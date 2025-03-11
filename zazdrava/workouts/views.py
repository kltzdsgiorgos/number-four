import gzip, os, fitparse
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workout, Record
from .forms import WorkoutUploadForm

import plotly.express as px
import pandas as pd
import plotly.io as pio


@login_required
def upload_workout(request):
    if request.method == "POST":
        form = WorkoutUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            workout_name = uploaded_file.name  # Use filename as workout name

            file = default_storage.save(
                f"fit_files/{uploaded_file.name}", ContentFile(uploaded_file.read())
            )

            if uploaded_file.name.endswith(".gz"):
                decompressed_path = file.replace(".gz", "")
                with gzip.open(default_storage.path(file), "rb") as f_in, open(
                        default_storage.path(decompressed_path), "wb"
                ) as f_out:
                    f_out.write(f_in.read())
                os.remove(default_storage.path(file))
                file = decompressed_path

            handle_fit_file(default_storage.path(file), workout_name)

            return redirect("workouts:dashboard")
    else:
        form = WorkoutUploadForm()
    return render(request, "upload.html", {"form": form})

def handle_fit_file(file, workout_name):
    """Extracts data from FIT file and saves it to the database under a workout."""
    fit_data = fitparse.FitFile(file)
    records = []
    workout, _ = Workout.objects.get_or_create(name=workout_name)

    for record in fit_data.get_messages("record"):
        record_data = {}
        record_fields = {
            "timestamp": None,
            "position_lat": None,
            "position_long": None,
            "gps_accuracy": None,
            "enhanced_altitude": None,
            "altitude": None,
            "grade": None,
            "distance": None,
            "heart_rate": None,
            "calories": None,
            "enhanced_speed": None,
            "speed": None,
            "battery_soc": None,
            "ascent": None,
        }

        for field in record:
            if field.name and field.value is not None:
                if isinstance(field.value, datetime):
                    record_data[field.name] = field.value.isoformat()
                else:
                    record_data[field.name] = field.value

                if field.name in record_fields:
                    record_fields[field.name] = field.value

        if record_fields["timestamp"]:
            records.append(
                Record(
                    workout=workout,
                    timestamp=record_fields["timestamp"],
                    position_lat=record_fields["position_lat"],
                    position_long=record_fields["position_long"],
                    gps_accuracy=record_fields["gps_accuracy"],
                    enhanced_altitude=record_fields["enhanced_altitude"],
                    altitude=record_fields["altitude"],
                    grade=record_fields["grade"],
                    distance=record_fields["distance"],
                    heart_rate=record_fields["heart_rate"],
                    calories=record_fields["calories"],
                    enhanced_speed=record_fields["enhanced_speed"],
                    speed=record_fields["speed"],
                    battery_soc=record_fields["battery_soc"],
                    ascent=record_fields["ascent"],
                    data=record_data,
                )
            )

    Record.objects.bulk_create(records)



@login_required
def view_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    records = Record.objects.filter(workout=workout)
    return render(
        request, "workout_detail.html", {"workout": workout, "records": records}
    )

@login_required
def dashboard(request):
    workouts = Workout.objects.all
    return render(request, "dashboard.html", {"workouts": workouts})


def fit_data_view(request):
    """Display only the workout chart."""
    workouts = Workout.objects.prefetch_related("records").all()

    if not workouts.exists():
        return render(
            request,
            "zazdrava/fit_data.html",
            {"charts": "<p>No workout data available.</p>"},
        )

    # Process data
    data = []
    for workout in workouts:
        for record in workout.records.all():  # ✅ Corrected attribute access
            data.append(
                {
                    "timestamp": record.timestamp,
                    "speed": record.data.get("speed", 0),
                    "workout": workout.name,
                }
            )

    df = pd.DataFrame(data)

    # Create the Plotly chart
    fig = px.line(
        df, x="timestamp", y="speed", color="workout", title="Workout Speed Over Time"
    )
    chart_html = fig.to_html(full_html=False)

    return render(request, "zazdrava/fit_data.html", {"charts": chart_html})
