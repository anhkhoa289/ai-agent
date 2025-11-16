# Quick Provider Switch Guide

Hướng dẫn nhanh để chuyển đổi giữa các AI providers.

## 🎯 Cách Chuyển Provider

### Bước 1: Điền API Keys vào `.env`

Mở file `.env` và điền API keys của bạn:

```bash
# Chỉ cần điền key cho providers bạn muốn dùng
ANTHROPIC_API_KEY=sk-ant-xxx...
OPENAI_API_KEY=sk-xxx...
GOOGLE_API_KEY=AIzaSy-xxx...
GROQ_API_KEY=gsk_xxx...
```

### Bước 2: Chọn Provider

Trong file `.env`, thay đổi 2 dòng sau:

```bash
LLM_PROVIDER=anthropic  # Đổi thành: anthropic, openai, gemini, groq, ollama
MODEL_NAME=claude-sonnet-4-5-20250929  # Đổi model tương ứng
```

### Bước 3: Restart Server

```bash
# Ctrl+C để dừng server hiện tại
python main.py
```

## 📋 Quick Switch Examples

Copy và paste các ví dụ sau vào file `.env` của bạn:

### 1️⃣ Anthropic Claude Sonnet 4.5 (Mặc định - Chất lượng cao nhất)

```bash
LLM_PROVIDER=anthropic
MODEL_NAME=claude-sonnet-4-5-20250929
```

**Khi nào dùng:** Cần chất lượng tốt nhất, có ngân sách vừa phải

---

### 2️⃣ OpenAI GPT-4o (Tiêu chuẩn ngành)

```bash
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o
```

**Khi nào dùng:** Cần sự ổn định, đã quen với OpenAI

---

### 3️⃣ OpenAI GPT-4o Mini (Nhanh & Rẻ)

```bash
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
```

**Khi nào dùng:** Cần tiết kiệm chi phí, tasks đơn giản
**Chi phí:** Rẻ hơn GPT-4o **95%** (~$0.15/$0.60 per 1M tokens)

---

### 4️⃣ Google Gemini Pro (Chất lượng cao, giá tốt)

```bash
LLM_PROVIDER=gemini
MODEL_NAME=gemini-1.5-pro
```

**Khi nào dùng:** Cần chất lượng tốt với giá rẻ hơn
**Chi phí:** ~$1.25/$5.00 per 1M tokens

---

### 5️⃣ Google Gemini Flash (Rất nhanh & rẻ)

```bash
LLM_PROVIDER=gemini
MODEL_NAME=gemini-1.5-flash
```

**Khi nào dùng:** Cần tốc độ cao, chi phí thấp
**Chi phí:** Cực rẻ ~$0.075/$0.30 per 1M tokens
**Tốc độ:** Rất nhanh, phù hợp cho production

---

### 6️⃣ Groq Llama 3.1 70B (Miễn phí & siêu nhanh)

```bash
LLM_PROVIDER=groq
MODEL_NAME=llama-3.1-70b-versatile
```

**Khi nào dùng:** Cần tốc độ cực nhanh, có free tier
**Chi phí:** FREE tier có sẵn!
**Tốc độ:** Siêu nhanh (~300 tokens/s)

---

### 7️⃣ Ollama Local (Miễn phí, riêng tư, offline)

```bash
LLM_PROVIDER=ollama
MODEL_NAME=llama2
```

**Setup trước khi dùng:**
```bash
# 1. Cài Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull model
ollama pull llama2

# 3. Chạy Ollama
ollama serve
```

**Khi nào dùng:**
- Cần privacy tuyệt đối
- Không muốn gửi data ra ngoài
- Không có internet hoặc muốn tiết kiệm 100% chi phí
- Có GPU mạnh để chạy local

---

## 💡 Tips Chuyển Provider

### Test Nhanh Một Provider

Không cần restart server, chỉ cần:

1. Stop server (Ctrl+C)
2. Sửa `.env`:
   ```bash
   LLM_PROVIDER=gemini
   MODEL_NAME=gemini-1.5-flash
   ```
3. Start lại: `python main.py`
4. Test API: `curl http://localhost:8000/api/v1/crewai/test`

### So Sánh Providers

Để test cùng một request với nhiều providers:

```bash
# 1. Test với Anthropic
LLM_PROVIDER=anthropic
MODEL_NAME=claude-sonnet-4-5-20250929
# Chạy test, ghi lại kết quả

# 2. Test với Gemini
LLM_PROVIDER=gemini
MODEL_NAME=gemini-1.5-pro
# Chạy test, so sánh kết quả

# 3. Test với Groq (nhanh nhất)
LLM_PROVIDER=groq
MODEL_NAME=llama-3.1-70b-versatile
# Chạy test, so sánh tốc độ
```

## 📊 So Sánh Nhanh

| Provider | Model | Chi phí | Tốc độ | Chất lượng | Use Case |
|----------|-------|---------|--------|------------|----------|
| Anthropic | Sonnet 4.5 | $$ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Production, critical tasks |
| OpenAI | GPT-4o | $$ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Production, familiar |
| OpenAI | GPT-4o Mini | $ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Cost-effective |
| Gemini | Pro | $ | ⚡⚡⚡ | ⭐⭐⭐⭐ | Best value |
| Gemini | Flash | $ | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | High volume |
| Groq | Llama 3.1 | FREE | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Speed critical |
| Ollama | Local | FREE | ⚡⚡⚡ | ⭐⭐⭐ | Privacy, offline |

## 🔧 Troubleshooting

### Lỗi: "API key for X is not set"

```bash
# Check .env có đúng key chưa
cat .env | grep ANTHROPIC_API_KEY

# Phải có key thật, không phải placeholder
ANTHROPIC_API_KEY=sk-ant-xxx  # ✓ Đúng
ANTHROPIC_API_KEY=your_key     # ✗ Sai - vẫn là placeholder
```

### Lỗi: "Authentication failed"

- Check API key có đúng không
- Check API key có hết hạn hoặc hết credits không
- Verify lại trên trang console của provider

### Ollama không chạy

```bash
# Check Ollama có đang chạy không
ollama list

# Nếu chưa chạy, start Ollama
ollama serve

# Pull model nếu chưa có
ollama pull llama2
```

## 📚 Tài Liệu Chi Tiết

Xem thêm: [docs/LLM_PROVIDERS.md](LLM_PROVIDERS.md)
