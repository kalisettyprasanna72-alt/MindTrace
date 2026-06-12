"""Fatigue prediction function using best trained model."""

from typing import Any

import numpy as np

from .preprocessor import preprocess_single


LABEL_MAP = {0: "Low Fatigue", 1: "Medium Fatigue", 2: "High Fatigue"}


def predict_fatigue(
	student_data: dict,
	model: Any,
	scaler
) -> str:
	"""
	Takes a dict with all 20 feature keys.
	Preprocesses using preprocess_single() from preprocessor.py.
	Returns one of: 'Low Fatigue', 'Medium Fatigue', 'High Fatigue'.
	Also prints the predicted class and predicted probabilities for all 3 classes.
	"""
	X = preprocess_single(student_data, scaler)

	if hasattr(model, "predict_proba"):
		probs = model.predict_proba(X)[0]
	else:
		# fallback when predict_proba not available
		pred = int(model.predict(X)[0])
		probs = np.zeros(len(LABEL_MAP), dtype=float)
		probs[pred] = 1.0

	pred_class = int(np.argmax(probs))
	print(f"Predicted class: {LABEL_MAP[pred_class]} ({pred_class})")
	print("Predicted probabilities:")
	for i in sorted(LABEL_MAP.keys()):
		print(f"  {LABEL_MAP[i]}: {probs[i]:.4f}")

	return LABEL_MAP[pred_class]


TEST_STUDENT = {
	"sleep_duration": 5.0, "sleep_quality": 3,
	"screen_time_hours": 9.0, "pre_sleep_screen": 3,
	"study_hours_per_day": 10.0, "study_break_pattern": 3,
	"stress_score": 9, "anxiety_episodes": 6,
	"exercise_minutes": 10, "activity_type": 3,
	"water_intake_liters": 1.0, "meal_regularity": 2,
	"mood_score": 3, "irritability_level": 3,
	"focus_span_minutes": 15, "distraction_frequency": 3,
	"caffeine_drinks_per_day": 6, "energy_drink_use": 2,
	"break_time_hours": 0.5, "social_support_level": 3
}
