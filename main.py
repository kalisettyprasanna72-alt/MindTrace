"""Main pipeline runner for Student Mental Fatigue Detector."""

if __name__ == "__main__":
	from .data_generator import generate_data, TARGET_COLUMN
	from .preprocessor import preprocess
	from .models import train_all_models
	from .evaluator import evaluate_all, plot_feature_importance
	from .predictor import predict_fatigue, TEST_STUDENT

	# Step 1: generate data
	df = generate_data(n_samples=1000)
	print("Dataset shape:", df.shape)
	print("Class distribution:\n", df["fatigue_level"].value_counts())

	# Step 2: preprocess
	X_train, X_test, y_train, y_test, scaler = preprocess(df)
	print("Train size:", X_train.shape, "Test size:", X_test.shape)

	# Step 3: train models
	trained_models = train_all_models(X_train, y_train)

	# Step 4: evaluate
	results_df = evaluate_all(trained_models, X_test, y_test)
	print(results_df)

	# Step 5: plot feature importance — derive feature names from DataFrame to ensure exact order
	feature_names = [c for c in df.columns if c != TARGET_COLUMN]
	try:
		plot_feature_importance(trained_models["Random Forest"], feature_names)
	except Exception as e:
		print("Could not plot feature importance:", e)

	# Step 6: pick best model by accuracy
	best_row = results_df.loc[results_df["Accuracy"].idxmax()]
	best_name = best_row["Model"]
	best_model = trained_models[best_name]

	# Step 7: sample prediction
	result = predict_fatigue(TEST_STUDENT, best_model, scaler)
	print("\n=== SAMPLE PREDICTION ===")
	print("Predicted Fatigue Level:", result)
	print("\n✓ Fatigue Detector pipeline complete.")
