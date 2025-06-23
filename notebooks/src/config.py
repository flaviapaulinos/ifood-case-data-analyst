from pathlib import Path
PROJECT_FOLDER = Path(__file__).resolve().parents[2]
REPORTS_FOLDER = PROJECT_FOLDER  / "reports"

DATA_FOLDER = PROJECT_FOLDER / "data"
IMAGES_FOLDER = REPORTS_FOLDER / "images"
MODELS_FOLDER = PROJECT_FOLDER / "models"


ORIGINAL_DATA = DATA_FOLDER / "ml_project1_data.csv"
SCALED_DATA = DATA_FOLDER / "ml_project1_data_scaled.parquet"
TREATED_DATA = DATA_FOLDER / "ml_project1_data_treated.parquet"
CLUSTERED_DATA = DATA_FOLDER /  "ml_project1_data_clustered.parquet"
DADOS_PCA_SCALED = DATA_FOLDER /  "ml_project1_data_pca.parquet"

REPORT = REPORTS_FOLDER / "00-fbps-eda.html"
MODEL_CLUSTERING = MODELS_FOLDER / "modelo_clustering.pkl"
PCA_MODEL = MODELS_FOLDER / "modelo_pca_clustering.pkl"
CLASSIFICATION_MODEL = MODELS_FOLDER / "modelo_class.pkl"




