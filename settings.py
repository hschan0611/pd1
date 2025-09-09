from os import environ

# Default session settings
SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.005,
    'participation_fee': 5.00,
    'doc': "",
}

# Session configurations
SESSION_CONFIGS = [
    dict(
        name='prisoner',
        display_name='Infinitely Repeated PD',
        num_demo_participants=2,
        app_sequence=['prisoner', 'payment'],
        real_world_currency_per_point=1 / 32,  # 32 pts = $1
        participation_fee=8.00,  # $8 show-up fee
    ),
]

# Define participant fields
PARTICIPANT_FIELDS = [
    'progress',
    'bret_points',
    'base_points_total',
    'belief_points_total',
    'pd_points_total',
]


# Language and currency settings
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

# Room configurations
ROOMS = [
    dict(
        name='Prolific_1',
        display_name='Prolific_1',
    ),
]

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')  # Uses environment variable for security

# Production mode setting
OTREE_PRODUCTION = environ.get('OTREE_PRODUCTION', '1')  # Default to production mode

# Debug mode (change to `True` only for development)
DEBUG = False  # ✅ Change to `True` during local testing if needed

# Demo page intro
DEMO_PAGE_INTRO_HTML = "Here are some oTree games."

# Secret key for security
SECRET_KEY = '3105680212138'

# Installed apps
INSTALLED_APPS = ['otree']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Ensures security best practices
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ Enables CSRF protection
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
