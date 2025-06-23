# Ollama API Wrapper Proxy

## Breakdown

This project extends the buildin Ollama API with a proxy via Vercel and user auth with Supabase. All features are janky at best... but they work 🤷

## Requesting

### Each request requires 4 fields

- `model-prompt`: the actual prompt for the model
- `model-name`: the name of the model you would like
- `name`: your name as registered in the `users` table of the DB
- `key`: your API key  as registered in the `users` table of the DB

### Example

**Bash**
```bash
curl -X GET \
  -H "model-prompt: Name the 3 most popular programming languages." \
  -H "model-name: gemma3:12b" \
  -H "name: John Doe" \
  -H "key: 0000000000" \
  https://ollama-proxy-server-five.vercel.app/api
```