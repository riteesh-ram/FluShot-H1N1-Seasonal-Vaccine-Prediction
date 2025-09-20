# FluShot: H1N1 and Seasonal Vaccine Prediction Platform

## 📌 Project Overview
An innovative machine learning platform designed to predict individuals' likelihood of getting vaccinated for both H1N1 (Swine Flu) and seasonal flu. This project addresses a critical healthcare challenge by using data-driven approaches to understand and predict vaccination patterns.

## 🎯 Business Impact
- Helps healthcare providers optimize vaccine distribution
- Enables data-driven public health planning
- Improves vaccination campaign effectiveness
- Supports resource allocation for healthcare facilities

## 💡 Key Features

### 1. Predictive Analytics
- **Dual Prediction System**
  - H1N1 vaccine uptake probability
  - Seasonal flu vaccine uptake probability
  - Real-time prediction capabilities

- **Flexible Input Methods**
  - Batch processing via CSV files
  - Individual case predictions
  - Automated data preprocessing

### 2. User-Friendly Interface
- Interactive dashboard for project management
- Visual representation of model performance
- Easy file upload and download system
- Project deployment controls

### 3. Project Management
- Create and manage multiple prediction projects
- Deploy/Undeploy models as needed
- Monitor model performance metrics
- Download prediction results

## 🛠️ Technical Stack

### Frontend
- Angular
- TypeScript
- Bootstrap for responsive design
- Chart.js for data visualization

### Backend
- Python
- FastAPI for REST API
- MongoDB for data storage
- Scikit-learn for ML models

## 📊 Prediction Features
The system analyzes various factors including:

### Personal Factors
- Age group
- Education level
- Race
- Sex
- Income level
- Marital status

### Health Indicators
- Chronic medical conditions
- Health insurance status
- Health worker status
- Presence of young children

### Behavioral Factors
- Use of preventive medications
- Preventive behaviors
- Healthcare practices
- Social interaction patterns

### Opinion Metrics
- Vaccine effectiveness perception
- Risk assessment
- Side effects concerns
- Medical recommendations

## 🔄 Workflow

1. **Data Input**
   - Upload CSV files for batch processing
   - Input individual cases through web interface

2. **Processing**
   - Automated data cleaning
   - Feature preprocessing
   - Model application

3. **Output**
   - Probability scores for both vaccine types
   - Downloadable prediction results
   - Performance visualizations

## 💻 Implementation Details

### API Endpoints
```python
- /predictCSV   # Batch predictions
- /predictInd   # Individual predictions
- /trainmodel   # Model training
- /deployModel  # Model deployment
- /getModelInfo # Model statistics
```

### Data Processing Pipeline
```python
# Feature Categories
categorical_features = [
    'race', 'sex', 'marital_status',
    'employment_industry', 'employment_occupation'
]

ordinal_features = [
    'age_group', 'education',
    'income_poverty', 'employment_status'
]
```

## 📈 Technical Highlights

1. **Robust Architecture**
   - Microservices-based design
   - RESTful API implementation
   - Secure data handling

2. **ML Implementation**
   - Automated feature engineering
   - Model persistence
   - Performance monitoring

3. **Data Security**
   - User authentication
   - Project-level access control
   - Secure data transmission

## 🌟 Unique Selling Points

1. **Dual Prediction Capability**
   - Simultaneous prediction for both vaccine types
   - Comprehensive feature analysis

2. **Scalable Design**
   - Handles both individual and batch predictions
   - Supports multiple concurrent projects

3. **User-Centric Features**
   - Intuitive interface
   - Automated data processing
   - Clear visualization of results

## 🔗 Project Structure
```
Project/
├── Angular/                 # Frontend
│   └── src/
│       └── app/
│           ├── dash/       # Dashboard
│           └── services/   # API Services
└── Python Services/        # Backend
    ├── build/             # Model Building
    ├── predict/           # Prediction Logic
    ├── user/             # User Management
    └── configs/          # Configurations
```

## 🎓 Technical Skills Demonstrated

1. **Full-Stack Development**
   - Angular frontend development
   - Python backend implementation
   - RESTful API design

2. **Machine Learning**
   - Predictive modeling
   - Feature engineering
   - Model deployment

3. **Database Management**
   - MongoDB integration
   - Data modeling
   - Query optimization

4. **DevOps**
   - API deployment
   - Service integration
   - Performance monitoring

This project showcases the implementation of machine learning in healthcare, demonstrating both technical expertise and practical business application. It represents a modern approach to healthcare analytics, combining data science with user-friendly interfaces for practical deployment.
