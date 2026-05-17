# Flask Application Configuration

import os
from datetime import timedelta
from pathlib import Path

# ============================================================================
# Application Configuration Base
# ============================================================================

class Config:
    """Base configuration."""
    
    # Application Settings
    FLASK_APP = "server.py"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False
    
    # API Configuration
    API_TITLE = "SDN AI Congestion Control API"
    API_VERSION = "1.0.0"
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
    CORS_MAX_AGE = 3600
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "/var/log/sdn-ai/backend.log")
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Model Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "../ai/models/model.pkl")
    LSTM_INPUT_SHAPE = 5
    DQN_HIDDEN_SIZE = 128
    
    # Caching Configuration
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv("RATELIMIT_ENABLED", "True").lower() == "true"
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    
    # Thresholds
    CONGESTION_THRESHOLD = 0.7
    BANDWIDTH_WARNING_THRESHOLD = 80  # Percentage
    PACKET_DROP_THRESHOLD = 5  # Percentage
    
    # Feature Scaling
    FEATURE_SCALING = os.getenv("FEATURE_SCALING", "minmax")
    
    # Timeouts
    PREDICTION_TIMEOUT = 5  # seconds
    REQUEST_TIMEOUT = 30  # seconds
    
    # API Keys (if authentication enabled)
    API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "False").lower() == "true"


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"
    
    # Allow all origins in development
    CORS_ORIGINS = "*"
    
    # Disable caching in development
    CACHE_ENABLED = False
    
    # Disable rate limiting in development
    RATELIMIT_ENABLED = False
    
    # Relaxed timeouts for debugging
    PREDICTION_TIMEOUT = 30


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
    # Disable caching for tests
    CACHE_ENABLED = False
    
    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False
    
    # Use in-memory model for testing
    MODEL_PATH = "tests/fixtures/mock_model.pkl"


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    
    # Restrict CORS in production
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://yourdomain.com")
    
    # Enable caching in production
    CACHE_ENABLED = True
    CACHE_TTL = 7200  # 2 hours
    
    # Enable rate limiting in production
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per day, 20 per hour"
    
    # Require valid API keys
    API_KEY_REQUIRED = True
    
    # Longer timeouts
    PREDICTION_TIMEOUT = 10
    REQUEST_TIMEOUT = 60
    
    # Ensure critical variables are set
    @staticmethod
    def validate_config():
        """Validate required production configuration."""
        required = [
            "SECRET_KEY",
            "MODEL_PATH",
            "CORS_ORIGINS",
            "LOG_FILE",
            "CACHE_REDIS_URL"
        ]
        
        for var in required:
            if not os.getenv(var):
                raise ValueError(f"Missing required environment variable: {var}")


# ============================================================================
# Configuration Selection
# ============================================================================

def get_config():
    """Get configuration based on environment."""
    env = os.getenv("FLASK_ENV", "development").lower()
    
    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    
    config_class = configs.get(env, DevelopmentConfig)
    
    # Validate production config
    if env == "production":
        config_class.validate_config()
    
    return config_class


# ============================================================================
# Configuration Initialization
# ============================================================================

def load_config(app):
    """Load configuration into Flask app."""
    config = get_config()
    app.config.from_object(config)
    
    return config


# ============================================================================
# Model Configuration
# ============================================================================

class ModelConfig:
    """Machine Learning Model Configuration."""
    
    # LSTM Configuration
    LSTM = {
        "input_shape": 5,
        "hidden_units": 128,
        "num_layers": 2,
        "dropout": 0.2,
        "activation": "relu",
        "optimizer": "adam",
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 50,
        "validation_split": 0.2,
    }
    
    # DQN Configuration
    DQN = {
        "state_size": 10,
        "action_size": 8,
        "hidden_size": 256,
        "learning_rate": 0.0005,
        "gamma": 0.99,  # Discount factor
        "epsilon_start": 1.0,
        "epsilon_end": 0.01,
        "epsilon_decay": 0.995,
        "buffer_size": 100000,
        "batch_size": 64,
        "update_frequency": 1000,
    }
    
    # Feature Scaling Configuration
    SCALING = {
        "method": "minmax",  # or "standard", "robust"
        "feature_ranges": {
            "bandwidth": (0, 1000),  # Mbps
            "rtt": (0, 100),  # ms
            "drop_rate": (0, 100),  # %
            "queue_length": (0, 1000),  # packets
            "inter_arrival": (0, 10),  # ms
        }
    }


# ============================================================================
# Data Configuration
# ============================================================================

class DataConfig:
    """Data and Dataset Configuration."""
    
    # Dataset paths
    DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "ai", "dataset")
    TRAIN_DATA = os.path.join(DATASET_DIR, "train_data.csv")
    TEST_DATA = os.path.join(DATASET_DIR, "test_data.csv")
    VALIDATION_DATA = os.path.join(DATASET_DIR, "validation_data.csv")
    
    # Data characteristics
    FEATURES = ["bandwidth", "rtt", "drop_rate", "queue_length", "inter_arrival"]
    TARGET = "congested"
    
    # Data processing
    SEQUENCE_LENGTH = 10  # Lookback window
    PREDICTION_HORIZON = 3  # Predict 3 seconds ahead
    
    # Missing value handling
    HANDLE_MISSING = "mean"  # or "forward_fill", "drop"
    
    # Outlier handling
    OUTLIER_METHOD = "iqr"  # or "zscore", "isolation_forest"
    OUTLIER_THRESHOLD = 3  # IQR multiplier or z-score threshold


# ============================================================================
# API Configuration
# ============================================================================

class APIConfig:
    """REST API Endpoint Configuration."""
    
    # Endpoint versions
    API_VERSION = "v1"
    BASE_URL = f"/api/{API_VERSION}"
    
    # Endpoints
    ENDPOINTS = {
        "health": "/health",
        "predict": "/predict",
        "stats": "/stats",
        "config": "/config",
        "route": "/route",
    }
    
    # Response settings
    JSON_SORT_KEYS = False
    JSON_INDENT = 2  # In development, set to None for production
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Timeouts
    RESPONSE_TIMEOUT = 30  # seconds


# ============================================================================
# Monitoring Configuration
# ============================================================================

class MonitoringConfig:
    """Monitoring and Observability Configuration."""
    
    # Metrics collection
    METRICS_ENABLED = os.getenv("METRICS_ENABLED", "True").lower() == "true"
    METRICS_PORT = int(os.getenv("METRICS_PORT", 8000))
    
    # Health check interval
    HEALTH_CHECK_INTERVAL = 30  # seconds
    
    # Metric retention
    METRICS_RETENTION = 24 * 3600  # 24 hours in seconds
    
    # Alert thresholds
    ALERTS = {
        "prediction_latency_ms": 100,  # Alert if > 100ms
        "error_rate": 0.05,  # Alert if > 5%
        "memory_usage_mb": 512,  # Alert if > 512MB
        "cpu_usage_percent": 80,  # Alert if > 80%
    }


# ============================================================================
# Configuration Utilities
# ============================================================================

def validate_config():
    """Validate all configuration values."""
    config = get_config()
    
    # Check model path exists
    if not os.path.exists(config.MODEL_PATH):
        print(f"Warning: Model file not found at {config.MODEL_PATH}")
    
    # Check log directory exists
    log_dir = os.path.dirname(config.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    
    # Validate numeric thresholds
    if not (0 <= config.CONGESTION_THRESHOLD <= 1):
        raise ValueError("CONGESTION_THRESHOLD must be between 0 and 1")
    
    if not (0 <= config.BANDWIDTH_WARNING_THRESHOLD <= 100):
        raise ValueError("BANDWIDTH_WARNING_THRESHOLD must be between 0 and 100")
    
    if not (0 <= config.PACKET_DROP_THRESHOLD <= 100):
        raise ValueError("PACKET_DROP_THRESHOLD must be between 0 and 100")
    
    print("✅ Configuration validation passed")


if __name__ == "__main__":
    validate_config()
