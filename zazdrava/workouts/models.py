from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Record(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="records"
    )
    data = models.JSONField()
    timestamp = models.DateTimeField()
    position_lat = models.FloatField(blank=True, null=True)
    position_long = models.FloatField(blank=True, null=True)
    gps_accuracy = models.IntegerField(blank=True, null=True)
    enhanced_altitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    enhanced_speed = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    battery_soc = models.FloatField(blank=True, null=True)
    ascent = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Record at {self.timestamp}"


class Session(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="sessions"
    )
    event = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    start_time = models.DateTimeField()
    total_elapsed_time = models.FloatField()
    total_timer_time = models.FloatField()
    enhanced_avg_speed = models.FloatField(blank=True, null=True)
    avg_speed = models.FloatField(blank=True, null=True)
    enhanced_max_speed = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)
    total_distance = models.FloatField()
    min_heart_rate = models.IntegerField(blank=True, null=True)
    avg_heart_rate = models.IntegerField(blank=True, null=True)
    max_heart_rate = models.IntegerField(blank=True, null=True)
    total_calories = models.IntegerField()
    total_ascent = models.FloatField()
    total_descent = models.FloatField()
    sport = models.CharField(max_length=100)
    sub_sport = models.CharField(max_length=100)
    num_laps = models.IntegerField(blank=True, null=True)
    threshold_power = models.IntegerField(blank=True, null=True)
    auto_lap_duration = models.FloatField(blank=True, null=True)


class Lap(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="laps")
    event = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    start_time = models.DateTimeField()
    total_elapsed_time = models.FloatField()
    total_timer_time = models.FloatField()
    avg_speed = models.FloatField()
    max_speed = models.FloatField()
    total_distance = models.FloatField()
    avg_heart_rate = models.IntegerField(blank=True, null=True)
    max_heart_rate = models.IntegerField(blank=True, null=True)
    total_calories = models.IntegerField()
    total_ascent = models.FloatField()
    total_descent = models.FloatField()


class HRZone(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="hr_zones"
    )
    message_index = models.IntegerField()
    high_bpm = models.IntegerField()


class PowerZone(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="power_zones"
    )
    message_index = models.IntegerField()
    high_value = models.IntegerField()
