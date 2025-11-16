# LLM Provider Configuration Guide

This guide explains how to configure different LLM providers for the Scrum Master AI Agent.

## Supported Providers

The system supports multiple LLM providers through CrewAI's integration with LiteLLM:

- **Anthropic** (Claude)
- **OpenAI** (GPT)
- **Google** (Gemini)
- **Groq** (Fast inference)
- **Ollama** (Local models)

## Configuration

### 1. Choose Your Provider

Set the `LLM_PROVIDER` in your `.env` file:

```bash
LLM_PROVIDER=anthropic  # Options: anthropic, openai, gemini, groq, ollama
```

### 2. Set API Key

Only set the API key for your chosen provider:

#### Anthropic (Claude)

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MODEL_NAME=claude-sonnet-4-5-20250929
```

**Get API Key:** https://console.anthropic.com/

**Available Models:**
- `claude-sonnet-4-5-20250929` - Latest Sonnet model (recommended)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-opus-20240229` - Most capable, slowest
- `claude-3-haiku-20240307` - Fast and affordable

#### OpenAI (GPT)

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4o
```

**Get API Key:** https://platform.openai.com/api-keys

**Available Models:**
- `gpt-4o` - Latest GPT-4 Omni (recommended)
- `gpt-4o-mini` - Fast and affordable
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - Fastest, most affordable

#### Google (Gemini)

```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-key-here
MODEL_NAME=gemini-1.5-pro
```

**Get API Key:** https://makersuite.google.com/app/apikey

**Available Models:**
- `gemini-1.5-pro` - Most capable (recommended)
- `gemini-1.5-flash` - Fast and efficient
- `gemini-2.0-flash-exp` - Experimental latest version

#### Groq (Fast Inference)

```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your-key-here
MODEL_NAME=llama-3.1-70b-versatile
```

**Get API Key:** https://console.groq.com/

**Available Models:**
- `llama-3.1-70b-versatile` - Most capable (recommended)
- `llama-3.1-8b-instant` - Very fast
- `mixtral-8x7b-32768` - Good for long context

#### Ollama (Local Models)

```bash
LLM_PROVIDER=ollama
MODEL_NAME=llama2
# No API key needed for Ollama
```

**Setup:** Install Ollama from https://ollama.ai/

**Available Models:**
- `llama2` - Meta's Llama 2
- `mistral` - Mistral AI
- `codellama` - Code-specialized Llama
- Pull models with: `ollama pull <model-name>`

## Complete Example Configurations

### Example 1: Using Anthropic Claude (Default)

```bash
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-api03-xxx
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Example 2: Using OpenAI GPT-4

```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
MODEL_NAME=gpt-4o
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Example 3: Using Google Gemini

```bash
# .env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSyxxx
MODEL_NAME=gemini-1.5-pro
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Example 4: Using Groq for Fast Inference

```bash
# .env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxx
MODEL_NAME=llama-3.1-70b-versatile
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### Example 5: Using Local Ollama

```bash
# .env
LLM_PROVIDER=ollama
MODEL_NAME=llama2
MAX_TOKENS=4096
TEMPERATURE=0.7

# Make sure Ollama is running:
# ollama serve
```

## Model Parameters

### MAX_TOKENS

Maximum number of tokens in the response.

- **Anthropic:** Up to 4096 (Claude 3) or 8192 (newer models)
- **OpenAI:** Up to 4096 (GPT-4), 16384 (GPT-4 Turbo)
- **Gemini:** Up to 2048 (standard), 32768 (with special config)
- **Groq:** Varies by model
- **Ollama:** Depends on model

### TEMPERATURE

Controls randomness in responses (0.0 to 1.0).

- **0.0-0.3:** More focused and deterministic (good for factual tasks)
- **0.4-0.7:** Balanced creativity and consistency (recommended)
- **0.8-1.0:** More creative and varied responses

## Switching Providers

To switch providers:

1. Update `LLM_PROVIDER` in `.env`
2. Set the appropriate API key
3. Update `MODEL_NAME` to match the provider
4. Restart your application

```bash
# Restart the FastAPI server
# Ctrl+C to stop, then:
python -m uvicorn src.main:app --reload
```

## Cost Comparison

| Provider | Model | Cost per 1M Input Tokens | Cost per 1M Output Tokens |
|----------|-------|--------------------------|---------------------------|
| Anthropic | Claude Sonnet 4.5 | $3.00 | $15.00 |
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o Mini | $0.15 | $0.60 |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 |
| Groq | Llama 3.1 70B | Free tier available | - |
| Ollama | Any | Free (local) | Free (local) |

*Prices as of January 2025, check provider websites for current pricing*

## Troubleshooting

### Error: "API key for X is not set"

Make sure you've set the correct API key in `.env`:
- Check the variable name matches your provider
- Restart your application after updating `.env`
- Verify the API key is valid

### Error: "Authentication failed"

- Verify your API key is correct
- Check if your API key has sufficient credits/quota
- Ensure you're using the right API key for the provider

### Error: "Model not found"

- Verify the model name is correct for your provider
- For Ollama, make sure you've pulled the model: `ollama pull <model-name>`
- Check the model is available in your region (some providers have regional restrictions)

### Slow Response Times

- Try a faster model (e.g., GPT-4o Mini, Gemini Flash, Groq)
- Use Ollama for local inference (no network latency)
- Reduce `MAX_TOKENS` if you don't need long responses

## Additional Resources

- [CrewAI LLM Documentation](https://docs.crewai.com/concepts/llms)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Google AI Studio](https://ai.google.dev/)
- [Groq Documentation](https://console.groq.com/docs)
- [Ollama Documentation](https://ollama.ai/docs)
