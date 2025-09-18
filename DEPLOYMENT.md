# Deployment Guide for Roots to Realities

This Django application is ready for deployment to various cloud platforms. Here are the deployment options:

## Prerequisites

1. Your application is now configured for production deployment
2. All necessary dependencies are in `requirements.txt`
3. Environment variables are configured (see `.env.example`)

## Deployment Options

### Option 1: Heroku (Recommended)

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   heroku config:set PAYFAST_MERCHANT_ID="10041623"
   heroku config:set PAYFAST_MERCHANT_KEY="7busob28glxau"
   heroku config:set SITE_URL="https://your-app-name.herokuapp.com"
   ```

4. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push heroku main
   ```

6. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 2: Railway

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.railway.app`
   - PayFast settings
   - `SITE_URL=https://your-domain.railway.app`

3. **Deploy automatically** when you push to GitHub

### Option 3: PythonAnywhere

1. **Upload your code** to PythonAnywhere
2. **Create a web app** with manual configuration
3. **Set up virtual environment** and install requirements
4. **Configure WSGI file** to point to your Django app
5. **Set environment variables** in the web app configuration

## Post-Deployment Steps

1. **Update PayFast URLs** in your PayFast merchant account:
   - Return URL: `https://yourdomain.com/payfast/return/`
   - Cancel URL: `https://yourdomain.com/payfast/cancel/`
   - Notify URL: `https://yourdomain.com/payfast/notify/`

2. **Test the application**:
   - User registration and login
   - VR experience booking
   - Payment processing
   - Admin interface

3. **Monitor logs** for any issues

## Environment Variables Reference

- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain name(s)
- `DATABASE_URL`: PostgreSQL connection string (auto-set by hosting platforms)
- `SITE_URL`: Your deployed application URL
- PayFast configuration variables

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique secret keys for production
- Enable HTTPS in production
- Regularly update dependencies

## Support

For deployment issues, check the logs of your hosting platform or contact their support.