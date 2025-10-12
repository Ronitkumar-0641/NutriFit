# NutriFit Troubleshooting Guide

## ImportError: cannot import name 'get_algorithm_by_name' from 'jwt'

### Problem
You may encounter this error when trying to run the NutriFit application:
```
ImportError: cannot import name 'get_algorithm_by_name' from 'jwt' 
(C:\Users\nrk06\AppData\Local\Programs\Python\Python313\Lib\site-packages\jwt\__init__.py)
```

### Root Cause
This error occurs when Python is using the **global Python installation** instead of the **virtual environment (venv)**. The global Python has an incompatible `jwt` package (version 1.4.0) installed, while the venv has the correct `PyJWT` package (version 2.10.1).

### Solution

#### Option 1: Use the Startup Script (Recommended)
The `start_app.ps1` script has been updated to explicitly use the virtual environment:

```powershell
.\start_app.ps1
```

This script will:
- Activate the virtual environment
- Start the backend API using the venv's Python
- Start the frontend using the venv's Streamlit

#### Option 2: Manual Activation
If you prefer to run components manually:

1. **Activate the virtual environment first:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Start the backend:**
   ```powershell
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start the frontend (in a new terminal):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   cd frontend
   streamlit run app.py
   ```

#### Option 3: Use Explicit Paths
Always use the venv's executables directly:

```powershell
# Backend
.\venv\Scripts\python.exe -m uvicorn backend.main:app --reload

# Frontend
.\venv\Scripts\streamlit.exe run frontend\app.py
```

### Verification
To verify your environment is set up correctly, run:

```powershell
.\venv\Scripts\python.exe test_imports.py
```

You should see:
```
✅ jwt module imported successfully
   Version: 2.10.1
   Has get_algorithm_by_name: True
✅ supabase imported successfully
✅ backend.auth imported successfully
```

### Prevention
To avoid this issue in the future:

1. **Always activate the venv** before running any Python commands
2. **Use the startup script** which handles activation automatically
3. **Check which Python is being used:**
   ```powershell
   where.exe python
   ```
   The first result should be: `C:\Users\nrk06\Desktop\NutriFit\venv\Scripts\python.exe`

4. **Verify you're in the venv** by checking your prompt - it should show `(venv)` at the beginning

### Additional Notes

#### Why This Happens
- The global Python installation has a package called `jwt` (version 1.4.0)
- The venv has `PyJWT` (version 2.10.1)
- Both packages use the module name `jwt`, but they are different packages
- The `supabase` library requires `PyJWT`, not `jwt`
- When Python runs outside the venv, it uses the global `jwt` package, causing the import error

#### Package Differences
- **jwt** (1.4.0): A different JWT library by Kohei YOSHIDA
- **PyJWT** (2.10.1): The correct JWT library required by Supabase

## Other Common Issues

### Issue: "Module not found" errors
**Solution:** Reinstall dependencies in the venv:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r frontend\requirements.txt
```

### Issue: Supabase connection errors
**Solution:** Check your `.env` file has the correct credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_key
```

### Issue: Port already in use
**Solution:** Kill the process using the port:
```powershell
# For port 8000 (backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# For port 8501 (frontend)
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

## Getting Help

If you continue to experience issues:

1. Check that all dependencies are installed correctly
2. Verify your `.env` file is configured
3. Ensure you're using Python 3.13 or compatible version
4. Try recreating the virtual environment:
   ```powershell
   Remove-Item -Recurse -Force venv
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -r frontend\requirements.txt
   ```