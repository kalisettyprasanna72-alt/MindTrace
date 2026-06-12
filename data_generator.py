"""Synthetic student data generation for fatigue detector."""

# Feature schema documents expected feature names, types and ranges.
FEATURE_SCHEMA = {
	"sleep_duration":          {"type": float, "range": (2, 12)},
	"sleep_quality":           {"type": int,   "range": (0, 4)},
	"screen_time_hours":       {"type": float, "range": (0, 16)},
	"pre_sleep_screen":        {"type": int,   "range": (0, 3)},
	"study_hours_per_day":     {"type": float, "range": (0, 16)},
	"study_break_pattern":     {"type": int,   "range": (0, 3)},
	"stress_score":            {"type": int,   "range": (1, 10)},
	"anxiety_episodes":        {"type": int,   "range": (0, 10)},
	"exercise_minutes":        {"type": int,   "range": (0, 120)},
	"activity_type":           {"type": int,   "range": (0, 3)},
	"water_intake_liters":     {"type": float, "range": (0.5, 5)},
	"meal_regularity":         {"type": int,   "range": (0, 3)},
	"mood_score":              {"type": int,   "range": (1, 10)},
	"irritability_level":      {"type": int,   "range": (0, 3)},
	"focus_span_minutes":      {"type": int,   "range": (5, 90)},
	"distraction_frequency":   {"type": int,   "range": (0, 3)},
	"caffeine_drinks_per_day": {"type": int,   "range": (0, 10)},
	"energy_drink_use":        {"type": int,   "range": (0, 3)},
	"break_time_hours":        {"type": float, "range": (0, 8)},
	"social_support_level":    {"type": int,   "range": (0, 3)},
}

# Target/label information
TARGET_COLUMN = "fatigue_level"
# Mapping: 0=Low, 1=Medium, 2=High
TARGET_MAPPING = {0: "Low", 1: "Medium", 2: "High"}

import numpy as np
import pandas as pd


def generate_data(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
	"""Generate synthetic student records with realistic fatigue correlations.

	Returns a DataFrame containing the 20 features defined in `FEATURE_SCHEMA`
	and a `fatigue_level` column (0=Low, 1=Medium, 2=High).
	"""
	rng = np.random.RandomState(random_state)

	# Sample features according to their schema
	data = {}
	for name, spec in FEATURE_SCHEMA.items():
		low, high = spec["range"]
		if spec["type"] is int:
			# include upper bound
			data[name] = rng.randint(int(low), int(high) + 1, size=n_samples)
		else:
			data[name] = rng.uniform(float(low), float(high), size=n_samples)

	# Convert to arrays for vectorized penalty computation
	sleep_duration = data["sleep_duration"]
	sleep_quality = data["sleep_quality"]
	screen_time_hours = data["screen_time_hours"]
	pre_sleep_screen = data["pre_sleep_screen"]
	study_hours_per_day = data["study_hours_per_day"]
	study_break_pattern = data["study_break_pattern"]
	stress_score = data["stress_score"]
	anxiety_episodes = data["anxiety_episodes"]
	exercise_minutes = data["exercise_minutes"]
	activity_type = data["activity_type"]
	water_intake_liters = data["water_intake_liters"]
	meal_regularity = data["meal_regularity"]
	mood_score = data["mood_score"]
	irritability_level = data["irritability_level"]
	focus_span_minutes = data["focus_span_minutes"]
	distraction_frequency = data["distraction_frequency"]
	caffeine_drinks_per_day = data["caffeine_drinks_per_day"]
	energy_drink_use = data["energy_drink_use"]
	break_time_hours = data["break_time_hours"]
	social_support_level = data["social_support_level"]

	# Base score (lower is less fatigued). Penalties increase fatigue score.
	base_score = 30.0

	penalties = (
		np.maximum(0, (8 - sleep_duration) * 3)
		+ (sleep_quality * 3)
		+ np.maximum(0, (screen_time_hours - 4) * 1.5)
		+ (pre_sleep_screen * 2)
		+ np.maximum(0, (study_hours_per_day - 5) * 1.5)
		+ (study_break_pattern * 2.5)
		+ (stress_score * 2)
		+ (anxiety_episodes * 1.5)
		+ np.maximum(0, (60 - exercise_minutes) / 10)
		+ (activity_type * 1.5)
		+ np.maximum(0, (2.5 - water_intake_liters) * 2)
		+ (meal_regularity * 2)
		+ np.maximum(0, (10 - mood_score) * 1.2)
		+ (irritability_level * 2)
		+ np.maximum(0, (45 - focus_span_minutes) / 8)
		+ (distraction_frequency * 1.5)
		+ np.maximum(0, (caffeine_drinks_per_day - 2) * 1.2)
		+ (energy_drink_use * 2)
		+ np.maximum(0, (3 - break_time_hours) * 1.5)
		+ (social_support_level * 1.2)
	)

	noise = rng.normal(0, 3, size=n_samples)

	fatigue_score = base_score + penalties + noise
	fatigue_score = np.clip(fatigue_score, 0, 100)

	# Map to discrete fatigue levels
	fatigue_level = np.where(fatigue_score <= 35, 0, np.where(fatigue_score <= 65, 1, 2)).astype(int)

	# Build DataFrame
	df = pd.DataFrame(data)
	df[TARGET_COLUMN] = fatigue_level
	return df

