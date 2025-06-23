import os


from .models import RANDOM_STATE

os.environ["OMP_NUM_THREADS"] = "9" #evitar o warning do kmeans

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.colors import ListedColormap
from matplotlib.ticker import PercentFormatter

from matplotlib.ticker import EngFormatter
from sklearn.metrics import PredictionErrorDisplay

from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.metrics import silhouette_score,  make_scorer


sns.set_theme(palette="bright")

PALETTE = "coolwarm"
SCATTER_ALPHA = 0.2




def pairplot(
    dataframe, columns, hue_column=None, alpha=0.5, corner=True, palette="tab10"
):
    """
    
    Function to generate a pairplot.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame containing the data.
    columns : List[str]
        List of column names (strings) to be used.
    hue_column : str, optional
        Column to be used for hue coloring, by default None.
    alpha : float, optional
        Transparency value, by default 0.5.
    corner : bool, optional
        If True, displays only the lower triangle of the pairplot; otherwise, shows the full plot. Default is True.
    palette : str, optional
        Color palette to be used, by default "tab10".
    """
    analysis = columns.copy() + [hue_column]

    sns.pairplot(
        dataframe[analysis],
        diag_kind="kde",
        hue=hue_column,
        plot_kws=dict(alpha=alpha),
        corner=corner,
        palette=palette,
    )


def plot_elbow_silhouette(X, random_state=42, range_k=(2, 11)):
    """
    Generates plots for the Elbow and Silhouette methods.
    
    Parameters
    ----------
    X : pandas.DataFrame
        DataFrame containing the data.
    random_state : int, optional
        Seed value to ensure reproducibility, by default 42.
    range_k : tuple, optional
        Range of cluster values to evaluate, by default (2, 11).
    """

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5), tight_layout=True)

    elbow = {}
    silhouette = []

    k_range = range(*range_k)

    for i in k_range:
        kmeans = KMeans(n_clusters=i, random_state=random_state, n_init=10)
        kmeans.fit(X)
        elbow[i] = kmeans.inertia_

        labels = kmeans.labels_
        silhouette.append(silhouette_score(X, labels))

    sns.lineplot(x=list(elbow.keys()), y=list(elbow.values()), ax=axs[0])
    axs[0].set_xlabel("K")
    axs[0].set_xlabel("Inertia")
    axs[0].set_title("Elbow Method")

    sns.lineplot(x=list(k_range), y=silhouette, ax=axs[1])
    axs[1].set_xlabel("K")
    axs[1].set_xlabel("Silhouette Score")
    axs[1].set_title("Silhouette Method")

    plt.show()


def plot_clusters_2D(
    dataframe,
    columns,
    n_colors,
    centroids,
    show_centroids=True,
    show_points=False,
    column_clusters=None,
):
    """Generates a 2D plot of the clusters.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame containing the data.
    columns : List[str]
        List of column names (strings) to be used.
    n_colors : int
        Number of colors for the plot.
    centroids : np.ndarray
        Array containing the centroids.
    show_centroids : bool, optional
        Whether to display the centroids in the plot, by default True.
    show_points : bool, optional
        Whether to display the data points in the plot, by default False.
    column_clusters : List[int], optional
        Column containing the cluster numbers to color the points (if show_points is True), by default None.
    """


    fig = plt.figure()

    ax = fig.add_subplot(111)

    cores = plt.cm.tab10.colors[:n_colors]
    cores = ListedColormap(cores)

    x = dataframe[columns[0]]
    y = dataframe[columns[1]]

    ligar_centroids = show_centroids
    ligar_pontos = show_points

    for i, centroid in enumerate(centroids):
        if ligar_centroids:
            ax.scatter(*centroid, s=500, alpha=0.5)
            ax.text(
                *centroid,
                f"{i}",
                fontsize=20,
                horizontalalignment="center",
                verticalalignment="center",
            )

        if ligar_pontos:
            s = ax.scatter(x, y, c=column_clusters, cmap=cores)
            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.3, 1))

    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_title("Clusters")

    plt.show()

def plot_columns_percent_by_cluster(
    dataframe,
    columns,
    rows_cols=(2, 3),
    figsize=(15, 8),
    column_cluster="cluster",
):
    """Function to generate bar plots showing the percentage of each value per cluster.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame containing the data.
    columns : List[str]
        List of column names (strings) to be used.
    rows_cols : tuple, optional
        Tuple with the number of rows and columns in the grid layout, by default (2, 3).
    figsize : tuple, optional
        Tuple with the figure width and height, by default (15, 8).
    column_cluster : str, optional
        Name of the column containing the cluster numbers, by default "cluster".
    """
    fig, axs = plt.subplots(
        nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True
    )

    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)

    for ax, col in zip(axs.flatten(), columns):
        h = sns.histplot(
            x=column_cluster,
            hue=col,
            data=dataframe,
            ax=ax,
            multiple="fill",
            stat="percent",
            discrete=True,
            shrink=0.8,
        )

        n_clusters = dataframe[column_cluster].nunique()
        h.set_xticks(range(n_clusters))
        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel("")
        h.tick_params(axis="both", which="both", length=0)

        # Adiciona rótulos nas barras
        for bars in h.containers:
            h.bar_label(
                bars,
                label_type="center",
                labels=[f"{b.get_height():.1%}" for b in bars],
                color="white",
                weight="bold",
                fontsize=11,
            )

        # Remove bordas das barras
        for bar in h.patches:
            bar.set_linewidth(0)

        # --- LEGENDA CENTRALIZADA NO TOPO ---
        # Pega handles e labels do subplot atual
        legend= h.get_legend()
        legend.remove()

        # Pegar os handles e labels de um dos subplots para criar a legenda única
        labels = [text.get_text() for text in legend.get_texts()]
        
        # Adicionar uma única legenda centralizada no topo
        h.legend(handles = legend.legend_handles, labels=labels, loc='upper center', ncols= dataframe[col].nunique(), bbox_to_anchor=(0.5, 1.25), title=col)

    # Ajusta espaçamento entre subplots
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.show()

def plot_columns_percent_hue_cluster(
    dataframe,
    columns,
    rows_cols=(2, 3),
    figsize=(15, 8),
    column_cluster="cluster",
    palette="tab10",
):
    """Function to generate bar plots showing the percentage of each value with clusters as hue.
    
    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame containing the data.
    columns : List[str]
        List of column names (strings) to be used.
    rows_cols : tuple, optional
        Tuple with the number of rows and columns in the grid layout, by default (2, 3).
    figsize : tuple, optional
        Tuple with the figure width and height, by default (15, 8).
    column_cluster : str, optional
        Name of the column containing the cluster numbers, by default "cluster".
    palette : str, optional
        Color palette to be used, by default "tab10".
    """
    fig, axs = plt.subplots(
        nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True
    )

    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)

    for ax, col in zip(axs.flatten(), columns):
        h = sns.histplot(
            x=col,
            hue=column_cluster,
            data=dataframe,
            ax=ax,
            multiple="fill",
            stat="percent",
            discrete=True,
            shrink=0.8,
            palette=palette,
        )

        if dataframe[col].dtype != "object":
            h.set_xticks(range(dataframe[col].nunique()))

        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel("")
        h.tick_params(axis="both", which="both", length=0)

        for bars in h.containers:
            h.bar_label(
                bars,
                label_type="center",
                labels=[f"{b.get_height():.1%}" for b in bars],
                color="white",
                weight="bold",
                fontsize=11,
            )

        for bar in h.patches:
            bar.set_linewidth(0)

        legend = h.get_legend()
        legend.remove()

    labels = [text.get_text() for text in legend.get_texts()]

    fig.legend(
        handles=legend.legend_handles,
        labels=labels,
        loc="upper center",
        ncols=dataframe[column_cluster].nunique(),
        title="Clusters",
        bbox_to_anchor=(0.5, 1.1)
    )

    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    plt.show()

def plot_coefficients(df_coefs, title="Coefficients"):
    """
    Plots horizontal bar chart of model coefficients.

    Parameters:
    df_coefs (pd.DataFrame): DataFrame containing the model coefficients.
    title (str): Title of the plot.
    """
    plt.figure(figsize=(30, 20))
    df_coefs.plot.barh()
    plt.title(title)
    plt.axvline(x=0, color=".5")
    plt.xlabel("Coefficients")
    plt.gca().get_legend().remove()
    plt.show()

def plot_residuals(y_true, y_pred):
    """
    Plots residual analysis using histogram, residuals vs predicted, and actual vs predicted.

    Parameters:
    y_true (array-like): True target values.
    y_pred (array-like): Predicted target values.
    """
    residuals = y_true - y_pred

    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    sns.histplot(residuals, kde=True, ax=axes[0])

    PredictionErrorDisplay.from_predictions(
        y_true=y_true, y_pred=y_pred, kind="residual_vs_predicted", ax=axes[1]
    )

    PredictionErrorDisplay.from_predictions(
        y_true=y_true, y_pred=y_pred, kind="actual_vs_predicted", ax=axes[2]
    )

    plt.tight_layout()
    plt.show()
    
def plot_residuals_from_estimator(estimator, X, y, use_eng_formatter=False, sample_fraction=0.25):
    """
    Plots residual analysis for a fitted estimator using residuals vs predicted, actual vs predicted, and histogram.

    Parameters:
    estimator (estimator object): A fitted estimator with `predict` method.
    X (array-like): Features used for prediction.
    y (array-like): True target values.
    use_eng_formatter (bool): Whether to format axes using engineering notation.
    sample_fraction (float): Fraction of data to subsample for scatter plots.
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    display_residuals = PredictionErrorDisplay.from_estimator(
        estimator,
        X,
        y,
        kind="residual_vs_predicted",
        ax=axes[1],
        random_state=RANDOM_STATE,
        scatter_kwargs={"alpha": SCATTER_ALPHA},
        subsample=sample_fraction,
    )

    PredictionErrorDisplay.from_estimator(
        estimator,
        X,
        y,
        kind="actual_vs_predicted",
        ax=axes[2],
        random_state=RANDOM_STATE,
        scatter_kwargs={"alpha": SCATTER_ALPHA},
        subsample=sample_fraction,
    )

    residuals = display_residuals.y_true - display_residuals.y_pred
    sns.histplot(residuals, kde=True, ax=axes[0])

    if use_eng_formatter:
        for ax in axes:
            ax.yaxis.set_major_formatter(EngFormatter())
            ax.xaxis.set_major_formatter(EngFormatter())

    plt.tight_layout()
    plt.show()

def plot_compare_model_metrics(results_df):
    """
    Plots boxplots comparing various evaluation metrics across different models.

    Args:
        results_df: DataFrame containing model evaluation metrics (e.g., from cross-validation),
                    including columns such as 'model', 'test_accuracy', 'test_f1', etc.

    Displays:
        A grid of boxplots for each metric, comparing performance across models.
    """
    fig, axs = plt.subplots(4, 2, figsize=(9, 9), sharex=True)

    comparison_metrics = [
        "time_seconds",
        "test_accuracy",
        "test_balanced_accuracy",
        "test_f1",
        "test_precision",
        "test_recall",
        "test_roc_auc",
        "test_average_precision",
    ]

    metric_names = [
        "Time (s)",
        "Accuracy",
        "Balanced Accuracy",
        "F1 Score",
        "Precision",
        "Recall",
        "AUROC",
        "AUPRC",
    ]

    for ax, metric, name in zip(axs.flatten(), comparison_metrics, metric_names):
        sns.boxplot(
            x="model",
            y=metric,
            data=results_df,
            ax=ax,
            showmeans=True,
        )
        ax.set_title(name)
        ax.set_ylabel(name)
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.show()
