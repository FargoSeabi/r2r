# Roots to Realities - Testing Checklist

## 🧪 Application Testing Guide

Use this checklist to verify that your application works correctly both locally and on the deployed version.

### **Local Testing**: http://127.0.0.1:8000/
### **Deployed Testing**: https://roots-to-realities.onrender.com/

---

## ✅ **Core Functionality Tests**

### **1. Homepage & Navigation**
- [ ] Homepage loads correctly
- [ ] Navigation menu works
- [ ] All links are functional
- [ ] Responsive design on mobile/tablet
- [ ] Static files (CSS, images) load properly

### **2. User Authentication**
- [ ] User registration form works
- [ ] User can create new account
- [ ] Login functionality works
- [ ] Logout functionality works
- [ ] Password validation works
- [ ] User profile access

### **3. Ticket System**
- [ ] Ticket listing page loads
- [ ] Individual ticket details display
- [ ] Ticket selection works
- [ ] Add to cart functionality
- [ ] Cart displays correctly
- [ ] Quantity adjustments work

### **4. Payment Integration (PayFast)**
- [ ] Checkout process initiates
- [ ] PayFast redirect works (sandbox mode)
- [ ] Payment form displays correctly
- [ ] Test payment processing
- [ ] Return URL handling
- [ ] Payment confirmation page
- [ ] Receipt generation

### **5. Database Operations**
- [ ] User data saves correctly
- [ ] Order records created
- [ ] Customer information stored
- [ ] Payment status updates
- [ ] Data persistence across sessions

### **6. Admin Panel**
- [ ] Admin login works (`/admin/`)
- [ ] User management interface
- [ ] Order management
- [ ] Ticket management
- [ ] Customer data access

---

## 🔧 **Technical Tests**

### **7. Security & Performance**
- [ ] HTTPS enabled (deployed version)
- [ ] CSRF protection working
- [ ] Session security
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] Page load times acceptable

### **8. Error Handling**
- [ ] 404 pages display correctly
- [ ] Form validation errors show
- [ ] Payment failure handling
- [ ] Database connection errors
- [ ] Graceful error messages

### **9. Environment-Specific**

#### **Local Development**
- [ ] Debug mode shows detailed errors
- [ ] SQLite database works
- [ ] Static files served by Django
- [ ] Hot reload works

#### **Production (Render)**
- [ ] Debug mode disabled
- [ ] PostgreSQL database connected
- [ ] Static files served by WhiteNoise
- [ ] Environment variables loaded
- [ ] Logs accessible in Render dashboard

---

## 🎯 **User Journey Tests**

### **Complete User Flow**
1. [ ] Visit homepage
2. [ ] Browse available tickets
3. [ ] Register new user account
4. [ ] Login with credentials
5. [ ] Select tickets for purchase
6. [ ] Add items to cart
7. [ ] Proceed to checkout
8. [ ] Complete payment process (sandbox)
9. [ ] Receive confirmation
10. [ ] View order history
11. [ ] Logout successfully

### **Admin Workflow**
1. [ ] Access admin panel
2. [ ] Create superuser account
3. [ ] Add new ticket types
4. [ ] View customer orders
5. [ ] Process payments
6. [ ] Generate reports

---

## 🐛 **Common Issues to Check**

### **Deployment-Specific**
- [ ] Environment variables set correctly
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] ALLOWED_HOSTS configured
- [ ] PayFast URLs updated for production

### **PayFast Integration**
- [ ] Merchant credentials configured
- [ ] Sandbox mode enabled for testing
- [ ] Return URLs accessible
- [ ] Signature validation working
- [ ] Payment notifications handled

### **Database Issues**
- [ ] Migrations up to date
- [ ] Foreign key relationships intact
- [ ] Data integrity maintained
- [ ] Connection pooling working

---

## 📊 **Performance Benchmarks**

### **Page Load Times** (Target: < 3 seconds)
- [ ] Homepage: _____ seconds
- [ ] Ticket listing: _____ seconds
- [ ] Checkout page: _____ seconds
- [ ] Payment redirect: _____ seconds

### **Database Queries**
- [ ] No N+1 query problems
- [ ] Efficient database usage
- [ ] Proper indexing

---

## 🚨 **Critical Issues to Report**

If any of these fail, they need immediate attention:

1. **Application won't start**
2. **Database connection errors**
3. **Payment processing failures**
4. **Security vulnerabilities**
5. **Data loss or corruption**
6. **Authentication bypass**

---

## 📝 **Testing Notes**

**Date**: _______________
**Tester**: _______________
**Environment**: [ ] Local [ ] Deployed
**Browser**: _______________
**Device**: _______________

### **Issues Found**:
```
Issue 1: 
Description: 
Severity: [ ] Critical [ ] High [ ] Medium [ ] Low
Status: [ ] Open [ ] Fixed [ ] Deferred

Issue 2:
Description: 
Severity: [ ] Critical [ ] High [ ] Medium [ ] Low
Status: [ ] Open [ ] Fixed [ ] Deferred
```

### **Overall Assessment**:
- [ ] ✅ All tests passed - Ready for production
- [ ] ⚠️ Minor issues found - Acceptable for launch
- [ ] ❌ Major issues found - Needs fixes before launch

---

## 🎉 **Post-Testing Actions**

After successful testing:
1. [ ] Document any configuration changes needed
2. [ ] Update environment variables if required
3. [ ] Switch PayFast to live mode (when ready)
4. [ ] Set up monitoring and alerts
5. [ ] Create backup procedures
6. [ ] Plan maintenance schedule

---

**Happy Testing! 🚀**