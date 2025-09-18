# Render Environment Variables Setup

## 🚨 **URGENT: Fix Payment Redirect Issue**

The payment page is not redirecting to the Zithulele page because the `SITE_URL` environment variable is not set on Render. Follow these steps to fix it:

## 📋 **Required Environment Variables**

Go to your Render dashboard → Your service → Environment tab and add these variables:

### **Essential Variables (Required)**
```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=roots-to-realities.onrender.com
SITE_URL=https://roots-to-realities.onrender.com
```

### **PayFast Configuration (For Payment Processing)**
```
PAYFAST_MERCHANT_ID=10041623
PAYFAST_MERCHANT_KEY=7busob28glxau
PAYFAST_PASSPHRASE=
PAYFAST_ENVIRONMENT=sandbox
```

### **Security Settings (Optional - Auto-configured)**
```
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🔧 **Step-by-Step Fix**

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Select your "roots-to-realities" service

2. **Add Environment Variables**
   - Click "Environment" tab
   - Click "Add Environment Variable"
   - Add each variable from the list above

3. **Most Important Variable**
   ```
   Key: SITE_URL
   Value: https://roots-to-realities.onrender.com
   ```

4. **Deploy Changes**
   - Click "Manual Deploy" or wait for auto-deploy
   - Monitor deployment logs

## ✅ **What This Fixes**

- ✅ PayFast return URLs will use production domain
- ✅ Payment success page will redirect to Zithulele
- ✅ Auto-redirect timer will work correctly
- ✅ All payment flows will function properly

## 🧪 **Testing After Fix**

1. Visit: https://roots-to-realities.onrender.com
2. Complete a test payment
3. Verify redirect to Zithulele page after payment success
4. Check that auto-redirect countdown appears

## 📝 **Notes**

- The code changes have been pushed to GitHub
- Render will auto-deploy the fixes
- Environment variables must be set manually in Render dashboard
- Database URL is automatically provided by Render PostgreSQL addon

## 🆘 **If Still Not Working**

Check Render logs for errors:
1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. Look for any error messages

The payment redirect should work immediately after setting the `SITE_URL` environment variable.