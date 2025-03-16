import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, ProfileNotFound
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import ChatMessageHistory

class BedrockError(Exception):
    """Custom exception for Bedrock-related errors with helpful messages."""
    def __init__(self, error: Exception, help_message: str):
        self.original_error = error
        self.help_message = help_message
        super().__init__(str(error))


def create_bedrock_client(profile_name="default") -> BaseClient:
    """Create a Bedrock runtime client with AWS SSO session."""
    try:
        # Explicitly use profile for clarity
        session = boto3.Session(profile_name=profile_name, region_name='us-east-1')
        return session.client('bedrock-runtime')
    except ProfileNotFound as e:
        raise BedrockError(e, f"Profile '{profile_name}' not found. Check ~/.aws/config or run 'aws configure sso'")
    except ClientError as e:
        if 'ExpiredToken' in str(e):
            raise BedrockError(e, "AWS SSO session expired. Run 'aws sso login' to refresh it.")
        raise BedrockError(e, "Client error occurred. Check credentials and permissions.")
    except Exception as e:
        raise BedrockError(e, "Unexpected error. Verify AWS setup and permissions.")


def initialize_llm(client: BaseClient) -> ChatBedrock:
    """Initialize the Bedrock chat model with Claude 3 Haiku."""
    try:
        return ChatBedrock(
            client=client,
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            model_kwargs={
                "max_tokens": 300,
                "temperature": 0.9,
                "anthropic_version": "bedrock-2023-05-31"
            }
        )
    except ClientError as e:
        raise BedrockError(e, "Check if you have access to Claude 3 Haiku in AWS Bedrock")
    except Exception as e:
        raise BedrockError(e, "Failed to initialize Bedrock LLM model. Check model name and client.")


def chat_with_claude(chat_model: ChatBedrock):
    """Run a simple conversation loop with Claude 3 Haiku."""
    print("Start chatting with Claude 3 Haiku! Type 'exit' to stop.")

    
    chat_history = ChatMessageHistory()


    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        try:
            messages = [
                ("system", "You are a helpful AI assistant. Please provide clear and concise responses."),
                ("human", user_input)
            ]
            response = chat_model.invoke(messages)
            chat_history.add_user_message(user_input)
            chat_history.add_ai_message(response.content)

            print(f"Claude: {response.content}\n")


        except Exception as e:
            print(f"Error during chat: {e}")
            break


if __name__ == "__main__":
    try:
        # Setup client and LLM
        bedrock_client = create_bedrock_client()
        llm_model = initialize_llm(bedrock_client)

        # Start conversation loop
        chat_with_claude(llm_model)

    except BedrockError as e:
        print(f"Error: {e.help_message}\nDetails: {e.original_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")
