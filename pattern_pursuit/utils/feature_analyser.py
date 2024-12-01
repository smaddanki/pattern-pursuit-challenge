import json
import logging
import os
from typing import Any, Dict, Optional, Union

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image


class DataLoader:
    """Handle loading different data types"""

    @staticmethod
    def load_data(
        data_path: str, data_type: str
    ) -> Union[pd.DataFrame, dict, Image.Image, gpd.GeoDataFrame]:
        if data_type == "pandas":
            if data_path.endswith(".csv"):
                return pd.read_csv(data_path)
            elif data_path.endswith(".parquet"):
                return pd.read_parquet(data_path)
        elif data_type == "json":
            with open(data_path, "r") as f:
                return json.load(f)
        elif data_type == "image":
            return Image.open(data_path)
        elif data_type == "geojson":
            return gpd.read_file(data_path)
        raise ValueError(f"Unsupported data type: {data_type}")


class FeatureAnalyzer:
    """Main class for feature analysis and EDA"""

    def __init__(self, data_path: str, data_type: str):
        self.data_loader = DataLoader()
        self.data = self.data_loader.load_data(data_path, data_type)
        self.data_type = data_type
        self.analysis_results = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("FeatureAnalyzer")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def analyze_data_quality(self) -> Dict:
        """Analyze data quality based on data type"""
        self.logger.info("Starting data quality analysis")
        quality_metrics = {}

        if self.data_type == "pandas":
            quality_metrics = self._analyze_pandas_quality()
        elif self.data_type == "json":
            quality_metrics = self._analyze_json_quality()
        elif self.data_type == "image":
            quality_metrics = self._analyze_image_quality()
        elif self.data_type == "geojson":
            quality_metrics = self._analyze_geospatial_quality()

        self.analysis_results["quality_metrics"] = quality_metrics
        return quality_metrics

    def _analyze_pandas_quality(self) -> Dict:
        """Analyze quality metrics for pandas DataFrame"""
        df = self.data
        metrics = {
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "data_types": df.dtypes.to_dict(),
            "unique_counts": df.nunique().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
        }
        return metrics

    def _analyze_json_quality(self) -> Dict:
        """Analyze quality metrics for JSON data"""

        def count_nulls(obj):
            if isinstance(obj, dict):
                return sum(count_nulls(v) for v in obj.values())
            elif isinstance(obj, list):
                return sum(count_nulls(item) for item in obj)
            return 1 if obj is None else 0

        metrics = {
            "total_nulls": count_nulls(self.data),
            "structure_depth": self._get_json_depth(self.data),
            "size_bytes": len(json.dumps(self.data)),
        }
        return metrics

    def _analyze_image_quality(self) -> Dict:
        """Analyze quality metrics for image data"""
        img = np.array(self.data)
        metrics = {
            "dimensions": img.shape,
            "mean_brightness": np.mean(img),
            "std_brightness": np.std(img),
            "is_grayscale": len(img.shape) == 2
            or (len(img.shape) == 3 and img.shape[2] == 1),
            "file_size": (
                os.path.getsize(self.data.filename)
                if hasattr(self.data, "filename")
                else None
            ),
        }
        return metrics

    def _analyze_geospatial_quality(self) -> Dict:
        """Analyze quality metrics for geospatial data"""
        gdf = self.data
        metrics = {
            "crs": str(gdf.crs),
            "geometry_types": gdf.geometry.type.value_counts().to_dict(),
            "bounds": gdf.total_bounds.tolist(),
            "null_geometries": gdf.geometry.isna().sum(),
        }
        return metrics

    def perform_univariate_analysis(self) -> Dict:
        """Perform univariate analysis based on data type"""
        self.logger.info("Starting univariate analysis")
        univariate_stats = {}

        if self.data_type == "pandas":
            univariate_stats = self._analyze_pandas_univariate()
        elif self.data_type == "json":
            univariate_stats = self._analyze_json_univariate()
        elif self.data_type == "image":
            univariate_stats = self._analyze_image_univariate()
        elif self.data_type == "geojson":
            univariate_stats = self._analyze_geospatial_univariate()

        self.analysis_results["univariate_stats"] = univariate_stats
        return univariate_stats

    def _analyze_pandas_univariate(self) -> Dict:
        """Univariate analysis for pandas DataFrame"""
        df = self.data
        stats = {}

        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                stats[column] = {
                    "mean": df[column].mean(),
                    "median": df[column].median(),
                    "std": df[column].std(),
                    "skew": df[column].skew(),
                    "kurtosis": df[column].kurtosis(),
                }
            else:
                stats[column] = {
                    "unique_values": df[column].nunique(),
                    "top_values": df[column].value_counts().head().to_dict(),
                }
        return stats

    def perform_bivariate_analysis(self, target_column: Optional[str] = None) -> Dict:
        """Perform bivariate analysis based on data type"""
        self.logger.info("Starting bivariate analysis")
        bivariate_stats = {}

        if self.data_type == "pandas":
            bivariate_stats = self._analyze_pandas_bivariate(target_column)
        elif self.data_type == "image":
            bivariate_stats = self._analyze_image_bivariate()
        elif self.data_type == "geojson":
            bivariate_stats = self._analyze_geospatial_bivariate()

        self.analysis_results["bivariate_stats"] = bivariate_stats
        return bivariate_stats

    def _analyze_pandas_bivariate(self, target_column: Optional[str]) -> Dict:
        """Bivariate analysis for pandas DataFrame"""
        df = self.data
        stats = {}

        if target_column:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col != target_column:
                    correlation = df[col].corr(df[target_column])
                    stats[col] = {"correlation_with_target": correlation}

        # Correlation matrix for all numeric columns
        corr_matrix = df.select_dtypes(include=[np.number]).corr()
        stats["correlation_matrix"] = corr_matrix.to_dict()

        return stats

    def generate_visualizations(self, output_dir: str):
        """Generate visualizations based on data type"""
        self.logger.info("Generating visualizations")
        os.makedirs(output_dir, exist_ok=True)

        if self.data_type == "pandas":
            self._generate_pandas_visualizations(output_dir)
        elif self.data_type == "image":
            self._generate_image_visualizations(output_dir)
        elif self.data_type == "geojson":
            self._generate_geospatial_visualizations(output_dir)

    def _generate_pandas_visualizations(self, output_dir: str):
        """Generate visualizations for pandas DataFrame"""
        df = self.data

        # Distribution plots for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x=col, kde=True)
            plt.title(f"Distribution of {col}")
            plt.savefig(f"{output_dir}/{col}_distribution.png")
            plt.close()

        # Correlation heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_dir}/correlation_heatmap.png")
        plt.close()

    def generate_report(self, output_path: str):
        """Generate comprehensive analysis report"""
        self.logger.info("Generating analysis report")

        report = {
            "data_type": self.data_type,
            "analysis_timestamp": pd.Timestamp.now().isoformat(),
            "quality_metrics": self.analysis_results.get("quality_metrics", {}),
            "univariate_stats": self.analysis_results.get("univariate_stats", {}),
            "bivariate_stats": self.analysis_results.get("bivariate_stats", {}),
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=4)

    @staticmethod
    def _get_json_depth(obj: Any, depth: int = 0) -> int:
        """Helper method to get JSON structure depth"""
        if isinstance(obj, dict):
            if not obj:
                return depth
            return max(
                FeatureAnalyzer._get_json_depth(v, depth + 1) for v in obj.values()
            )
        elif isinstance(obj, list):
            if not obj:
                return depth
            return max(FeatureAnalyzer._get_json_depth(item, depth + 1) for item in obj)
        return depth


# Example usage
if __name__ == "__main__":
    # Example for pandas DataFrame
    analyzer = FeatureAnalyzer("data.csv", "pandas")
    analyzer.analyze_data_quality()
    analyzer.perform_univariate_analysis()
    analyzer.perform_bivariate_analysis(target_column="target")
    analyzer.generate_visualizations("output/visualizations")
    analyzer.generate_report("output/analysis_report.json")
