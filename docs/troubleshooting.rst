Troubleshooting Guide
=====================

Common Issues and Solutions
---------------------------

**1. Database Connection Errors**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Symptoms*: "Unable to connect to database", SQLAlchemy errors

*Solutions*:
   - Check PostgreSQL is running: `sudo service postgresql status`
   - Verify credentials in `.env` file match your PostgreSQL setup
   - Try connecting with: `psql -U postgres -h localhost`

**2. "Module Not Found" Errors**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Symptoms*: Import errors when running app.py

*Solutions*:
   - Make sure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python path includes project root

**3. Docker Compose Issues**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Symptoms*: Containers won't start, port conflicts

*Solutions*:
   - Stop existing containers: `docker-compose down`
   - Check for port conflicts (5000, 5432)
   - Rebuild images: `docker-compose build --no-cache`
   - Check Docker logs: `docker-compose logs`

**4. Application Runs but Pages Don't Load**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Symptoms*: Flask runs but browser shows errors

*Solutions*:
   - Check Flask is running on correct port (default: 5000)
   - Look for errors in terminal where Flask is running
   - Clear browser cache and cookies
   - Check `logs/log.txt` for application errors

**5. "Template Not Found" Errors**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Symptoms*: Jinja2 template errors

*Solutions*:
   - Verify template files exist in `templates/` directory
   - Check for typos in template names
   - Ensure Flask is configured with correct template folder

Debugging Steps
---------------

1. **Check Logs**: Always look at `logs/log.txt` first
2. **Simplify**: Comment out recent changes to isolate issues
3. **Test Components**: Test database, routes, and templates separately
4. **Use Print Statements**: Add `print()` statements to trace execution
5. **Check Console**: Look for JavaScript errors in browser console

Getting Help
------------

If issues persist:

1. Check the project's GitHub Issues page
2. Search for similar problems online (include error messages)
3. Ask for help in class forums or with classmates
4. Review Flask and SQLAlchemy documentation

Known Limitations
-----------------

* The search feature only searches users, not posts or media
* No pagination for posts (could be slow with many users)
* No input validation on all form fields
* Basic error handling - some errors may show technical details to users