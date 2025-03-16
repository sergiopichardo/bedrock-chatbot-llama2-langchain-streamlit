# bedrock-chatbot-claude3-langchain
Chatbot built with Amazon Bedrock, Claude 3 Haiku, and LangChain

### Overview 
This application is a command-line chatbot that uses Claude 3 Haiku through Amazon Bedrock. It provides an interactive chat experience with message history and robust error handling.

### Architecture 
The application is structured in a single file (`backend.py`) with distinct components:

1. **AWS Configuration:**
   - Bedrock client initialization with SSO support
   - Region-specific configuration (us-east-1)
   - Custom BedrockError class for error handling

2. **LLM Configuration:**
   - Claude 3 Haiku model setup
   - Custom parameters (max_tokens: 300, temperature: 0.9)
   - ChatBedrock integration via LangChain

3. **Chat Implementation:**
   - Interactive command-line interface
   - Message history using ChatMessageHistory
   - System message configuration
   - Error handling with helpful messages

### Understanding the code 
- **Chat Implementation:**
  - Uses ChatMessageHistory for message tracking
  - Implements system prompt for AI behavior
  - Provides clear user/assistant interaction
  - Graceful exit handling with 'exit' command

### Running the code 
1. **Install Dependencies:**
   ```bash
   uv sync
   ```
   This will sync all dependencies from `pyproject.toml` into your virtual environment.

2. **AWS Configuration:**
   ```bash
   aws configure sso
   ```

3. **Starting the Application:**
   ```bash
   uv run backend.py
   ```

### Project Structure
```
.
├── README.md
├── pyproject.toml          # Project dependencies and metadata
└── backend.py             # Main application code
```

### Technologies Used 
- **LangChain**: Framework for building LLM applications
    - **ChatBedrock**: Integration with Amazon Bedrock
    - **ChatMessageHistory**: Message history management
- **Claude 3 Haiku**: Anthropic's LLM accessed through Bedrock
- **Amazon Bedrock**: Managed service for LLM deployment
- **Boto3**: AWS SDK for Python

### Resources 
- [Amazon Bedrock Documentation](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock/create-inference-profile.html)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Claude 3 Documentation](https://docs.anthropic.com/claude/docs)