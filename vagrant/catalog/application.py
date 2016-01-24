#!/usr/bin/env python
from app import app, app_config

if __name__ == '__main__':
    app.run(host=app_config.HOST,
            port=app_config.PORT)
