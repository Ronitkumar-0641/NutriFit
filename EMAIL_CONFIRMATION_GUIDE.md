# 📧 Email Confirmation Guide

## Understanding Email Confirmation

When you register for a NutriFit account, Supabase (our authentication provider) may require you to confirm your email address before you can log in. This is a security feature to ensure that the email address you provided is valid and belongs to you.

## What Happens During Registration?

1. **You create an account** with your email and password
2. **Supabase sends a confirmation email** to your inbox
3. **You must click the confirmation link** in the email
4. **After confirmation, you can log in** to your account

## ❌ "Email not confirmed" Error

If you see this error when trying to log in, it means you haven't clicked the confirmation link in your email yet.

### Solutions:

#### Option 1: Check Your Email
1. Open your email inbox
2. Look for an email from Supabase (check spam/junk folder too!)
3. Click the confirmation link in the email
4. Return to NutriFit and try logging in again

#### Option 2: Resend Confirmation Email
1. Try to log in with your email and password
2. When you see the "Email not confirmed" error
3. Click the **"📧 Resend Confirmation Email"** button that appears
4. Check your email for the new confirmation link
5. Click the link and try logging in again

#### Option 3: Disable Email Confirmation (For Testing/Development)

If you're a developer or testing the application, you can disable email confirmation in Supabase:

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Navigate to: **Authentication → Settings**
4. Find **"Enable email confirmations"**
5. Toggle it **OFF**
6. Save changes
7. Try registering and logging in again

**Note:** Disabling email confirmation is not recommended for production environments as it reduces security.

## 💡 Tips

- **Check spam folder:** Confirmation emails sometimes end up in spam
- **Wait a few minutes:** Email delivery can take a few minutes
- **Use a valid email:** Make sure you're using a real email address you have access to
- **Whitelist Supabase:** Add Supabase emails to your contacts to prevent them from going to spam

## 🔧 For Developers

### How the Email Confirmation Works

The authentication flow has been updated to handle email confirmation gracefully:

1. **Backend (`backend/auth.py`):**
   - Detects "Email not confirmed" errors from Supabase
   - Returns a specific error message with helpful instructions
   - Provides a `resend_confirmation_email()` method

2. **Frontend (`frontend/pages/1_🔐_Login.py`):**
   - Displays a user-friendly error message
   - Shows a "Resend Confirmation Email" button when needed
   - Provides tips about checking spam folders

3. **Registration (`frontend/pages/2_📝_Register.py`):**
   - Informs users to check their email after registration
   - Handles both confirmed and unconfirmed registration flows

### Testing Email Confirmation

To test the email confirmation flow:

```python
# Test registration
result = AuthService.sign_up("test@example.com", "SecurePass123!", "Test User")

# Test login with unconfirmed email (will fail)
result = AuthService.sign_in("test@example.com", "SecurePass123!")
# Returns: {"success": False, "email_not_confirmed": True, ...}

# Resend confirmation email
result = AuthService.resend_confirmation_email("test@example.com")
```

## 🆘 Still Having Issues?

If you're still experiencing problems:

1. **Verify your Supabase configuration:**
   - Check that `SUPABASE_URL` and `SUPABASE_API_KEY` are set correctly in `.env`
   - Ensure your Supabase project is active

2. **Check Supabase logs:**
   - Go to your Supabase dashboard
   - Navigate to Authentication → Users
   - Check if the user exists and their confirmation status

3. **Try a different email:**
   - Some email providers may block automated emails
   - Try using a different email service (Gmail, Outlook, etc.)

4. **Contact support:**
   - If all else fails, check the Supabase documentation or contact their support

## 📚 Related Documentation

- [Supabase Authentication Documentation](https://supabase.com/docs/guides/auth)
- [Email Confirmation Settings](https://supabase.com/docs/guides/auth/auth-email)
- [Troubleshooting Auth Issues](https://supabase.com/docs/guides/auth/debugging/error-codes)