import pandas as pd
import seaborn as sns
#from sklearn.pipeline import Pipeline

from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import KFold, cross_validate, GridSearchCV
from sklearn.metrics import fbeta_score, make_scorer

RANDOM_STATE = 42

def build_classification_model_pipeline(
    classifier,
    preprocessor=None,
    feature_selector=None,
    sampler=None
):
    """
    Builds a classification pipeline, optionally including a preprocessor and feature selector.

    Args:
        classifier: A classification estimator.
        preprocessor: Optional preprocessing pipeline.
        feature_selector: Optional feature selector (e.g., SelectFromModel, RFE, etc.).
        sampler:  Optional sampling

    Returns:
        model: Pipeline.
    """
    steps = []

    if preprocessor is not None:
        steps.append(("preprocessor", preprocessor))
    
    if feature_selector is not None:
        steps.append(("feature_selector", feature_selector))

    if sampler is not None:
        steps.append(("sampler", sampler))
    
    steps.append(("clf", classifier))

    pipeline = Pipeline(steps)
    return pipeline
    

def train_and_validate_classification_model(
    X,
    y,
    cv,
    classifier,
    preprocessor=None,
    feature_selector=None,
    sampler=None,
    multi_class=False,
    beta=2
):
    model = build_classification_model_pipeline(
        classifier=classifier,
        preprocessor=preprocessor,
        feature_selector=feature_selector,
        sampler=sampler
    )

    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "f1": "f1_weighted" if multi_class else "f1",
        "precision": "precision_weighted" if multi_class else "precision",
        "recall": "recall_weighted" if multi_class else "recall",
        "roc_auc": "roc_auc_ovr" if multi_class else "roc_auc",
        "average_precision": "average_precision",
        "f2_score": make_scorer(fbeta_score, beta=beta, average='weighted' if multi_class else 'binary')
    }

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=scoring,
    )

    return scores

def grid_search_cv_classifier(
    classifier,
    param_grid,
    cv,
    preprocessor=None,
    return_train_score=False,
    refit_metric="roc_auc",
    multi_class=False,
    beta=2  # Beta parameter for fbeta_score
):
    """
    Performs grid search (GridSearchCV) to optimize classifier hyperparameters.

    Args:
        classifier: A classification estimator.
        param_grid: Dictionary of hyperparameters to search.
        cv: Cross-validation strategy.
        preprocessor: Optional preprocessing pipeline.
        return_train_score: If True, includes training scores in the results. Default is False.
        refit_metric: Metric used to refit the best model. Default is "roc_auc".
        multi_class: Whether the task is multi-class. Default is False.
        beta: Beta value for the fbeta_score. Default is 2.

    Returns:
        grid_search: Fitted `GridSearchCV` object.
    """
    model = build_classification_model_pipeline(classifier, preprocessor)

    # Create the scorer for fbeta_score
    fbeta_scorer = make_scorer(fbeta_score, beta=beta, average='weighted' if multi_class else 'binary')

    # Define scoring metrics
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "f1": "f1_weighted" if multi_class else "f1",
        "precision": "precision_weighted" if multi_class else "precision",
        "recall": "recall_weighted" if multi_class else "recall",
        "roc_auc": "roc_auc_ovr" if multi_class else "roc_auc",
        "average_precision": "average_precision",
        "f2_score": fbeta_scorer
    }

    grid_search = GridSearchCV(
        model,
        cv=cv,
        param_grid=param_grid,
        scoring=scoring,
        refit=refit_metric,
        n_jobs=-1,
        return_train_score=return_train_score,
        verbose=1,
    )

    return grid_search

def organize_cv_results(results):
    """
    Organizes cross-validation results into a formatted DataFrame.

    Adds total execution time (fit + score) and transforms the dictionary of results
    into an expanded DataFrame with one row per fold.

    Args:
        results: Dictionary containing results from cross_validate or GridSearch.

    Returns:
        expanded_results_df: DataFrame with organized and expanded results by fold.
    """
    for key, value in results.items():
        results[key]["time_seconds"] = (
            results[key]["fit_time"] + results[key]["score_time"]
        )

    results_df = (
        pd.DataFrame(results).T.reset_index().rename(columns={"index": "model"})
    )

    expanded_results_df = results_df.explode(
        results_df.columns[1:].to_list()
    ).reset_index(drop=True)

    try:
        expanded_results_df = expanded_results_df.apply(pd.to_numeric)
    except ValueError:
        pass

    return expanded_results_df