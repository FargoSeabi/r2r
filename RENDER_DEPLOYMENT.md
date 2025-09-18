# Deploying Roots to Realities to Render

This guide will help you deploy your Django application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Step 1: Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```bash
git init
git add .
git commit -m "Initial commit - ready for Render deployment"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Go to https://render.com and sign in
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Review the configuration and click "Apply"

### Option B: Manual Setup

1. Go to https://render.com and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: roots-to-realities
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn roots_to_realities.wsgi:application`
   - **Plan**: Free

## Step 3: Configure Environment Variables

Set these environment variables in your Render dashboard:

### Required Variables:
- `SECRET_KEY`: Generate a new secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your Render app URL (e.g., `your-app-name.onrender.com`)
- `DATABASE_URL`: Will be auto-populated if you add a PostgreSQL database

### PayFast Configuration:
- `PAYFAST_MERCHANT_ID`: Your PayFast merchant ID
- `PAYFAST_MERCHANT_KEY`: Your PayFast merchant key
- `PAYFAST_PASSPHRASE`: Your PayFast passphrase
- `PAYFAST_ENVIRONMENT`: `sandbox` for testing, `live` for production

### Site Configuration:
- `SITE_URL`: Your full app URL (e.g., `https://your-app-name.onrender.com`)

## Step 4: Add a Database (Optional)

If you want to use PostgreSQL instead of SQLite:

1. In your Render dashboard, click "New +" and select "PostgreSQL"
2. Choose the free plan
3. Once created, copy the "External Database URL"
4. Add it as the `DATABASE_URL` environment variable in your web service

## Step 5: Deploy and Test

1. Render will automatically build and deploy your application
2. Once deployed, visit your app URL
3. Test all functionality including:
   - User registration/login
   - Ticket purchasing
   - PayFast integration (in sandbox mode)

## Step 6: Post-Deployment

### Create a Superuser
Access your app's shell to create an admin user:

1. Go to your web service dashboard
2. Click "Shell" tab
3. Run: `python manage.py createsuperuser`

### Monitor Logs
- Check the "Logs" tab in your Render dashboard for any issues
- Monitor performance and errors

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the build logs for missing dependencies
2. **Static Files Not Loading**: Ensure `STATIC_URL` and `STATIC_ROOT` are configured
3. **Database Errors**: Verify `DATABASE_URL` is set correctly
4. **PayFast Issues**: Ensure all PayFast environment variables are set

### Getting Help:
- Check Render's documentation: https://render.com/docs
- Review Django deployment best practices
- Check application logs in the Render dashboard

## Security Notes

- Never commit sensitive environment variables to your repository
- Use strong, unique passwords for your database
- Regularly update your dependencies
- Monitor your application for security vulnerabilities

## Scaling

Render's free tier includes:
- 750 hours/month of runtime
- Automatic SSL certificates
- Custom domains (on paid plans)

For production applications, consider upgrading to a paid plan for:
- Always-on services
- More resources
- Priority support

---

Your Django application should now be successfully deployed on Render! 🎉