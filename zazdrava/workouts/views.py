import gzip, os, fitparse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workout, Record
from .forms import WorkoutUploadForm


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
    workout, created = Workout.objects.get_or_create(name=workout_name)
    print("We made it so far!!!!!!!!!!!")
    print(workout)
    # Ensure Workout exists
    for record in fit_data.get_messages("record"):
        record_data = {}
        timestamp = None

        for field in record:
            print(type(field))
            if field.name and field.value is not None:
                if field.name == "timestamp":
                    timestamp = field.value
                else:
                    record_data[field.name] = field.value

        if timestamp:
            records.append(
                Record(workout=workout, timestamp=timestamp, data=record_data)
            )

    Record.objects.bulk_create(records)


# @login_required
def view_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    records = Record.objects.filter(workout=workout)
    return render(
        request, "workout_detail.html", {"workout": workout, "records": records}
    )


# @login_required
def dashboard(request):
    workouts = Workout.objects.all
    return render(request, "dashboard.html", {"workouts": workouts})
