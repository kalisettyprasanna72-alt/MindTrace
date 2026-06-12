"""Model evaluation, metrics, and plots for fatigue detector."""

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score


LABEL_NAMES = ["Low", "Medium", "High"]


def evaluate_model(name: str, model, X_test, y_test) -> dict:
	"""
	Print for the given model:
	  - Accuracy score
	  - Classification report with labels ['Low','Medium','High']
	  - Confusion matrix using seaborn heatmap (save as <name>_confusion.png)
	Return dict: {
	  "name": name,
	  "accuracy": float,
	  "f1_low": float,
	  "f1_medium": float,
	  "f1_high": float
	}
	"""
	y_pred = model.predict(X_test)

	acc = float(accuracy_score(y_test, y_pred))
	print(f"Model: {name}")
	print(f"Accuracy: {acc:.4f}")

	print("Classification Report:")
	# classification_report default labels are 0,1,2 — provide target_names
	print(classification_report(y_test, y_pred, target_names=LABEL_NAMES))

	cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])
	plt.figure(figsize=(6, 4))
	sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=LABEL_NAMES, yticklabels=LABEL_NAMES)
	plt.xlabel("Predicted")
	plt.ylabel("Actual")
	plt.title(f"Confusion Matrix: {name}")
	plt.tight_layout()
	fname = f"{name}_confusion.png"
	plt.savefig(fname, bbox_inches="tight")
	plt.close()

	f1s = f1_score(y_test, y_pred, labels=[0, 1, 2], average=None)

	return {
		"name": name,
		"accuracy": acc,
		"f1_low": float(f1s[0]),
		"f1_medium": float(f1s[1]),
		"f1_high": float(f1s[2]),
	}


def evaluate_all(models: Dict[str, object], X_test, y_test) -> pd.DataFrame:
	"""
	Run evaluate_model() for each model in dict.
	Return a DataFrame comparison table:
	  columns = ['Model', 'Accuracy', 'F1-Low', 'F1-Medium', 'F1-High']
	Print the table at the end.
	"""
	rows = []
	for name, model in models.items():
		res = evaluate_model(name, model, X_test, y_test)
		rows.append([
			res["name"],
			res["accuracy"],
			res["f1_low"],
			res["f1_medium"],
			res["f1_high"],
		])

	df = pd.DataFrame(rows, columns=["Model", "Accuracy", "F1-Low", "F1-Medium", "F1-High"])
	print("\nModel comparison:")
	print(df)
	return df


def plot_feature_importance(rf_model, feature_names: list) -> None:
	"""
	Plot top 10 feature importances from Random Forest.
	Horizontal bar chart, sorted descending.
	Save as feature_importance.png.
	"""
	if not hasattr(rf_model, "feature_importances_"):
		raise ValueError("Provided model does not have feature_importances_ attribute")

	importances = np.array(rf_model.feature_importances_)
	if len(importances) != len(feature_names):
		raise ValueError("Length of feature_names does not match feature_importances_")

	inds = np.argsort(importances)[::-1][:10]
	top_feats = [feature_names[i] for i in inds]
	top_imps = importances[inds]

	plt.figure(figsize=(8, 6))
	sns.barplot(x=top_imps, y=top_feats, orient="h")
	plt.xlabel("Importance")
	plt.title("Top 10 Feature Importances")
	plt.tight_layout()
	plt.savefig("feature_importance.png", bbox_inches="tight")
	plt.close()
