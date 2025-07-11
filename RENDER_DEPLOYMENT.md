# 🚀 Render Deployment Guide - LangChain API

This guide will help you deploy your LangChain API to Render for free!

## 🎯 **Why Render?**

- **Free Tier:** 750 hours/month (enough for 24/7 usage)
- **Easy Deployment:** Connect GitHub, auto-deploy
- **Custom Domains:** Add your own domain
- **SSL Certificate:** Automatic HTTPS
- **Great Performance:** Fast and reliable

---

## 📋 **Step-by-Step Deployment**

### **Step 1: Prepare Your Repository**

Make sure these files are in your GitHub repository:
- ✅ `api_app.py` - Main FastAPI application
- ✅ `requirements.txt` - Python dependencies
- ✅ `static/index.html` - Web interface
- ✅ `.gitignore` - Exclude sensitive files

### **Step 2: Deploy to Render**

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub** (recommended)
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repository**
5. **Configure the service:**

#### **Basic Settings:**
- **Name:** `langchain-api` (or your preferred name)
- **Environment:** `Python 3`
- **Region:** Choose closest to your team
- **Branch:** `main` (or your default branch)

#### **Build & Deploy Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn api_app:app --host 0.0.0.0 --port $PORT`

### **Step 3: Set Environment Variables**

In Render dashboard:
1. Go to your service
2. Click "Environment" tab
3. Add these variables:

| Variable Name | Value |
|---------------|-------|
| `OPENAI_API_KEY` | `your_openai_api_key_here` |

### **Step 4: Deploy!**

1. Click "Create Web Service"
2. Render will build and deploy your app
3. Wait 2-5 minutes for deployment
4. Get your URL: `https://your-app-name.onrender.com`

---

## 🌐 **Your Deployed API**

Once deployed, your team can access:

### **Base URL:** `https://your-app-name.onrender.com`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/ui` | GET | Beautiful web interface |
| `/docs` | GET | Interactive API docs |
| `/chat` | POST | AI Chat with memory |
| `/document-qa` | POST | Document Q&A |
| `/code/analyze` | POST | Code analysis |
| `/code/generate` | POST | Code generation |
| `/sessions` | GET | Active chat sessions |

---

## 🧪 **Testing Your Deployment**

### **1. Health Check**
```bash
curl https://your-app-name.onrender.com/
```

### **2. Test Web Interface**
Open in browser: `https://your-app-name.onrender.com/ui`

### **3. Test Chat API**
```bash
curl -X POST "https://your-app-name.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### **4. Test Document Q&A**
```bash
curl -X POST "https://your-app-name.onrender.com/document-qa" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is LangChain?"}'
```

---

## 📊 **Render Dashboard Features**

### **Monitoring:**
- **Logs:** Real-time application logs
- **Metrics:** CPU, memory usage
- **Deployments:** Automatic deployments from GitHub
- **Health Checks:** Automatic health monitoring

### **Settings:**
- **Auto-Deploy:** Enable/disable automatic deployments
- **Environment Variables:** Manage secrets
- **Custom Domains:** Add your own domain
- **SSL:** Automatic HTTPS certificates

---

## 🔒 **Security Best Practices**

### **For Production:**
1. **Environment Variables:** Never commit API keys to code
2. **Rate Limiting:** Consider adding rate limiting
3. **CORS:** Configure for your domain only
4. **Monitoring:** Set up alerts for errors

### **Quick Security Enhancement:**
Add to your `api_app.py`:

```python
# Add basic rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to endpoints
@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    # ... existing code
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **Build Fails:**
   - Check `requirements.txt` has all dependencies
   - Ensure Python version compatibility
   - Check build logs in Render dashboard

2. **Runtime Errors:**
   - Verify environment variables are set
   - Check application logs
   - Ensure API key is valid

3. **Cold Start:**
   - First request might be slow (30-60 seconds)
   - Subsequent requests will be faster
   - This is normal for free tier

4. **FAISS Issues:**
   - Render should handle FAISS installation automatically
   - If issues persist, check build logs

### **Getting Help:**
- **Render Logs:** Check logs in dashboard
- **Build Logs:** See what happened during deployment
- **Environment:** Verify variables are set correctly

---

## 📈 **Monitoring & Alerts**

### **Set Up Alerts:**
1. Go to your service in Render
2. Click "Alerts" tab
3. Set up notifications for:
   - Deployment failures
   - High error rates
   - Service downtime

### **Health Checks:**
```bash
# Check if service is responding
curl https://your-app-name.onrender.com/

# Check API documentation
curl https://your-app-name.onrender.com/docs
```

---

## 🎉 **Sharing with Your Team**

### **Email Template:**
```
Subject: LangChain API - Now Live on Render!

Hi Team,

Our LangChain API is now deployed and ready for testing!

🌐 **Web Interface:** https://your-app-name.onrender.com/ui
📚 **API Documentation:** https://your-app-name.onrender.com/docs
🔍 **Health Check:** https://your-app-name.onrender.com/

**Features Available:**
✅ AI Chat with conversation memory
✅ Document Q&A with semantic search
✅ Code analysis and suggestions
✅ Code generation from descriptions

**How to Test:**
1. Open the web interface for easy testing
2. Use Postman with the API endpoints
3. Check the documentation for examples

**API Endpoints:**
- POST /chat - Chat with AI
- POST /document-qa - Ask questions about documents
- POST /code/analyze - Analyze code
- POST /code/generate - Generate code

Let me know if you need help or have questions!

Best regards,
[Your Name]
```

---

## 💡 **Pro Tips**

1. **Custom Domain:** Add your own domain in Render settings
2. **Auto-Deploy:** Every push to GitHub triggers deployment
3. **Environment Separation:** Use different API keys for dev/prod
4. **Monitoring:** Set up alerts for important events
5. **Backup:** Keep local copies of your code

---

## 🆘 **Need Help?**

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **Render Support:** [render.com/support](https://render.com/support)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

Your API will be live and accessible to your team in minutes! 🚀 