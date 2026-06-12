"""ML model definitions and training for fatigue detector."""

from typing import Dict

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC


def get_random_forest() -> RandomForestClassifier:
	"""Return RandomForestClassifier(n_estimators=100, random_state=42)"""
	return RandomForestClassifier(n_estimators=100, random_state=42)


def get_gradient_boosting() -> GradientBoostingClassifier:
	"""Return GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)"""
	return GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)


def get_svm() -> SVC:
	"""Return SVC(kernel='rbf', C=1.0, probability=True, random_state=42)"""
	return SVC(kernel='rbf', C=1.0, probability=True, random_state=42)


def train_all_models(X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, object]:
	"""
	Train all 3 models on X_train, y_train.
	Return dict: {"Random Forest": model, "Gradient Boosting": model, "SVM": model}
	Print 'Training <name>...' before each fit.
	"""
	models = {
		"Random Forest": get_random_forest(),
		"Gradient Boosting": get_gradient_boosting(),
		"SVM": get_svm(),
	}

	for name, model in models.items():
		print(f"Training {name}...")
		model.fit(X_train, y_train)

	return models

