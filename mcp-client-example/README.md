# MCP Client Examples

This project provides multiple MCP (Model Control Protocol) client examples for interacting with different AI models, including OpenAI GPT-4, Anthropic Claude, and Deepseek AI.

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root directory and add the corresponding API keys based on the model you want to use:

```env
# OpenAI API key (for GPT-4)
OPENAI_API_KEY=your_openai_api_key

# Anthropic API key (for Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Deepseek API key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## Usage

The project provides three client examples, each corresponding to a different AI model:

### OpenAI GPT-4 Client
```bash
python openai_example.py path/to/ebook-mcp_project/main.py
```

### Anthropic Claude Client
```bash
python anthropic_example.py path/to/ebook-mcp_project/main.py
```

### Deepseek AI Client
```bash
python deepseek_example.py path/to/ebook-mcp_project/main.py
```

## Example Conversation

Here's an example of interacting with an ebook using the MCP client with DeepSeek:

```
Query: Can you ask me a few questions to test my understanding of this book?

[AI generated 5 questions about "Elon Musk", including:
1. How his childhood and family background shaped his personality and career
2. What problems Zip2 and X.com (later PayPal) solved
3. How SpaceX and Tesla survived the crisis in 2008
4. What controversies surround his management style
5. What his attitude toward artificial intelligence is]

Query: 
Question 1: His father's abusive attitude made him less empathetic towards others.
Question 2: Zip2 solved the problem of electronic maps and online yellow pages. X.com solved online payments.
Question 3: He secured a contract with NASA. Tesla solved its production problems by building a factory in China.
Question 4: I don't know. Please answer for me.
Question 5: He believes open-source technology is necessary to ensure AI is safe and open.
```

## Notes

- Make sure you have configured the appropriate API keys
- Each client generates log files in the `logs` directory. Use those log's tu understand the conversation and tools usage.
- Use the `clear` command to clear conversation history(not implement in deepseek version)
- Use the `quit` command to exit the program

## Contributing
Issues and suggestions for improvements are welcome!

