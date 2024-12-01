# Infrastructure Setup - Pattern Pursuit Challenge

## System Configuration
- **Hardware**: Mac Studio M2
- **Memory**: 32GB Shared Memory
- **Architecture**: ARM64 (Apple Silicon)
- **Storage**: Minimum 100GB recommended for development environment

## Infrastructure Components

### Data Processing & Streaming
1. **Apache Kafka**
   - Purpose: Real-time market data streaming and event processing
   - Configuration: 
     - 3 broker setup
     - Deployed in K3d cluster
     - Topics for: raw market data, processed signals, model predictions
   - Resource Allocation: 4GB memory per broker

2. **Apache Spark**
   - Purpose: Batch processing and feature engineering
   - Configuration:
     - Standalone mode for development
     - K3d deployment for production
     - Native ARM64 support
   - Resource Allocation: 8GB memory for driver, 4GB per executor

3. **ClickHouse**
   - Purpose: High-performance analytics and time-series storage
   - Configuration:
     - Single node setup
     - Optimized for time-series queries
     - Materialized views for real-time aggregations
   - Resource Allocation: 8GB memory

### Model Development & Serving

4. **MLflow**
   - Purpose: Model tracking, versioning, and deployment
   - Configuration:
     - Tracking server with Minio backend
     - Model registry enabled
     - Experiment tracking for each day's models
   - Resource Allocation: 2GB memory

5. **Seldon Core**
   - Purpose: Model serving and deployment
   - Configuration:
     - Deployed on K3d
     - REST API endpoints
     - Model monitoring enabled
   - Resource Allocation: 2GB per model server

### Orchestration & Storage

6. **Docker**
   - Purpose: Containerization of all services
   - Configuration:
     - BuildKit enabled
     - ARM64 base images
     - Custom networks for service isolation
   - Resource Allocation: Variable based on containers

7. **K3d (Kubernetes)**
   - Purpose: Container orchestration
   - Configuration:
     - Single master node
     - 2 worker nodes
     - Local registry enabled
     - Resource limits enforced
   - Resource Allocation: 12GB total cluster

8. **Apache Airflow**
   - Purpose: Workflow orchestration
   - Configuration:
     - LocalExecutor for development
     - KubernetesExecutor for production
     - DAGs for daily model training and evaluation
   - Resource Allocation: 4GB memory

9. **MinIO**
   - Purpose: Object storage for models and datasets
   - Configuration:
     - Single node setup
     - Multiple buckets for different data types
     - Versioning enabled
   - Resource Allocation: 2GB memory

10. **Redis**
    - Purpose: Caching and real-time feature store
    - Configuration:
      - Single node setup
      - Persistence enabled
      - Key expiration policies
    - Resource Allocation: 2GB memory

## Network Configuration
```
+----------------+     +------------------+     +-------------------+
|  Data Ingestion|     |  Processing Layer|     |  Serving Layer    |
|  (Kafka)       | --> |  (Spark)         | --> |  (Seldon)         |
+----------------+     +------------------+     +-------------------+
        |                      |                         |
        v                      v                         v
+----------------+     +------------------+     +-------------------+
|  Storage Layer |     |  Model Training  |     |  Monitoring       |
|  (ClickHouse,  |     |  (MLflow)        |     |  (Prometheus)    |
|   MinIO)       |     |                  |     |                  |
+----------------+     +------------------+     +-------------------+
```

## Resource Management
Total Memory Allocation (Peak): ~28GB
- Data Processing: 12GB
- Model Training: 8GB
- Storage Systems: 4GB
- Orchestration: 4GB

## Development Workflow
1. Local Development:
   - JupyterLab for model development
   - Docker Compose for service management
   - K3d for Kubernetes workloads

2. Data Pipeline:
   - Kafka → Spark → ClickHouse for real-time
   - Airflow orchestrated batch processing
   - MinIO for model artifacts and datasets

3. Model Deployment:
   - MLflow for tracking and versioning
   - Seldon for serving
   - Redis for feature serving

## Security Considerations
- Network isolation using Docker networks
- K3d RBAC enabled
- Service-to-service authentication
- Encrypted data storage
- Secure API endpoints

## Monitoring Setup
- Resource monitoring via Prometheus
- Service health checks
- Model performance tracking
- Pipeline monitoring
- Alert configuration

## Backup Strategy
- MinIO versioning for model artifacts
- ClickHouse data replication
- Configuration backups
- Regular state snapshots

## Scaling Considerations
- Horizontal scaling via K3d
- Vertical scaling limits on M2
- Resource allocation adjustment
- Performance monitoring

## Additional Notes
- All services optimized for ARM64 architecture
- Development environment containerized
- Resource limits configured for stability
- Service mesh consideration for production