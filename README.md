# AI Data Analytics Dashboard

**A comprehensive Streamlit application combining AI chatbot capabilities (OpenAI & Anthropic), interactive data analysis, dynamic dashboards, and API integration tools.**

## Features

- **🤖 AI Chatbot** - Chat with OpenAI GPT-4 or Anthropic Claude with real-time streaming responses and **answers questions about your uploaded data!**
- **📊 Data Analysis** - Upload CSV/JSON files for instant analysis with statistics and insights
- **📈 Interactive Dashboard** - Dynamic visualizations with Plotly (bar charts, line charts, scatter plots, heatmaps, and more)
- **☁️ API Tools** - Connect to REST APIs and external services
- **⚙️ Settings** - Secure API key management and app preferences
- **🔄 Session Persistence** - Data and chat history persist across all pages

## Screenshots

### Home Page
Landing page with quick access to all features

### AI Chatbot
Real-time streaming responses from OpenAI or Anthropic Claude

### Data Analysis
Automatic statistics, filtering, and data exploration

### Dashboard
Interactive visualizations that update based on your data

## Run Locally

```bash
# Clone the repo
git clone <your-repo-url>
cd ai-powered-data-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your actual API keys

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## API Keys Setup

### Get Your API Keys

1. **OpenAI API Key**
   - Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Create an account or sign in
   - Click "Create new secret key"
   - Copy your key

2. **Anthropic API Key**
   - Visit [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
   - Create an account or sign in
   - Generate a new API key
   - Copy your key

### Configure Keys Locally

Edit `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-key"
ANTHROPIC_API_KEY = "sk-ant-your-actual-anthropic-key"
```

**Important:** Never commit `secrets.toml` to version control! It's already in `.gitignore`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make sure `.gitignore` excludes `secrets.toml`)

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app"

4. Connect your GitHub repository

5. Configure secrets:
   - Go to app settings → Secrets
   - Paste your API keys in TOML format:
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   ANTHROPIC_API_KEY = "sk-ant-your-key"
   ```

6. Click "Deploy"

Your app will be live at `https://your-app-name.streamlit.app`


## Deploy to Streamlit in Snowflake

1. Remove `st.set_page_config()` from `app.py` (not supported in Snowflake)

2. Create a Streamlit app in Snowflake:
   ```sql
   CREATE STREAMLIT APP ai_data_hub
   ROOT_LOCATION = '@my_stage/app/'
   MAIN_FILE = 'app.py';
   ```

3. Upload all files to the Snowflake stage

4. Configure secrets in Snowflake

5. Run from Snowflake UI



## Project Structure

```
ai-data-analytics/
├── app.py                          # Main entry point with navigation
├── pages/
│   ├── home.py                     # Home page with overview
│   ├── chatbot.py                  # AI chatbot with streaming
│   ├── data_analysis.py            # Data upload and analysis
│   ├── dashboard.py                # Interactive visualizations
│   ├── api_tools.py                # REST/GraphQL API client
│   └── settings.py                 # Configuration and API keys
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml.example        # Template for API keys
└── README.md                       # This file
```

## Usage Guide

### 1. Configure API Keys
- Navigate to **Settings** page
- Enter your OpenAI and/or Anthropic API keys
- Follow the setup instructions

### 2. Upload Data
- Go to **Data Analysis** page
- Upload CSV or JSON files
- Explore automatic statistics and insights
- Filter and export processed data

### 3. Chat with AI
- Open **AI Chatbot** page
- Select provider (OpenAI or Anthropic)
- Choose model (GPT-4, Claude 3.5 Sonnet, etc.)
- **If you've uploaded data**: Ask questions about it! The chatbot automatically has access to your dataset
- Experience real-time streaming responses

### 4. Visualize Data
- Visit **Dashboard** page
- Select chart type (bar, line, scatter, box, histogram, pie, heatmap)
- Customize axes, colors, and groupings
- Data from uploaded files automatically available

### 5. API Integration
- Navigate to **API Tools**
- Connect to REST APIs or build custom requests
- Test with public APIs (examples provided)
- Save API responses to session for analysis

## Features in Detail

### AI Chatbot
- **Dual Provider Support**: Switch between OpenAI and Anthropic
- **Multiple Models**: Access GPT-4o, Claude 3.5 Sonnet, and more
- **Streaming Responses**: Real-time token-by-token generation
- **Data-Aware Mode**: Automatically answers questions about uploaded data
- **Chat History**: Persistent conversation across sessions
- **Response Caching**: Faster responses for repeated queries

When you upload data in the Data Analysis page, the chatbot automatically gains access to:
- Column names and data types
- Statistical summaries (min, max, mean, etc.)
- Sample rows from your dataset
- Missing value counts

**Example questions to ask:**
- "What's the average value of the sales column?"
- "How many rows have missing data?"
- "What are the top 5 categories by count?"
- "Describe the patterns you see in this data"

### Data Analysis
- **Multi-Format Support**: CSV and JSON file uploads
- **Automatic Statistics**: Descriptive stats for numeric columns
- **Missing Data Analysis**: Identify and visualize gaps
- **Data Explorer**: Filter, sort, and search through data
- **Multiple Export Formats**: Download as CSV, JSON, or Excel

### Interactive Dashboard
- **7 Chart Types**: Bar, line, scatter, box plot, histogram, pie, heatmap
- **Dynamic Configuration**: Customize axes, colors, groupings
- **Correlation Analysis**: Automatic heatmaps for numeric data
- **Quick Statistics**: Key metrics displayed prominently
- **Responsive Design**: Charts adapt to screen size

### API Tools
- **REST API Client**: GET, POST, PUT, DELETE requests
- **Authentication**: Bearer tokens, API keys, basic auth
- **Response Viewer**: JSON formatting and data table views
- **Session Integration**: Save API data for further analysis

## Dependencies

- `streamlit>=1.52.0` - Web app framework
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.14.0` - Interactive visualizations
- `numpy>=1.24.0` - Numerical computing
- `openai>=1.0.0` - OpenAI API client
- `anthropic>=0.18.0` - Anthropic API client
- `requests>=2.31.0` - HTTP requests
- `openpyxl>=3.1.0` - Excel export

## Troubleshooting

### API Key Issues
- Verify keys are correctly formatted in `secrets.toml`
- Check for extra spaces or quotes
- Ensure file is in `.streamlit/` directory
- Restart Streamlit after adding keys

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.9+ recommended)
- Try upgrading pip: `pip install --upgrade pip`

### Data Upload Problems
- Ensure CSV has headers
- JSON must be array of objects or single object
- Check file size limits (default 200MB)
- Verify file encoding is UTF-8

### Slow Performance
- Use `@st.cache_data` for expensive operations
- Limit displayed rows for large datasets
- Consider data sampling for very large files

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions:
- Open an issue on GitHub
- Check Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
- OpenAI docs: [platform.openai.com/docs](https://platform.openai.com/docs)
- Anthropic docs: [docs.anthropic.com](https://docs.anthropic.com)

---

**Built with [Streamlit](https://streamlit.io)**


