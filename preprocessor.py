"""Feature scaling and train/test split for fatigue detector."""

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from .data_generator import FEATURE_SCHEMA, TARGET_COLUMN


FLOAT_FEATURES = [
	"sleep_duration",
	"screen_time_hours",
	"study_hours_per_day",
	"water_intake_liters",
	"break_time_hours",
]


def preprocess(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, StandardScaler]:
	"""
	Split features and target, scale float features, split train/test.
	Returns: X_train, X_test, y_train, y_test, scaler
	- Use StandardScaler on FLOAT_FEATURES only
	- Train/test split: 80/20, random_state=42, stratify=y
	"""
	feature_names = list(FEATURE_SCHEMA.keys())

	X = df[feature_names].copy()
	y = df[TARGET_COLUMN].copy()

	scaler = StandardScaler()
	# fit_transform float features on full dataset before split to avoid leakage,
	# but per instruction typically we should fit on training set — here we fit on training set after split.

	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.2, random_state=42, stratify=y
	)

	# Fit scaler on training float features and transform both sets
	scaler.fit(X_train[FLOAT_FEATURES])
	X_train.loc[:, FLOAT_FEATURES] = scaler.transform(X_train[FLOAT_FEATURES])
	X_test.loc[:, FLOAT_FEATURES] = scaler.transform(X_test[FLOAT_FEATURES])

	return X_train, X_test, y_train, y_test, scaler


def preprocess_single(student_data: dict, scaler: StandardScaler) -> np.ndarray:
	"""
	Preprocess a single student dict for prediction.
	Apply the same StandardScaler to FLOAT_FEATURES.
	Return a 2D numpy array (1 row, 20 columns) in correct feature order.
	"""
	feature_names = list(FEATURE_SCHEMA.keys())

	# Build single-row DataFrame in correct order
	row = {name: student_data.get(name, np.nan) for name in feature_names}
	df = pd.DataFrame([row], columns=feature_names)

	# Apply scaler to float features
	df.loc[:, FLOAT_FEATURES] = scaler.transform(df[FLOAT_FEATURES])

	return df[feature_names].to_numpy()
