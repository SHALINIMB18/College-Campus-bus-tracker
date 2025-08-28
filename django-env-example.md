# Environment Variables for Django

To securely manage sensitive settings (like secret keys, database credentials, etc.), use a `.env` file and the `python-dotenv` package.

## Example `.env` file:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Usage in Django `settings.py`:

Install `python-dotenv`:
```
pip install python-dotenv
```

Add this to the top of your `settings.py`:
```python
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
DATABASE_URL = os.getenv('DATABASE_URL')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

**Never commit your `.env` file to version control. Add it to `.gitignore`.**
